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

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignUpPage />} />

        {/* Rotas com Layout Principal */}
        <Route element={<MainLayout />}>
          {/* Rotas Protegidas */}
          <Route element={<PrivateRoute />}>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/scans" element={<ScansPage />} />
            <Route path="/scans/:scanId" element={<ScanDetailPage />} />
          </Route>

          {/* Rotas de Admin */}
          <Route element={<AdminRoute />}>
            <Route path="/settings/scanners" element={<ScannerConfigsPage />} />
          </Route>
        </Route>

      </Routes>
    </Router>
  );
}

export default App;
