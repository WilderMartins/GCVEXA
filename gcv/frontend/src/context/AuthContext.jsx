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

  const login = async (credentials) => {
    const { data } = await api.post('/login/access-token', new URLSearchParams(credentials));
    localStorage.setItem('token', data.access_token);
    setToken(data.access_token);
    api.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`;
    // setUser( ... ); // Idealmente, a resposta do login retornaria os dados do usuário
  };

  const signup = async (userData) => {
    await api.post('/users/', userData);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    delete api.defaults.headers.common['Authorization'];
    setUser(null);
  };

  const authContextValue = {
    user,
    token,
    login,
    signup,
    logout,
    isAuthenticated: !!token,
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
