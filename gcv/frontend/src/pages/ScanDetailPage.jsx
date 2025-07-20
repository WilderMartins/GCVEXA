import React, { useState, useEffect } from 'react';

import { useParams } from 'react-router-dom';
import api from '../services/api';

const VulnerabilityRow = ({ vuln, onStatusChange, playbooks }) => {
  const [summary, setSummary] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentStatus, setCurrentStatus] = useState(vuln.status);
  const [showPlaybookMenu, setShowPlaybookMenu] = useState(false);


  const handleSummarize = async () => {
    setIsLoading(true);
    try {

      const response = await api.post(`/vulnerabilities/${vuln.id}/summarize`);

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

      const response = await api.post(`/vulnerabilities/${vuln.id}/status`, { status: newStatus });
      setCurrentStatus(response.data.status);
      onStatusChange(vuln.id, response.data);

      alert('Status updated!');
    } catch (error) {
      alert('Failed to update status.');
    }
  };

  const handleRunPlaybook = async (playbookId) => {
    if (!playbookId) return;
    try {

      const response = await api.post(`/playbooks/run/${vuln.id}/${playbookId}`);
      alert(response.data.msg);
      setShowPlaybookMenu(false);

    } catch (error) {
      alert(`Failed to run playbook: ${error.response?.data?.detail}`);
    }
  };

  return (
    <>
      <tr>

        <td>{vuln.name}</td>
        <td>{vuln.severity}</td>
        <td>{vuln.cvss_score}</td>
        <td>
          <select value={currentStatus} onChange={handleStatusChange}>
            <option value="open">Open</option>
            <option value="remediated">Remediated</option>
            <option value="false_positive">False Positive</option>
          </select>
        </td>
        <td>
          <button onClick={handleSummarize} disabled={isLoading} style={{ marginRight: '10px' }}>
            {isLoading ? 'Loading...' : 'Summarize with AI'}
          </button>
          <button onClick={() => setShowPlaybookMenu(!showPlaybookMenu)}>
            Run Playbook
          </button>
          {showPlaybookMenu && (
            <select
              onChange={(e) => handleRunPlaybook(e.target.value)}
              defaultValue=""
            >
              <option value="" disabled>Select a playbook</option>
              {playbooks.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
          )}
        </td>
      </tr>
      {summary && (
        <tr>
          <td colSpan="5" style={{ padding: '1rem', background: '#f8f9fa' }}>
            <strong>AI Summary:</strong>
            <div style={{ whiteSpace: 'pre-wrap' }}>{summary}</div>
          </td>
        </tr>
      )}
    </>
  );
};


const ScanDetailPage = () => {
  const { scanId } = useParams();
  const [scan, setScan] = useState(null);

  const [vulnerabilities, setVulnerabilities] = useState([]);
  const [playbooks, setPlaybooks] = useState([]);

  useEffect(() => {
    // Mock data
    setScan({ id: scanId, target_host: '192.168.1.1', status: 'Done', started_at: new Date().toISOString() });
    setVulnerabilities([
        { id: 1, name: 'SSL Certificate Cannot Be Trusted', severity: 'High', cvss_score: 7.5, status: 'open' },
        { id: 2, name: 'TCP Timestamps', severity: 'Low', cvss_score: 2.1, status: 'open' },
    ]);
    fetchPlaybooks();
    // fetchScanDetails();
  }, [scanId]);

  const fetchPlaybooks = async () => {
    try {
      const response = await api.get('/playbooks/');
      setPlaybooks(response.data);
    } catch (error) {
      console.error("Failed to fetch playbooks", error);
    }
  };

  const fetchScanDetails = async () => {
    try {
      const response = await api.get(`/scans/${scanId}`);
      setScan(response.data);
      setVulnerabilities(response.data.vulnerabilities);
    } catch (error) {
      console.error('Failed to fetch scan details', error);
    }
  };

  const handleImportResults = async () => {
    try {
      const response = await api.post(`/scans/${scanId}/import`);
      alert(response.data.msg);
      fetchScanDetails();
    } catch (error) {
      alert(`Failed to import results: ${error.response?.data?.detail}`);
    }
  };

  const handleDownloadReport = async () => {
    try {
      const response = await api.get(`/scans/${scanId}/report`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `gcv_scan_report_${scanId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      alert(`Failed to download report: ${error.response?.data?.detail || 'Error'}`);
    }
  };

  const handleStatusChange = (vulnId, updatedVuln) => {
    setVulnerabilities(vulnerabilities.map(v => v.id === vulnId ? updatedVuln : v));
  };

  if (!scan) return <div>Loading...</div>;

  return (
    <div>
      <h1>Scan Details for {scan.target_host}</h1>
      <p><strong>Status:</strong> {scan.status}</p>
      <p><strong>Started:</strong> {new Date(scan.started_at).toLocaleString()}</p>
      <button onClick={handleImportResults} disabled={scan.status !== 'Running'}>
        Import Results
      </button>
      <button onClick={handleDownloadReport} disabled={scan.status !== 'Done'} style={{ marginLeft: '1rem' }}>
        Download PDF Report
      </button>

      <hr />

      <h2>Vulnerabilities</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Severity</th>
            <th>CVSS</th>
            <th>Status</th>
            <th>AI Actions</th>
          </tr>
        </thead>
        <tbody>
          {vulnerabilities.map(vuln => (
            <VulnerabilityRow key={vuln.id} vuln={vuln} onStatusChange={handleStatusChange} playbooks={playbooks} />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ScanDetailPage;
