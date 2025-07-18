import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useCustomization } from '../../context/CustomizationContext';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const { customization } = useCustomization();
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
    <nav style={{ display: 'flex', alignItems: 'center', background: '#eee', padding: '1rem', marginBottom: '1rem' }}>
      {customization.logo_base64 && (
        <img src={`data:image/png;base64,${customization.logo_base64}`} alt="Logo" style={{ height: '30px', marginRight: '1rem' }} />
      )}
      <span style={{ fontWeight: 'bold', marginRight: '2rem' }}>{customization.app_title}</span>

      <Link to="/" style={{ marginRight: '1rem' }}>Dashboard</Link>
      <Link to="/scans" style={{ marginRight: '1rem' }}>Scans</Link>
      {isAdmin && (
        <Link to="/settings/scanners" style={{ marginRight: '1rem' }}>Settings</Link>
      )}
      {isAdmin && (
        <Link to="/settings/customization" style={{ marginRight: '1rem' }}>Customization</Link>
      )}
      {isAdmin && (
        <Link to="/playbooks" style={{ marginRight: '1rem' }}>Playbooks</Link>
      )}

      <div style={{ marginLeft: 'auto' }}>
        <Link to="/account/security" style={{ marginRight: '1rem' }}>
          {user?.email}
        </Link>
        <button onClick={handleLogout} style={{ marginLeft: '1rem' }}>Logout</button>
      </div>
    </nav>
  );
};

export default Navbar;
