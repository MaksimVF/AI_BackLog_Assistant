



import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, CircularProgress } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function Dashboard() {
  const [systemMetrics, setSystemMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch('/api/admin/metrics');
        const data = await response.json();
        setSystemMetrics(data);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch metrics:', error);
        setLoading(false);
      }
    };

    fetchMetrics();
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <CircularProgress />
      </div>
    );
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          Admin Dashboard
        </Typography>
      </Grid>

      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            System Health
          </Typography>
          {systemMetrics ? (
            <div>
              <div>CPU Usage: {systemMetrics.cpu_usage.toFixed(1)}%</div>
              <div>Memory Usage: {systemMetrics.memory_usage.toFixed(1)}%</div>
              <div>Disk Usage: {systemMetrics.disk_usage.toFixed(1)}%</div>
              <div>Status: {systemMetrics.status}</div>
            </div>
          ) : (
            <div>No system metrics available</div>
          )}
        </Paper>
      </Grid>

      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            System Metrics (Last 24h)
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart
              data={systemMetrics?.history || []}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="cpu_usage" name="CPU Usage (%)" stroke="#8884d8" />
              <Line type="monotone" dataKey="memory_usage" name="Memory Usage (%)" stroke="#82ca9d" />
            </LineChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>
    </Grid>
  );
}

export default Dashboard;



