import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LoginForm from '../components/auth/LoginForm';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

const MFALoginForm = ({ tempAuthToken, onSuccess }) => {
  const [otpCode, setOtpCode] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/login/mfa', {
        otp_code: otpCode,
        temp_auth_token: tempAuthToken,
      });
      onSuccess(response.data.access_token);
    } catch (error) {
      alert(`MFA Login Failed: ${error.response?.data?.detail || 'Please try again.'}`);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Enter Verification Code</h2>
      <p>Enter the code from your authenticator app.</p>
      <div>
        <label htmlFor="otpCode">6-Digit Code</label>
        <input
          type="text"
          id="otpCode"
          value={otpCode}
          onChange={(e) => setOtpCode(e.target.value)}
          required
        />
      </div>
      <button type="submit">Verify</button>
    </form>
  );
};


const LoginPage = () => {
  const { login, setTokenAndFetchUser } = useAuth();
  const navigate = useNavigate();
  const [mfaData, setMfaData] = useState(null);

  const handleLogin = async (credentials) => {
    try {
      const result = await login(credentials);
      if (result && result.mfa_required) {
        setMfaData(result);
      } else {
        navigate('/');
      }
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login Failed: ' + (error.response?.data?.detail || 'Please try again.'));
    }
  };

  const handleMfaSuccess = async (accessToken) => {
    await setTokenAndFetchUser(accessToken);
    navigate('/');
  };

  return (
    <div>
      <h1>Login</h1>
      {!mfaData ? (
        <LoginForm onSubmit={handleLogin} />
      ) : (
        <MFALoginForm
          tempAuthToken={mfaData.temp_auth_token}
          onSuccess={handleMfaSuccess}
        />
      )}
    </div>
  );
};

export default LoginPage;
