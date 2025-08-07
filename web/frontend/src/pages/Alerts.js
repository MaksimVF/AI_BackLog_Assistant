









import React, { useState, useEffect } from 'react';
import { Paper, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button, Grid, Alert } from '@mui/material';
import axios from 'axios';

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch alerts on component mount
  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/api/alerts');
        setAlerts(response.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  // Handle alert action
  const handleAlertAction = (alertId, action) => {
    // In a real implementation, this would call an API to handle the alert
    console.log(`Handling alert ${alertId} with action ${action}`);
    alert(`Alert ${alertId} action: ${action}`);
  };

  if (loading) return <Typography>Loading alerts...</Typography>;
  if (error) return <Typography color="error">Error: {error}</Typography>;

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Active Alerts
          </Typography>

          {/* Alerts table */}
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Timestamp</TableCell>
                  <TableCell>Level</TableCell>
                  <TableCell>Message</TableCell>
                  <TableCell>Source</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {alerts.map((alert) => (
                  <TableRow key={alert.id}>
                    <TableCell>{new Date(alert.timestamp).toLocaleString()}</TableCell>
                    <TableCell>{alert.level}</TableCell>
                    <TableCell>{alert.message}</TableCell>
                    <TableCell>{alert.source}</TableCell>
                    <TableCell>{alert.status}</TableCell>
                    <TableCell>
                      <Button
                        variant="outlined"
                        size="small"
                        onClick={() => handleAlertAction(alert.id, 'acknowledge')}
                      >
                        Acknowledge
                      </Button>
                      <Button
                        variant="outlined"
                        size="small"
                        color="secondary"
                        onClick={() => handleAlertAction(alert.id, 'resolve')}
                        sx={{ ml: 1 }}
                      >
                        Resolve
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Grid>
    </Grid>
  );
}

export default Alerts;










