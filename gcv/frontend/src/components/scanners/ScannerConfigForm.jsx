import React, { useState } from 'react';

const ScannerConfigForm = ({ onSubmit, onTestConnection, initialData = {} }) => {
  const [name, setName] = useState(initialData.name || '');
  const [url, setUrl] = useState(initialData.url || '');
  const [username, setUsername] = useState(initialData.username || '');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ name, url, username, password });
  };

  const handleTest = () => {
    onTestConnection({ name, url, username, password });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name</label>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
      </div>
      <div>
        <label>URL (e.g., tls://localhost)</label>
        <input type="text" value={url} onChange={(e) => setUrl(e.target.value)} required />
      </div>
      <div>
        <label>Username</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
      </div>
      <div>
        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Leave blank to keep unchanged" />
      </div>
      <button type="submit">Save</button>
      <button type="button" onClick={handleTest}>Test Connection</button>
    </form>
  );
};

export default ScannerConfigForm;
