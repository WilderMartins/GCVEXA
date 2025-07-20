import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import HeatMap from 'react-heatmap-grid';

// Componente para os cartões de métricas
const StatCard = ({ title, value, unit = '' }) => (
  <div style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '8px', textAlign: 'center' }}>
    <h3 style={{ margin: 0 }}>{title}</h3>
    <p style={{ fontSize: '2rem', margin: '0.5rem 0' }}>{value}{unit}</p>
  </div>
);

const DashboardPage = () => {
  const [basicStats, setBasicStats] = useState(null);
  const [advancedStats, setAdvancedStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAllStats = async () => {
      try {
        setLoading(true);
        const [basicRes, advancedRes] = await Promise.all([
          api.get('/dashboard/stats'),
          api.get('/dashboard/advanced-stats')
        ]);
        setBasicStats(basicRes.data);
        setAdvancedStats(advancedRes.data);
        setError('');
      } catch (err) {
        setError('Failed to fetch dashboard stats.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAllStats();
  }, []);

  if (loading) return <div>Loading dashboard...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!basicStats || !advancedStats) return <div>No data available.</div>;

  const severityChartData = Object.entries(basicStats.vulnerability_counts_by_severity).map(([name, value]) => ({ name, count: value }));

  // Dados para o Heatmap
  const heatmapLabels = [...new Set(advancedStats.heatmap_data.map(d => d.severity))];
  const heatmapData = advancedStats.heatmap_data.reduce((acc, { host, severity, count }) => {
    if (!acc[host]) acc[host] = Array(heatmapLabels.length).fill(0);
    acc[host][heatmapLabels.indexOf(severity)] = count;
    return acc;
  }, {});
  const heatmapXLabels = Object.keys(heatmapData);
  const heatmapYLabels = heatmapLabels;
  const heatmapGridData = Object.values(heatmapData);


  return (
    <div>
      <h1>Executive Dashboard</h1>

      {/* Scorecards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
        <StatCard title="Remediation Rate" value={advancedStats.remediation_rate.toFixed(1)} unit="%" />
        <StatCard title="Mean Time to Remediate" value={advancedStats.mean_time_to_remediate.toFixed(1)} unit=" days" />
      </div>

      {/* Gráficos */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem' }}>
        <div>
          <h2>Vulnerabilities by Severity</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={severityChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div>
          <h2>Critical Vulnerabilities Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={advancedStats.critical_vulns_trend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="count" stroke="#ca2c2c" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Heatmap */}
      {heatmapGridData.length > 0 && (
        <div style={{ marginBottom: '2rem' }}>
          <h2>Vulnerability Heatmap (Top 10 Hosts)</h2>
          <HeatMap
            xLabels={heatmapXLabels}
            yLabels={heatmapYLabels}
            data={heatmapGridData}
            squares
            cellStyle={(background, value, min, max, data, x, y) => ({
              background: `rgba(66, 86, 244, ${1 - (max - value) / (max - min)})`,
              fontSize: '11px',
            })}
          />
        </div>
      )}

      {/* Tabela de Scans Recentes */}
      <div>
        <h2>Last 5 Scans</h2>
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
            {basicStats.last_five_scans.map(scan => (
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
    </div>
  );
};

export default DashboardPage;
