import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const SetupWizardPage = () => {
  const navigate = useNavigate();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await api.post('/setup/initialize', {
        full_name: fullName,
        email: email,
        password: password,
      });
      alert(response.data.msg);
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during setup.');
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '5rem auto', padding: '2rem', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h1>Welcome to GCV!</h1>
      <p>Let's set up your administrator account.</p>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Full Name</label>
          <input type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} required />
        </div>
        <div>
          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit" style={{ width: '100%', marginTop: '1rem' }}>Create Admin Account</button>
      </form>
    </div>
  );
};

export default SetupWizardPage;
