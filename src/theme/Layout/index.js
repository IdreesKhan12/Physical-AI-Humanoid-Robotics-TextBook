import React, { useState } from 'react'; // Import useState
import clsx from 'clsx';
import ErrorBoundary from '@docusaurus/ErrorBoundary';
import {
  PageMetadata,
  SkipToContentFallbackId,
  ThemeClassNames,
} from '@docusaurus/theme-common';
import {useKeyboardNavigation} from '@docusaurus/theme-common/internal';
import SkipToContent from '@theme/SkipToContent';
import AnnouncementBar from '@theme/AnnouncementBar';
import Navbar from '@theme/Navbar';
import Footer from '@theme/Footer';
import LayoutProvider from '@theme/Layout/Provider';
import ErrorPageContent from '@theme/ErrorPageContent';
import styles from './styles.module.css';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Chatbot from '@site/src/components/Chatbot';

export default function Layout(props) {
  const {
    children,
    noFooter,
    wrapperClassName,
    title,
    description,
  } = props;
  useKeyboardNavigation();

  const {siteConfig} = useDocusaurusContext();
  const { ragBackendUrl } = siteConfig.customFields;

  const [isChatbotActive, setIsChatbotActive] = useState(false);

  return (
    <LayoutProvider>
      <PageMetadata title={title} description={description} />

      <SkipToContent />

      <AnnouncementBar />

      <Navbar />

      <div
        id={SkipToContentFallbackId}
        className={clsx(
          ThemeClassNames.layout.main.container,
          ThemeClassNames.wrapper.main,
          styles.mainWrapper,
          { [styles.mainWrapperWithChatbot]: isChatbotActive } // Apply class when chatbot is active
        )}>
        <ErrorBoundary fallback={(params) => <ErrorPageContent {...params} />}>
          {children}
        </ErrorBoundary>
      </div>

      {!noFooter && <Footer />}
      <Chatbot 
        backendUrl={ragBackendUrl} 
        onToggle={(isOpen) => setIsChatbotActive(isOpen)} // Pass callback to update state
      />
    </LayoutProvider>
  );
}
