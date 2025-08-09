






import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, CircularProgress, Button, Alert } from '@mui/material';

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        // Mock alert data for demonstration
        const mockAlerts = [];
        for (let i = 0; i < 10; i++) {
          mockAlerts.push({
            id: i + 1,
            timestamp: new Date(Date.now() - i * 3600000).toISOString(),
            level: i % 3 === 0 ? 'CRITICAL' : i % 2 === 0 ? 'WARNING' : 'INFO',
            message: `Alert ${i + 1} - ${i % 3 === 0 ? 'Critical system failure' : i % 2 === 0 ? 'High resource usage' : 'Informational alert'}`,
            source: `source_${i % 4}`,
            status: i % 4 === 0 ? 'resolved' : 'active'
          });
        }
        setAlerts(mockAlerts);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch alerts:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  const handleAcknowledge = async (alertId) => {
    try {
      // In a real implementation, this would call the API
      console.log(`Acknowledging alert ${alertId}`);

      // Update local state
      setAlerts(prev => prev.map(alert =>
        alert.id === alertId ? { ...alert, status: 'acknowledged' } : alert
      ));
      setSuccess(`Alert ${alertId} acknowledged successfully`);
      setError(null);
    } catch (err) {
      console.error('Failed to acknowledge alert:', err);
      setError(err.message);
      setSuccess(null);
    }
  };

  const handleResolve = async (alertId) => {
    try {
      // In a real implementation, this would call the API
      console.log(`Resolving alert ${alertId}`);

      // Update local state
      setAlerts(prev => prev.map(alert =>
        alert.id === alertId ? { ...alert, status: 'resolved' } : alert
      ));
      setSuccess(`Alert ${alertId} resolved successfully`);
      setError(null);
    } catch (err) {
      console.error('Failed to resolve alert:', err);
      setError(err.message);
      setSuccess(null);
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <CircularProgress />
      </div>
    );
  }

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Alert Management
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

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
            {alerts.length > 0 ? (
              alerts.map((alert) => (
                <TableRow key={alert.id} sx={{ backgroundColor: alert.level === 'CRITICAL' ? '#ffcdd2' : alert.level === 'WARNING' ? '#fff3e0' : 'inherit' }}>
                  <TableCell>{new Date(alert.timestamp).toLocaleString()}</TableCell>
                  <TableCell>{alert.level}</TableCell>
                  <TableCell>{alert.message}</TableCell>
                  <TableCell>{alert.source}</TableCell>
                  <TableCell>{alert.status}</TableCell>
                  <TableCell>
                    {alert.status === 'active' && (
                      <>
                        <Button
                          variant="outlined"
                          size="small"
                          color="primary"
                          onClick={() => handleAcknowledge(alert.id)}
                          sx={{ mr: 1 }}
                        >
                          Acknowledge
                        </Button>
                        <Button
                          variant="outlined"
                          size="small"
                          color="success"
                          onClick={() => handleResolve(alert.id)}
                        >
                          Resolve
                        </Button>
                      </>
                    )}
                    {alert.status === 'acknowledged' && (
                      <Button
                        variant="outlined"
                        size="small"
                        color="success"
                        onClick={() => handleResolve(alert.id)}
                      >
                        Resolve
                      </Button>
                    )}
                    {alert.status === 'resolved' && (
                      <Typography variant="body2" color="textSecondary">
                        Resolved
                      </Typography>
                    )}
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  No alerts found
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}

export default Alerts;






