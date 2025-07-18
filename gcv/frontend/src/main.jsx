import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { AuthProvider } from './context/AuthContext'
import { CustomizationProvider } from './context/CustomizationContext'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <CustomizationProvider>
      <AuthProvider>
        <App />
      </AuthProvider>
    </CustomizationProvider>
  </StrictMode>,
)
