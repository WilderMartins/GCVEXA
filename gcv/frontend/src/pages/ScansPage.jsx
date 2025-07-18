import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const ScansPage = () => {
  const [scans, setScans] = useState([]);
  const [showNewScanForm, setShowNewScanForm] = useState(false);

  useEffect(() => {
    // Mock data
    setScans([
      { id: 1, target_host: '192.168.1.1', status: 'Done', started_at: new Date().toISOString() },
      { id: 2, target_host: 'test.com', status: 'Running', started_at: new Date().toISOString() },
    ]);
    // fetchScans();
  }, []);

  const fetchScans = async () => {
    try {
      const response = await api.get('/scans/');
      setScans(response.data);
    } catch (error) {
      console.error('Failed to fetch scans', error);
    }
  };

  return (
    <div>
      <h1>Scans</h1>
      <button onClick={() => setShowNewScanForm(!showNewScanForm)}>
        {showNewScanForm ? 'Cancel' : 'New Scan'}
      </button>

      {showNewScanForm && <NewScanForm onSuccess={fetchScans} />}

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
    </div>
  );
};

// Componente do formulário de novo scan
const NewScanForm = ({ onSuccess }) => {
  const [targetHost, setTargetHost] = useState('');
  const [configId, setConfigId] = useState('');
  const [configs, setConfigs] = useState([]);

  useEffect(() => {
    // Mock data
    setConfigs([{ id: 1, name: 'OpenVAS Local' }]);
    // fetchScannerConfigs();
  }, []);

  const fetchScannerConfigs = async () => {
    const response = await api.get('/scanners/configs/');
    setConfigs(response.data);
    if (response.data.length > 0) {
      setConfigId(response.data[0].id);
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

  return (
    <form onSubmit={handleSubmit}>
      <h3>Start a New Scan</h3>
      <div>
        <label>Target Host (IP or URL)</label>
        <input type="text" value={targetHost} onChange={e => setTargetHost(e.target.value)} required />
      </div>
      <div>
        <label>Scanner Configuration</label>
        <select value={configId} onChange={e => setConfigId(e.target.value)} required>
          <option value="" disabled>Select a configuration</option>
          {configs.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </div>
      <button type="submit">Start Scan</button>
    </form>
  );
};

export default ScansPage;
