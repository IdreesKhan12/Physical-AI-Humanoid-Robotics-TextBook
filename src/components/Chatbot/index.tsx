import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface Message {
  id: string;
  sender: 'user' | 'agent';
  text: string;
  timestamp: string;
  citations?: { url: string; heading?: string; chunk_text_snippet: string }[];
}

interface ChatbotProps {
  backendUrl: string;
  onToggle: (isOpen: boolean) => void;
}

const Chatbot: React.FC<ChatbotProps> = ({ backendUrl, onToggle }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const [isChatbotOpen, setIsChatbotOpen] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    onToggle(isChatbotOpen);
  }, [isChatbotOpen, onToggle]);
  
  // Scroll to bottom of messages container whenever messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    const handleTextSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim();
      if (text && text.length > 50) {
        setSelectedText(text);
      } else {
        setSelectedText(null);
      }
    };

    document.addEventListener('mouseup', handleTextSelection);
    document.addEventListener('keyup', handleTextSelection);
    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
      document.removeEventListener('keyup', handleTextSelection);
    };
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newUserMessage: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text: input,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, newUserMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      const payload = {
        question: newUserMessage.text,
        selected_text: selectedText,
      };

      const response = await fetch(`${backendUrl}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Backend error: ${response.status}`);
      }

      const agentResponse = await response.json();
      const newAgentMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'agent',
        text: agentResponse.answer,
        timestamp: new Date().toISOString(),
        citations: agentResponse.citations,
      };
      setMessages((prev) => [...prev, newAgentMessage]);
    } catch (err) {
      console.error('Chatbot API error:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred.');
      setMessages((prev) => [...prev, {
        id: (Date.now() + 1).toString(),
        sender: 'agent',
        text: `Error: ${err instanceof Error ? err.message : 'An unknown error occurred.'}`,
        timestamp: new Date().toISOString(),
      }]);
    } finally {
      setIsLoading(false);
      setSelectedText(null);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !isLoading) {
      sendMessage();
    }
  };

  return (
    <>
      <button 
        className={clsx(styles.chatbotToggleButton, { [styles.open]: isChatbotOpen })}
        onClick={() => setIsChatbotOpen(!isChatbotOpen)}
        title={isChatbotOpen ? "Close Chatbot" : "Open Chatbot"}
      >
        {isChatbotOpen ? '✕' : '💬'}
      </button>

      <div className={clsx(styles.chatbotContainer, { [styles.open]: isChatbotOpen })}>
        <div className={styles.messagesContainer}>
          {selectedText && (
            <div className={styles.selectedContext}>
              <strong>Context from selection:</strong> {selectedText.substring(0, 150)}...
              <button onClick={() => setSelectedText(null)} className={styles.clearSelectionButton}>x</button>
            </div>
          )}
          {messages.map((message) => (
            <div key={message.id} className={`${styles.message} ${styles[message.sender]}`}>
              <p className={styles.messageText}>{message.text}</p>
              {message.citations && message.citations.length > 0 && (
                <div className={styles.citations}>
                  <strong>Sources:</strong>
                  {message.citations.map((citation, index) => (
                    <span key={index} className={styles.citation}>
                      <a href={citation.url} target="_blank" rel="noopener noreferrer">
                        {citation.heading || citation.url.split('/').pop()}
                      </a>
                    </span>
                  ))}
                </div>
              )}
              <span className={styles.timestamp}>{new Date(message.timestamp).toLocaleTimeString()}</span>
            </div>
          ))}
          {isLoading && <div className={`${styles.message} ${styles.agent}`}>Thinking...</div>}
          {error && <div className={`${styles.message} ${styles.error}`}>{error}</div>}
          <div ref={messagesEndRef} /> {/* Element to scroll to */}
        </div>
        <div className={styles.inputContainer}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about the book..."
            disabled={isLoading}
            className={styles.textInput}
          />
          <button onClick={sendMessage} disabled={isLoading} className={styles.sendButton}>
            Send
          </button>
        </div>
      </div>
    </>
  );
};

export default Chatbot;
