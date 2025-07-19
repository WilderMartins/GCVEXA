import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';

const VulnerabilityRow = ({ occurrence, onStatusChange, playbooks }) => {
  const [summary, setSummary] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentStatus, setCurrentStatus] = useState(occurrence.status);

  const handleSummarize = async () => {
    setIsLoading(true);
    try {
      const response = await api.post(`/vulnerabilities/occurrences/${occurrence.id}/summarize`);
      setSummary(response.data.msg);
    } catch (error) {
      setSummary(`Error: ${error.response?.data?.detail || 'Could not get summary.'}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStatusChange = async (e) => {
    const newStatus = e.target.value;
    try {
      const response = await api.post(`/vulnerabilities/occurrences/${occurrence.id}/status`, { status: newStatus });
      setCurrentStatus(response.data.status);
      onStatusChange(occurrence.id, response.data);
      alert('Status updated!');
    } catch (error) {
      alert('Failed to update status.');
    }
  };

  const handleRunPlaybook = async (playbookId) => {
    if (!playbookId) return;
    try {
      const response = await api.post(`/playbooks/run/${occurrence.id}/${playbookId}`);
      alert(response.data.msg);
    } catch (error) {
      alert(`Failed to run playbook: ${error.response?.data?.detail}`);
    }
  };

  return (
    <>
      <tr>
        <td>
          <Link to={`/vulnerabilities/definitions/${occurrence.definition.id}`}>{occurrence.definition.name}</Link>
        </td>
        <td>{occurrence.definition.severity}</td>
        <td>{currentStatus}</td>
        <td>
          <select onChange={(e) => handleRunPlaybook(e.target.value)} defaultValue="">
            <option value="" disabled>Run a playbook...</option>
            {playbooks.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
        </td>
        <td>
          <button onClick={handleSummarize} disabled={isLoading}>
            {isLoading ? 'Loading...' : 'AI Summary'}
          </button>
        </td>
        <td>
          <select value={currentStatus} onChange={handleStatusChange} style={{width: '150px'}}>
            <option value="open">Open</option>
            <option value="remediated">Remediated</option>
            <option value="false_positive">False Positive</option>
          </select>
        </td>
      </tr>
      {summary && (
        <tr>
          <td colSpan="6" style={{ padding: '1rem', background: '#f8f9fa', whiteSpace: 'pre-wrap' }}>
            <strong>AI Summary:</strong> {summary}
          </td>
        </tr>
      )}
    </>
  );
};


const ScanDetailPage = () => {
  const { scanId } = useParams();
  const [scan, setScan] = useState(null);
  const [playbooks, setPlaybooks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [scanRes, playbooksRes] = await Promise.all([
          api.get(`/scans/${scanId}`),
          api.get('/playbooks/')
        ]);
        setScan(scanRes.data);
        setPlaybooks(playbooksRes.data);
      } catch (error) {
        console.error("Failed to fetch page data", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [scanId]);

  const handleStatusChange = (occurrenceId, updatedOccurrence) => {
    const newVulnerabilities = scan.vulnerabilities.map(v => v.id === occurrenceId ? updatedOccurrence : v);
    setScan({ ...scan, vulnerabilities: newVulnerabilities });
  };

  if (loading) return <div>Loading scan details...</div>;
  if (!scan) return <div>Scan not found.</div>;

  return (
    <div>
      <h1>Scan Details for {scan.asset.name}</h1>
      <p><strong>Status:</strong> {scan.status}</p>
      <p><strong>Target:</strong> {scan.asset.address}</p>
      <p><strong>Started:</strong> {new Date(scan.started_at).toLocaleString()}</p>
      <hr />
      <h2>Vulnerabilities Found ({scan.vulnerabilities.length})</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Actions</th>
            <th>AI</th>
            <th>Set Status</th>
          </tr>
        </thead>
        <tbody>
          {scan.vulnerabilities.map(occ => (
            <VulnerabilityRow
              key={occ.id}
              occurrence={occ}
              onStatusChange={handleStatusChange}
              playbooks={playbooks}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ScanDetailPage;
