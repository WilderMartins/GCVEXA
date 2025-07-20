import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const AssetDetailPage = () => {
  const { assetId } = useParams();
  const [asset, setAsset] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAssetData = async () => {
      try {
        setLoading(true);
        const [assetRes, statsRes] = await Promise.all([
          api.get(`/assets/${assetId}`), // Precisaremos de um endpoint para buscar um único ativo
          api.get(`/assets/${assetId}/dashboard`)
        ]);
        setAsset(assetRes.data);
        setStats(statsRes.data);
      } catch (error) {
        console.error("Failed to fetch asset data", error);
      } finally {
        setLoading(false);
      }
    };
    fetchAssetData();
  }, [assetId]);

  if (loading) return <div>Loading asset details...</div>;
  if (!asset || !stats) return <div>Asset not found or no data available.</div>;

  const chartData = Object.entries(stats.vulnerability_counts_by_severity).map(([name, value]) => ({ name, count: value }));

  return (
    <div>
      <h1>{asset.name}</h1>
      <p><strong>Type:</strong> {asset.type}</p>
      <p><strong>Address:</strong> {asset.address}</p>

      <hr />

      <h2>Security Dashboard</h2>
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

      {/* A lista de ocorrências de vulnerabilidade viria aqui */}
    </div>
  );
};

export default AssetDetailPage;
