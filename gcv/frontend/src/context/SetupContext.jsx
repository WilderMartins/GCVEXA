import React, { useState, useEffect, createContext, useContext } from 'react';
import api from '../services/api';

const SetupContext = createContext(null);

export const SetupProvider = ({ children }) => {
  const [setupState, setSetupState] = useState({
    needsSetup: null, // null, true, false
    error: null,      // null ou uma mensagem de erro
  });

  useEffect(() => {
    const checkSetupStatus = async () => {
      try {
        const { data } = await api.get('/setup/status');
        setSetupState({ needsSetup: data.needs_setup, error: null });
      } catch (error) {
        console.error("Could not verify setup status.", error);
        setSetupState({
          needsSetup: false, // Previne loop de redirecionamento, mas o erro será mostrado
          error: "Could not connect to the backend. Please ensure all Docker containers are running correctly and try again."
        });
      }
    };
    checkSetupStatus();
  }, []);

  return (
    <SetupContext.Provider value={setupState}>
      {children}
    </SetupContext.Provider>
  );
};

export const useSetup = () => {
  return useContext(SetupContext);
};
