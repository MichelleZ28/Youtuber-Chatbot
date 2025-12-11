import React from 'react';
import ReactDOM from 'react-dom/client';
import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import App from './App';
import './index.css';

console.log('main.tsx: Starting application...');

const rootElement = document.getElementById('root');

if (!rootElement) {
  console.error('main.tsx: Failed to find root element');
} else {
  console.log('main.tsx: Found root element, rendering App component');
  const root = ReactDOM.createRoot(rootElement);
  const theme = extendTheme({
    fonts: {
      heading: 'Segoe UI, system-ui, -apple-system, sans-serif',
      body: 'Segoe UI, system-ui, -apple-system, sans-serif',
    },
  });
  root.render(
    <React.StrictMode>
      <ChakraProvider theme={theme}>
        <App />
      </ChakraProvider>
    </React.StrictMode>
  );
}
