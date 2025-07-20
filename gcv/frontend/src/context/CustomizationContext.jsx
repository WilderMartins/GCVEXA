import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';

const CustomizationContext = createContext(null);

export const CustomizationProvider = ({ children }) => {
  const [customization, setCustomization] = useState({ app_title: 'GCV', logo_base64: null });

  useEffect(() => {
    fetchCustomization();
  }, []);

  const fetchCustomization = async () => {
    try {
      const { data } = await api.get('/customization/');
      setCustomization(data);
      document.title = data.app_title || 'GCV';
    } catch (error) {
      console.error('Could not fetch customization settings.');
    }
  };

  const updateCustomization = async (customizationData) => {
    const { data } = await api.post('/customization/', customizationData);
    setCustomization(data);
    document.title = data.app_title || 'GCV';
  };

  const value = { customization, updateCustomization };

  return (
    <CustomizationContext.Provider value={value}>
      {children}
    </CustomizationContext.Provider>
  );
};

export const useCustomization = () => {
  return useContext(CustomizationContext);
};
