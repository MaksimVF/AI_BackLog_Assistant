








import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, Button, Alert } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

function Dashboard() {
  const [status, setStatus] = useState(null);
  const [logs, setLogs] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch all data on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // Fetch status
        const statusResponse = await axios.get('/api/status');
        setStatus(statusResponse.data);

        // Fetch logs
        const logsResponse = await axios.get('/api/logs', { params: { limit: 5 } });
        setLogs(logsResponse.data);

        // Fetch alerts
        const alertsResponse = await axios.get('/api/alerts');
        setAlerts(alertsResponse.data);

        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Handle self-healing action
  const handleSelfHealing = async (action) => {
    try {
      const response = await axios.post('/api/self-healing', { action });
      alert(`Self-healing action triggered: ${response.data.result}`);
    } catch (err) {
      alert(`Failed to trigger self-healing: ${err.message}`);
    }
  };

  if (loading) return <Typography>Loading...</Typography>;
  if (error) return <Alert severity="error">{error}</Alert>;

  // Prepare chart data
  const chartData = logs.map((log, index) => ({
    time: new Date(log.timestamp).toLocaleTimeString(),
    value: index * 10 + 20, // Mock data for chart
  }));

  return (
    <Grid container spacing={3}>
      {/* System Status */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            System Status
          </Typography>
          {status && (
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography>CPU Usage: {status.cpu_usage.toFixed(1)}%</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography>Memory Usage: {status.memory_usage.toFixed(1)}%</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography>Disk Usage: {status.disk_usage.toFixed(1)}%</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography>Processes: {status.process_count}</Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography>Status: {status.status}</Typography>
              </Grid>
            </Grid>
          )}
        </Paper>
      </Grid>

      {/* Self-Healing Actions */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Self-Healing Actions
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                onClick={() => handleSelfHealing('optimize_resources')}
              >
                Optimize Resources
              </Button>
            </Grid>
            <Grid item xs={6}>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                onClick={() => handleSelfHealing('restart_service')}
              >
                Restart Service
              </Button>
            </Grid>
            <Grid item xs={6}>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                onClick={() => handleSelfHealing('clear_cache')}
              >
                Clear Cache
              </Button>
            </Grid>
          </Grid>
        </Paper>
      </Grid>

      {/* Recent Logs */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Recent Logs
          </Typography>
          {logs.length > 0 ? (
            logs.map((log) => (
              <Paper key={log.timestamp} sx={{ p: 1, mb: 1 }}>
                <Typography variant="body2">
                  {new Date(log.timestamp).toLocaleString()} - {log.level}: {log.message}
                </Typography>
              </Paper>
            ))
          ) : (
            <Typography>No recent logs</Typography>
          )}
        </Paper>
      </Grid>

      {/* Active Alerts */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Active Alerts
          </Typography>
          {alerts.length > 0 ? (
            alerts.map((alert) => (
              <Alert key={alert.id} severity="warning" sx={{ mb: 1 }}>
                {alert.message}
              </Alert>
            ))
          ) : (
            <Typography>No active alerts</Typography>
          )}
        </Paper>
      </Grid>

      {/* Performance Chart */}
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Performance Metrics
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#8884d8" name="Performance" />
            </LineChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>
    </Grid>
  );
}

export default Dashboard;









