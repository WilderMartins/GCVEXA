import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const ScansPage = () => {
  const [scans, setScans] = useState([]);
  const [showNewScanForm, setShowNewScanForm] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchScans();
  }, []);

  const fetchScans = async () => {
    try {
      setLoading(true);
      const response = await api.get('/scans/');
      setScans(response.data);
    } catch (error) {
      console.error('Failed to fetch scans', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Scans</h1>
      <button onClick={() => setShowNewScanForm(!showNewScanForm)}>
        {showNewScanForm ? 'Cancel' : 'New Scan'}
      </button>

      {showNewScanForm && <NewScanForm onSuccess={fetchScans} />}

      {loading ? <p>Loading scans...</p> : (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Target</th>
              <th>Status</th>
              <th>Started At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {scans.map(scan => (
              <tr key={scan.id}>
                <td>{scan.id}</td>
                <td>{scan.target_host}</td>
                <td>{scan.status}</td>
                <td>{new Date(scan.started_at).toLocaleString()}</td>
                <td>
                  <Link to={`/scans/${scan.id}`}>View Details</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

// Componente do formulário de novo scan
const NewScanForm = ({ onSuccess }) => {
  const [targetHost, setTargetHost] = useState('');
  const [configId, setConfigId] = useState('');
  const [configs, setConfigs] = useState([]);
  const [selectedConfigType, setSelectedConfigType] = useState('');

  useEffect(() => {
    fetchScannerConfigs();
  }, []);

  const fetchScannerConfigs = async () => {
    try {
      const response = await api.get('/scanners/configs/');
      setConfigs(response.data);
      if (response.data.length > 0) {
        setConfigId(response.data[0].id);
        setSelectedConfigType(response.data[0].type);
      }
    } catch (error) {
      console.error("Failed to fetch scanner configs", error);
    }
  };

  const handleConfigChange = (e) => {
    const newConfigId = e.target.value;
    setConfigId(newConfigId);
    const selected = configs.find(c => c.id === parseInt(newConfigId));
    if (selected) {
      setSelectedConfigType(selected.type);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/scans/', { target_host: targetHost, config_id: parseInt(configId) });
      alert('Scan started successfully!');
      setTargetHost('');
      onSuccess();
    } catch (error) {
      alert(`Failed to start scan: ${error.response?.data?.detail}`);
    }
  };

  const getPlaceholder = () => {
    if (selectedConfigType === 'zap') {
      return 'e.g., https://example.com';
    }
    if (selectedConfigType === 'semgrep') {
      return 'e.g., https://github.com/user/repo.git';
    }
    return 'e.g., 192.168.1.1 or test.com';
  };

  return (
    <form onSubmit={handleSubmit} style={{ margin: '1rem 0', padding: '1rem', border: '1px solid #ccc' }}>
      <h3>Start a New Scan</h3>
      <div>
        <label>Scanner Configuration</label>
        <select value={configId} onChange={handleConfigChange} required>
          <option value="" disabled>Select a configuration</option>
          {configs.map(c => <option key={c.id} value={c.id}>{c.name} ({c.type})</option>)}
        </select>
      </div>
      <div>
        <label>Target</label>
        <input
          type="text"
          value={targetHost}
          onChange={e => setTargetHost(e.target.value)}
          placeholder={getPlaceholder()}
          required
        />
      </div>
      <button type="submit">Start Scan</button>
    </form>
  );
};

export default ScansPage;
