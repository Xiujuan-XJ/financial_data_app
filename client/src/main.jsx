import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import { SnackbarProvider } from 'notistack';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <SnackbarProvider 
      maxSnack={10}
      anchorOrigin={{
        vertical: 'right',
        horizontal: 'top',
      }}
      transitionDuration={300} // Duration of the transition animation in milliseconds
    >
      <App />
    </SnackbarProvider>
  </React.StrictMode>,
)
