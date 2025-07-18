import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // Aqui, você poderia adicionar uma chamada para validar o token no backend
      // e buscar os dados do usuário. Por enquanto, vamos assumir que o token é válido.
      // Ex: api.get('/users/me').then(response => setUser(response.data));
    }
    setLoading(false);
  }, [token]);

  const fetchUser = async () => {
    try {
      const { data } = await api.get('/users/me');
      setUser(data);
    } catch (error) {
      // Token inválido ou expirado, fazer logout
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    const response = await api.post('/login/access-token', new URLSearchParams(credentials));

    // Lidar com o fluxo MFA
    if (response.status === 202) {
      return response.data; // Retorna { mfa_required: true, temp_auth_token: ... }
    }

    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    setToken(access_token);
    api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
    await fetchUser();
    return null; // Indica que o login foi direto
  };

  useEffect(() => {
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const signup = async (userData) => {
    await api.post('/users/', userData);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    delete api.defaults.headers.common['Authorization'];
    setUser(null);
  };

  const setTokenAndFetchUser = async (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
    api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
    await fetchUser();
  };

  const authContextValue = {
    user,
    token,
    login,
    signup,
    logout,
    isAuthenticated: !!token,
    setTokenAndFetchUser,
  };

  return (
    <AuthContext.Provider value={authContextValue}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
