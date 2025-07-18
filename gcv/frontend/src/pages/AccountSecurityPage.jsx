import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

const AccountSecurityPage = () => {
  const { user } = useAuth();
  const [setupInfo, setSetupInfo] = useState(null);
  const [otpCode, setOtpCode] = useState('');

  const handleEnableMFA = async () => {
    try {
      const response = await api.post('/mfa/setup');
      setSetupInfo(response.data);
    } catch (error) {
      alert('Failed to start MFA setup.');
    }
  };

  const handleVerifyMFA = async (e) => {
    e.preventDefault();
    try {
      await api.post('/mfa/verify', {
        otp_code: otpCode,
        temp_secret: setupInfo.otp_uri, // otp_uri contém o segredo temporário
      });
      alert('MFA enabled successfully! You will be asked for a code on your next login.');
      // Idealmente, o estado do usuário no AuthContext seria atualizado aqui
      window.location.reload(); // Recarregar para atualizar o estado do usuário
    } catch (error) {
      alert(`Failed to verify MFA: ${error.response?.data?.detail}`);
    }
  };

  return (
    <div>
      <h1>Account Security</h1>
      <p>
        <strong>Two-Factor Authentication (2FA):</strong>
        {user?.mfa_enabled ? ' Enabled' : ' Disabled'}
      </p>

      {!user?.mfa_enabled && !setupInfo && (
        <button onClick={handleEnableMFA}>Enable 2FA</button>
      )}

      {setupInfo && (
        <div>
          <h2>Set Up 2FA</h2>
          <p>1. Scan this QR code with your authenticator app (e.g., Google Authenticator).</p>
          <img src={`data:image/png;base64,${setupInfo.qr_code}`} alt="MFA QR Code" />
          <p>2. Enter the 6-digit code from your app to verify.</p>
          <form onSubmit={handleVerifyMFA}>
            <input
              type="text"
              value={otpCode}
              onChange={(e) => setOtpCode(e.target.value)}
              placeholder="6-digit code"
              required
            />
            <button type="submit">Verify & Enable</button>
          </form>
        </div>
      )}

      <hr style={{ margin: '2rem 0' }} />

      <div>
        <h2>Notification Preferences</h2>
        <p>You will receive email notifications when your scans are completed.</p>
        <p>(More detailed notification settings will be available in a future update.)</p>
      </div>
    </div>
  );
};

export default AccountSecurityPage;
