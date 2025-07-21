import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import useFetchData from '../hooks/useFetchData';

const AssetsPage = () => {
  const { data: assets, loading, error, refetch } = useFetchData('/assets/');
  const [showForm, setShowForm] = useState(false);

  const handleCreate = async (assetData) => {
    try {
      await api.post('/assets/', assetData);
      alert('Asset created successfully!');
      setShowForm(false);
      refetch();
    } catch (error) {
      alert(`Failed to create asset: ${error.response?.data?.detail}`);
    }
  };

  if (loading) return <p>Loading assets...</p>;
  if (error) return <p style={{color: 'red'}}>Failed to load assets.</p>;

  return (
    <div>
      <h1>My Assets</h1>
      <button onClick={() => setShowForm(!showForm)}>
        {showForm ? 'Cancel' : 'New Asset'}
      </button>

      {showForm && <NewAssetForm onSubmit={handleCreate} />}

      <h2>Existing Assets</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Address</th>
          </tr>
        </thead>
        <tbody>
          {assets && assets.map(asset => (
            <tr key={asset.id}>
              <td>
                <Link to={`/assets/${asset.id}`}>{asset.name}</Link>
              </td>
              <td>{asset.type}</td>
              <td>{asset.address}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// O componente NewAssetForm permanece o mesmo
const NewAssetForm = ({ onSubmit }) => {
  const [name, setName] = useState('');
  const [type, setType] = useState('host');
  const [address, setAddress] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ name, type, address });
  };

  return (
    <form onSubmit={handleSubmit} style={{ margin: '1rem 0', padding: '1rem', border: '1px solid #ccc' }}>
      <h3>New Asset</h3>
      <div>
        <label>Asset Name</label>
        <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder="e.g., Production API Server" required />
      </div>
      <div>
        <label>Asset Type</label>
        <select value={type} onChange={e => setType(e.target.value)}>
          <option value="host">Host</option>
          <option value="application">Application</option>
          <option value="repository">Repository</option>
        </select>
      </div>
      <div>
        <label>Address (IP, URL, Git URL)</label>
        <input type="text" value={address} onChange={e => setAddress(e.target.value)} required />
      </div>
      <button type="submit">Create Asset</button>
    </form>
  );
};


export default AssetsPage;
