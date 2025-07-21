import React from 'react';
import { useLocation, Navigate, Outlet } from 'react-router-dom';
import { useSetup } from '../context/SetupContext';

const SetupGuard = () => {
  const setupState = useSetup();
  const location = useLocation();

  if (setupState === null || setupState.needsSetup === null) {
    return <div>Loading application configuration...</div>;
  }

  if (setupState.error) {
    return (
      <div style={{ padding: '2rem', color: 'red', textAlign: 'center' }}>
        <h1>Connection Error</h1>
        <p>{setupState.error}</p>
      </div>
    );
  }

  if (setupState.needsSetup && location.pathname !== '/setup') {
    return <Navigate to="/setup" replace />;
  }

  if (!setupState.needsSetup && location.pathname === '/setup') {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};
