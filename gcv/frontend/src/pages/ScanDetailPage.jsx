import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';

const ScanDetailPage = () => {
  const { scanId } = useParams();
  const [scan, setScan] = useState(null);
  const [vulnerabilities, setVulnerabilities] = useState([]);

  useEffect(() => {
    // Mock data
    setScan({ id: scanId, target_host: '192.168.1.1', status: 'Done', started_at: new Date().toISOString() });
    setVulnerabilities([
        { id: 1, name: 'SSL Certificate Cannot Be Trusted', severity: 'High', cvss_score: 7.5 },
        { id: 2, name: 'TCP Timestamps', severity: 'Low', cvss_score: 2.1 },
    ]);
    // fetchScanDetails();
  }, [scanId]);

  const fetchScanDetails = async () => {
    try {
      // No backend, precisaríamos de um endpoint GET /scans/{scan_id} que retorne o scan e suas vulnerabilidades
      // const response = await api.get(`/scans/${scanId}`);
      // setScan(response.data);
      // setVulnerabilities(response.data.vulnerabilities);
    } catch (error) {
      console.error('Failed to fetch scan details', error);
    }
  };

  const handleImportResults = async () => {
    try {
      const response = await api.post(`/scans/${scanId}/import`);
      alert(response.data.msg);
      fetchScanDetails(); // Recarregar os dados
    } catch (error) {
      alert(`Failed to import results: ${error.response?.data?.detail}`);
    }
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

      <hr />

      <h2>Vulnerabilities</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Severity</th>
            <th>CVSS</th>
          </tr>
        </thead>
        <tbody>
          {vulnerabilities.map(vuln => (
            <tr key={vuln.id}>
              <td>{vuln.name}</td>
              <td>{vuln.severity}</td>
              <td>{vuln.cvss_score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ScanDetailPage;
