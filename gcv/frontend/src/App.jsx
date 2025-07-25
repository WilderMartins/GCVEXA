import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

// Guards e Layouts
import SetupGuard from './components/SetupGuard';
import PrivateRoute from './components/PrivateRoute';
import AdminRoute from './components/AdminRoute';
import MainLayout from './components/layout/MainLayout';
import ImportScanPage from './pages/ImportScanPage';

// Páginas Públicas e de Setup
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import LoginCallbackPage from './pages/LoginCallbackPage';
import SetupWizardPage from './pages/SetupWizardPage';

// Páginas Protegidas
import DashboardPage from './pages/DashboardPage';
import AssetsPage from './pages/AssetsPage';
import AssetDetailPage from './pages/AssetDetailPage';
import ScansPage from './pages/ScansPage';
import ScanDetailPage from './pages/ScanDetailPage';
import VulnerabilityDefinitionPage from './pages/VulnerabilityDefinitionPage';
import AccountSecurityPage from './pages/AccountSecurityPage';

// Páginas de Admin
import ScannerConfigsPage from './pages/ScannerConfigsPage';
import CustomizationPage from './pages/CustomizationPage';
import PlaybooksPage from './pages/PlaybooksPage';
import ReportsPage from './pages/ReportsPage';

function App() {
  return (
    <Router>
      <Routes>
        {/* O SetupGuard envolve todas as rotas para a verificação inicial */}
        <Route element={<SetupGuard />}>

          {/* Rotas Públicas */}
          <Route path="/setup" element={<SetupWizardPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/login/callback" element={<LoginCallbackPage />} />
          <Route path="/signup" element={<SignUpPage />} />

          {/* Rotas Protegidas com o Layout Principal */}
          <Route element={<MainLayout />}>
            <Route element={<PrivateRoute />}>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/assets" element={<AssetsPage />} />
              <Route path="/assets/:assetId" element={<AssetDetailPage />} />
              <Route path="/scans" element={<ScansPage />} />
              <Route path="/scans/:scanId" element={<ScanDetailPage />} />
              <Route path="/vulnerabilities/definitions/:definitionId" element={<VulnerabilityDefinitionPage />} />
              <Route path="/account/security" element={<AccountSecurityPage />} />

              {/* Rotas de Admin (também são privadas e usam o MainLayout) */}
              <Route element={<AdminRoute />}>
                <Route path="/settings/scanners" element={<ScannerConfigsPage />} />
                <Route path="/settings/customization" element={<CustomizationPage />} />
                <Route path="/playbooks" element={<PlaybooksPage />} />
                <Route path="/reporting" element={<ReportsPage />} />
                <Route path="/import-scan" element={<ImportScanPage />} />
              </Route>
            </Route>
          </Route>

        </Route>
      </Routes>
    </Router>
  );
}

export default App;
