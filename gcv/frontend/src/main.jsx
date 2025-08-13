import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter as Router } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import { AuthProvider } from './context/AuthContext'
import { CustomizationProvider } from './context/CustomizationContext'
import { SetupProvider } from './context/SetupContext'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <SetupProvider>
        <CustomizationProvider>
          <AuthProvider>
            <App />
          </AuthProvider>
        </CustomizationProvider>
      </SetupProvider>
    </Router>
  </StrictMode>,
)
