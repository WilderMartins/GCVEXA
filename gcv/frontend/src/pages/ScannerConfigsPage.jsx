import React, { useState } from 'react';
import ScannerConfigForm from '../components/scanners/ScannerConfigForm';
import api from '../services/api';

const ScannerConfigsPage = () => {
  // Mock data por enquanto
  const [configs, setConfigs] = useState([
    { id: 1, name: 'OpenVAS Local', url: 'tls://localhost', username: 'admin' },
  ]);
  const [editingConfig, setEditingConfig] = useState(null);

  const handleTestConnection = async (configData) => {
    try {
      const response = await api.post('/scanners/configs/test-connection', configData);
      alert(`Connection successful: ${response.data.msg}`);
    } catch (error) {
      alert(`Connection failed: ${error.response?.data?.detail || 'Unknown error'}`);
    }
  };

  const handleSaveConfig = async (configData) => {
    try {
      if (editingConfig) {
        // Lógica de update
        await api.put(`/scanners/configs/${editingConfig.id}`, configData);
        alert('Configuration updated!');
      } else {
        // Lógica de create
        await api.post('/scanners/configs/', configData);
        alert('Configuration created!');
      }
      // Resetar e recarregar a lista
      setEditingConfig(null);
      // fetchConfigs();
    } catch (error) {
      alert(`Failed to save: ${error.response?.data?.detail || 'Unknown error'}`);
    }
  };

  return (
    <div>
      <h1>Scanner Configurations</h1>
      <h2>Existing Configs</h2>
      <ul>
        {configs.map(config => (
          <li key={config.id}>
            {config.name} ({config.url})
            <button onClick={() => setEditingConfig(config)}>Edit</button>
          </li>
        ))}
      </ul>

      <hr />

      <h2>{editingConfig ? 'Edit Configuration' : 'New Configuration'}</h2>
      <ScannerConfigForm
        onSubmit={handleSaveConfig}
        onTestConnection={handleTestConnection}
        initialData={editingConfig}
      />
      {editingConfig && <button onClick={() => setEditingConfig(null)}>Cancel Edit</button>}
    </div>
  );
};

export default ScannerConfigsPage;
