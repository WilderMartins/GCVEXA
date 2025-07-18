import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const DashboardPage = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      const response = await api.get('/dashboard/stats');
      setStats(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch dashboard stats.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading dashboard...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!stats) return <div>No data available.</div>;

  const chartData = Object.entries(stats.vulnerability_counts_by_severity).map(([name, value]) => ({
    name,
    count: value,
  }));

  return (
    <div>
      <h1>Dashboard</h1>

      <div style={{ marginBottom: '2rem' }}>
        <h2>Vulnerabilities by Severity</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>

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
            {stats.last_five_scans.map(scan => (
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
