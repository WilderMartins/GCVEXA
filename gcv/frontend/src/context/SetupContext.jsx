import React, { useState, useEffect, createContext, useContext } from 'react';
import api from '../services/api';

const SetupContext = createContext(null);

export const SetupProvider = ({ children }) => {
  const [needsSetup, setNeedsSetup] = useState(null);

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
