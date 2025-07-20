
import React from 'react';
import { useLocation, Navigate, Outlet } from 'react-router-dom';
import { useSetup } from '../context/SetupContext';

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

export default SetupGuard;