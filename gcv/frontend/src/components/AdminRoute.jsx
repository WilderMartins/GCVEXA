import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AdminRoute = () => {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  const isAdmin = user && user.roles.includes('Admin');

  return isAdmin ? <Outlet /> : <Navigate to="/" />;
};

export default AdminRoute;
