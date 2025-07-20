import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { AuthProvider } from './context/AuthContext'
import { CustomizationProvider } from './context/CustomizationContext'
import { SetupProvider } from './components/SetupGuard'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SetupProvider>
      <CustomizationProvider>
        <AuthProvider>
          <App />
        </AuthProvider>
      </CustomizationProvider>
    </SetupProvider>
  </StrictMode>,
)
