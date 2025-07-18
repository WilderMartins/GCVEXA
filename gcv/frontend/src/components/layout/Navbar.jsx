import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isAdmin = user && user.roles.includes('Admin');

  if (!isAuthenticated) {
    return null; // Não mostra a navbar em telas de login/cadastro
  }

  return (
    <nav style={{ background: '#eee', padding: '1rem', marginBottom: '1rem' }}>
      <Link to="/" style={{ marginRight: '1rem' }}>Dashboard</Link>
      <Link to="/scans" style={{ marginRight: '1rem' }}>Scans</Link>
      {isAdmin && (
        <Link to="/settings/scanners" style={{ marginRight: '1rem' }}>Settings</Link>
      )}
      <div style={{ float: 'right' }}>
        <span>{user?.email}</span>
        <button onClick={handleLogout} style={{ marginLeft: '1rem' }}>Logout</button>
      </div>
    </nav>
  );
};

export default Navbar;
