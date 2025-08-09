





import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, CircularProgress, Alert } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function SystemMonitoring() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch('/api/admin/monitoring');
        if (!response.ok) {
          throw new Error('Failed to fetch monitoring data');
        }
        const data = await response.json();
        setMetrics(data);
        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch monitoring data:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <CircularProgress />
      </div>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          System Monitoring
        </Typography>
      </Grid>

      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Current System Status
          </Typography>
          <div>CPU Usage: {metrics.cpu_usage.toFixed(1)}%</div>
          <div>Memory Usage: {metrics.memory_usage.toFixed(1)}%</div>
          <div>Disk Usage: {metrics.disk_usage.toFixed(1)}%</div>
          <div>Process Count: {metrics.process_count}</div>
          <div>Status: {metrics.status}</div>
        </Paper>
      </Grid>

      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Resource Utilization
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart
              data={metrics.history}
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
              <Line type="monotone" dataKey="disk_usage" name="Disk Usage (%)" stroke="#ffc658" />
            </LineChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>

      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            System Alerts
          </Typography>
          {metrics.alerts && metrics.alerts.length > 0 ? (
            <ul>
              {metrics.alerts.map((alert, index) => (
                <li key={index}>
                  <strong>{alert.level}:</strong> {alert.message} (Source: {alert.source})
                </li>
              ))}
            </ul>
          ) : (
            <div>No active alerts</div>
          )}
        </Paper>
      </Grid>
    </Grid>
  );
}

export default SystemMonitoring;





