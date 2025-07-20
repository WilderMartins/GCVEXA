import React from 'react';
import { useNavigate } from 'react-router-dom';
import SignUpForm from '../components/auth/SignUpForm';
import { useAuth } from '../context/AuthContext';

const SignUpPage = () => {
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSignUp = async (userData) => {
    try {
      await signup(userData);
      alert('Sign up successful! Please log in.');
      navigate('/login');
    } catch (error) {
      console.error('Sign up failed:', error);
      alert('Sign Up Failed: ' + (error.response?.data?.detail || 'Please try again.'));
    }
  };

  return (
    <div>
      <h1>Sign Up</h1>
      <SignUpForm onSubmit={handleSignUp} />
    </div>
  );
};

export default SignUpPage;
