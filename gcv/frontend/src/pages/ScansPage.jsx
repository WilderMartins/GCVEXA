import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const ScansPage = () => {
  // ... (código existente da ScansPage) ...
};

// Formulário de novo scan refatorado
const NewScanForm = ({ onSuccess }) => {
  const [assetId, setAssetId] = useState('');
  const [configId, setConfigId] = useState('');
  const [configs, setConfigs] = useState([]);
  const [assets, setAssets] = useState([]);
  const [filteredAssets, setFilteredAssets] = useState([]);
  const [selectedConfigType, setSelectedConfigType] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [configsRes, assetsRes] = await Promise.all([
          api.get('/scanners/configs/'),
          api.get('/assets/')
        ]);
        setConfigs(configsRes.data);
        setAssets(assetsRes.data);
        if (configsRes.data.length > 0) {
          const firstConfig = configsRes.data[0];
          setConfigId(firstConfig.id);
          updateFilteredAssets(firstConfig.type, assetsRes.data);
        }
      } catch (error) {
        console.error("Failed to fetch data for new scan form", error);
      }
    };
    fetchData();
  }, []);

  const updateFilteredAssets = (configType, allAssets) => {
    let compatibleTypes = [];
    if (configType === 'openvas' || configType === 'zap') {
      compatibleTypes = ['host', 'application'];
    } else if (configType === 'semgrep' || configType === 'sonarqube') {
      compatibleTypes = ['repository'];
    }
    const filtered = allAssets.filter(asset => compatibleTypes.includes(asset.type));
    setFilteredAssets(filtered);
    setSelectedConfigType(configType);
    if (filtered.length > 0) {
      setAssetId(filtered[0].id);
    } else {
      setAssetId('');
    }
  };

  const handleConfigChange = (e) => {
    const newConfigId = e.target.value;
    setConfigId(newConfigId);
    const selected = configs.find(c => c.id === parseInt(newConfigId));
    if (selected) {
      updateFilteredAssets(selected.type, assets);
    }
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


  const getPlaceholder = () => {
    if (selectedConfigType === 'zap') {
      return 'e.g., https://example.com';
    }
    if (selectedConfigType === 'semgrep' || selectedConfigType === 'sonarqube') {
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

// A ScansPage precisa ser mantida, apenas o NewScanForm é totalmente substituído.
// Vou colar o corpo da ScansPage aqui para garantir.

const FullScansPage = () => {
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
                <th>Asset</th>
                <th>Status</th>
                <th>Started At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {scans.map(scan => (
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
        )}
      </div>
    );
};

export default FullScansPage;
