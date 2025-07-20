import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LoginCallbackPage = () => {
  const { setTokenAndFetchUser } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handleAuthCallback = async () => {
      const params = new URLSearchParams(location.search);
      const token = params.get('token');

      if (token) {
        await setTokenAndFetchUser(token);
        navigate('/');
      } else {
        // Lidar com erro ou redirecionar para o login
        navigate('/login');
      }
    };

    handleAuthCallback();
  }, [setTokenAndFetchUser, navigate, location]);

  return (
    <div>
      <p>Finalizing login...</p>
    </div>
  );
};

export default LoginCallbackPage;
