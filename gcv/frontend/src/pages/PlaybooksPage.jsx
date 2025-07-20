import React, { useState, useEffect } from 'react';
import api from '../services/api';

const PlaybooksPage = () => {
  const [playbooks, setPlaybooks] = useState([]);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchPlaybooks();
  }, []);

  const fetchPlaybooks = async () => {
    try {
      const response = await api.get('/playbooks/');
      setPlaybooks(response.data);
    } catch (error) {
      console.error('Failed to fetch playbooks', error);
    }
  };

  const handleCreate = async (playbookData) => {
    try {
      await api.post('/playbooks/', playbookData);
      alert('Playbook created successfully!');
      setShowForm(false);
      fetchPlaybooks();
    } catch (error) {
      alert(`Failed to create playbook: ${error.response?.data?.detail}`);
    }
  };

  return (
    <div>
      <h1>Playbooks</h1>
      <button onClick={() => setShowForm(!showForm)}>
        {showForm ? 'Cancel' : 'New Playbook'}
      </button>

      {showForm && <NewPlaybookForm onSubmit={handleCreate} />}

      <h2>Existing Playbooks</h2>
      <ul>
        {playbooks.map(p => (
          <li key={p.id}>{p.name} - {p.description}</li>
        ))}
      </ul>
    </div>
  );
};

// Formulário para criar um novo playbook (simplificado)
const NewPlaybookForm = ({ onSubmit }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [webhookUrl, setWebhookUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const playbookData = {
      name,
      description,
      steps: [
        {
          step_number: 1,
          action_type: 'webhook',
          action_config: {
            config: JSON.stringify({ url: webhookUrl })
          }
        }
      ]
    };
    onSubmit(playbookData);
  };

  return (
    <form onSubmit={handleSubmit} style={{ margin: '1rem 0', padding: '1rem', border: '1px solid #ccc' }}>
      <h3>New Webhook Playbook</h3>
      <div>
        <label>Playbook Name</label>
        <input type="text" value={name} onChange={e => setName(e.target.value)} required />
      </div>
      <div>
        <label>Description</label>
        <input type="text" value={description} onChange={e => setDescription(e.target.value)} />
      </div>
      <div>
        <label>Webhook URL</label>
        <input type="url" value={webhookUrl} onChange={e => setWebhookUrl(e.target.value)} required placeholder="https://hooks.slack.com/..." />
      </div>
      <button type="submit">Create Playbook</button>
    </form>
  );
};

export default PlaybooksPage;
