
import React, { useState, useEffect, createContext, useContext } from 'react';
import { useLocation, Navigate, Outlet } from 'react-router-dom';
import api from '../services/api';

// Usar um Context para evitar chamadas repetidas da API
const SetupContext = createContext(null);

export const SetupProvider = ({ children }) => {
  const [needsSetup, setNeedsSetup] = useState(null); // null = não verificado, true/false = verificado

  useEffect(() => {
    const checkSetupStatus = async () => {
      try {
        const { data } = await api.get('/setup/status');
        setNeedsSetup(data.needs_setup);
      } catch (error) {
        console.error("Could not verify setup status. Assuming setup is complete.", error);
        setNeedsSetup(false);
      }
    };
    checkSetupStatus();
  }, []);
  return (
    <SetupContext.Provider value={needsSetup}>
      {children}
    </SetupContext.Provider>
  );
};

export const useSetup = () => {
  return useContext(SetupContext);
};

const SetupGuard = () => {
  const needsSetup = useSetup();
  const location = useLocation();

  if (needsSetup === null) {
    return <div>Loading application configuration...</div>;
  }

  if (needsSetup && location.pathname !== '/setup') {
    return <Navigate to="/setup" replace />;
  }

  if (!needsSetup && location.pathname === '/setup') {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};
