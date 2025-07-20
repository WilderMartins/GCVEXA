import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import useFetchData from '../hooks/useFetchData';

const ScansPage = () => {
  const { data: scans, loading, error, refetch } = useFetchData('/scans/');
  const [showNewScanForm, setShowNewScanForm] = useState(false);

  if (loading) return <p>Loading scans...</p>;
  if (error) return <p style={{ color: 'red' }}>Failed to load scans.</p>;

  return (
    <div>
      <h1>Scans</h1>
      <button onClick={() => setShowNewScanForm(!showNewScanForm)}>
        {showNewScanForm ? 'Cancel' : 'New Scan'}
      </button>

      {showNewScanForm && <NewScanForm onSuccess={refetch} />}

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Asset</th>
            <th>Status</th>
            <th>Started At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {scans && scans.map(scan => (
            <tr key={scan.id}>
              <td>{scan.id}</td>
              <td>{scan.asset.name}</td>
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

// O componente NewScanForm permanece o mesmo.
const NewScanForm = ({ onSuccess }) => {
  const [assetId, setAssetId] = useState('');
  const [configId, setConfigId] = useState('');
  const { data: configs, loading: loadingConfigs } = useFetchData('/scanners/configs/');
  const { data: assets, loading: loadingAssets } = useFetchData('/assets/');
  const [filteredAssets, setFilteredAssets] = useState([]);

  useEffect(() => {
    if (configs && configs.length > 0 && assets) {
      if (!configId) {
        const firstConfig = configs[0];
        setConfigId(firstConfig.id);
        updateFilteredAssets(firstConfig.type, assets);
      } else {
        const currentConfig = configs.find(c => c.id === parseInt(configId));
        if (currentConfig) {
          updateFilteredAssets(currentConfig.type, assets);
        }
      }
    }
  }, [configs, assets, configId]);

  const updateFilteredAssets = (configType, allAssets) => {
    let compatibleTypes = [];
    if (configType === 'openvas' || configType === 'zap') {
      compatibleTypes = ['host', 'application'];
    } else if (configType === 'semgrep' || configType === 'sonarqube') {
      compatibleTypes = ['repository'];
    }
    const filtered = allAssets.filter(asset => compatibleTypes.includes(asset.type));
    setFilteredAssets(filtered);
    if (filtered.length > 0 && !filtered.some(a => a.id === parseInt(assetId))) {
      setAssetId(filtered[0].id);
    } else if (filtered.length === 0) {
      setAssetId('');
    }
  };

  const handleConfigChange = (e) => {
    setConfigId(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/scans/', { asset_id: parseInt(assetId), config_id: parseInt(configId) });
      alert('Scan started successfully!');
      onSuccess();
    } catch (error) {
      alert(`Failed to start scan: ${error.response?.data?.detail}`);
    }
  };

  if (loadingConfigs || loadingAssets) return <p>Loading form...</p>;

  return (
    <form onSubmit={handleSubmit} style={{ margin: '1rem 0', padding: '1rem', border: '1px solid #ccc' }}>
      <h3>Start a New Scan</h3>
      <div>
        <label>Scanner Configuration</label>
        <select value={configId} onChange={handleConfigChange} required>
          <option value="" disabled>Select a configuration</option>
          {configs && configs.map(c => <option key={c.id} value={c.id}>{c.name} ({c.type})</option>)}
        </select>
      </div>
      <div>
        <label>Asset to Scan</label>
        <select value={assetId} onChange={e => setAssetId(e.target.value)} required>
          <option value="" disabled>Select an asset</option>
          {filteredAssets.length > 0 ? (
            filteredAssets.map(a => <option key={a.id} value={a.id}>{a.name} ({a.address})</option>)
          ) : (
            <option disabled>No compatible assets for this scanner type</option>
          )}
        </select>
      </div>
      <button type="submit" disabled={!assetId}>Start Scan</button>
    </form>
  );
};

export default ScansPage;
