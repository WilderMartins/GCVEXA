import React, { useState, useEffect } from 'react';
import { useLocation, Navigate, Outlet } from 'react-router-dom';
import api from '../services/api';

const SetupGuard = () => {
  const [needsSetup, setNeedsSetup] = useState(null);
  const location = useLocation();

  useEffect(() => {
    const checkSetupStatus = async () => {
      try {
        const { data } = await api.get('/setup/status');
        setNeedsSetup(data.needs_setup);
      } catch (error) {
        // Se a API falhar, assumimos que algo está errado e não bloqueamos a UI
        console.error("Could not verify setup status.", error);
        setNeedsSetup(false);
      }
    };
    checkSetupStatus();
  }, []);

  if (needsSetup === null) {
    return <div>Loading configuration...</div>; // Ou um spinner
  }

  if (needsSetup && location.pathname !== '/setup') {
    // Se o setup é necessário e não estamos na página de setup, redireciona
    return <Navigate to="/setup" replace />;
  }

  if (!needsSetup && location.pathname === '/setup') {
    // Se o setup não é necessário mas estamos na página de setup, redireciona para o login
    return <Navigate to="/login" replace />;
  }

  // Se tudo estiver ok, renderiza a rota filha
  return <Outlet />;
};

export default SetupGuard;
