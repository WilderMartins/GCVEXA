import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import DashboardPage from './pages/DashboardPage';
import ScansPage from './pages/ScansPage';
import ScanDetailPage from './pages/ScanDetailPage';
import ScannerConfigsPage from './pages/ScannerConfigsPage';
import PrivateRoute from './components/PrivateRoute';
import AdminRoute from './components/AdminRoute';

import MainLayout from './components/layout/MainLayout';
import AccountSecurityPage from './pages/AccountSecurityPage';
import CustomizationPage from './pages/CustomizationPage';
import LoginCallbackPage from './pages/LoginCallbackPage';
import SetupWizardPage from './pages/SetupWizardPage';
import PlaybooksPage from './pages/PlaybooksPage';
import ReportsPage from './pages/ReportsPage';

import SetupGuard from './components/SetupGuard';

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<SetupGuard />}>
          <Route path="/setup" element={<SetupWizardPage />} />
          <Route path="/login" element={<LoginPage />} />
        <Route path="/login/callback" element={<LoginCallbackPage />} />
        <Route path="/signup" element={<SignUpPage />} />

        {/* Rotas com Layout Principal */}
        <Route element={<MainLayout />}>
          {/* Rotas Protegidas */}
          <Route element={<PrivateRoute />}>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/scans" element={<ScansPage />} />
            <Route path="/scans/:scanId" element={<ScanDetailPage />} />
            <Route path="/account/security" element={<AccountSecurityPage />} />
          </Route>

import CustomizationPage from './pages/CustomizationPage';
...
          {/* Rotas de Admin */}
          <Route element={<AdminRoute />}>
            <Route path="/settings/scanners" element={<ScannerConfigsPage />} />
          <Route path="/settings/customization" element={<CustomizationPage />} />
            <Route path="/playbooks" element={<PlaybooksPage />} />
            <Route path="/reporting" element={<ReportsPage />} />
          </Route>
        </Route>
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
