





import React, { useState, useEffect } from 'react';
import { TextField, Button, Grid, Paper, Typography, CircularProgress, Alert } from '@mui/material';

function Configuration() {
  const [config, setConfig] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        // Mock configuration data for demonstration
        // In a real implementation, this would fetch from an API
        const mockConfig = {
          logLevel: 'INFO',
          maxRetries: 3,
          cacheTTL: 3600,
          rateLimit: 100
        };
        setConfig(mockConfig);
        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch configuration:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchConfig();
  }, []);

  const handleConfigUpdate = async (param, value) => {
    try {
      // In a real implementation, this would call the API
      console.log(`Updating ${param} to ${value}`);

      // Update local state
      setConfig(prev => ({ ...prev, [param]: value }));
      setSuccess(`Configuration ${param} updated successfully`);
      setError(null);
    } catch (err) {
      console.error('Failed to update configuration:', err);
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
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          System Configuration
        </Typography>
      </Grid>

      {error && (
        <Grid item xs={12}>
          <Alert severity="error">{error}</Alert>
        </Grid>
      )}

      {success && (
        <Grid item xs={12}>
          <Alert severity="success">{success}</Alert>
        </Grid>
      )}

      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            General Settings
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                label="Log Level"
                value={config.logLevel || ''}
                onChange={(e) => handleConfigUpdate('logLevel', e.target.value)}
                fullWidth
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Max Retries"
                type="number"
                value={config.maxRetries || 0}
                onChange={(e) => handleConfigUpdate('maxRetries', parseInt(e.target.value))}
                fullWidth
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Cache TTL (seconds)"
                type="number"
                value={config.cacheTTL || 0}
                onChange={(e) => handleConfigUpdate('cacheTTL', parseInt(e.target.value))}
                fullWidth
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Rate Limit (requests/min)"
                type="number"
                value={config.rateLimit || 0}
                onChange={(e) => handleConfigUpdate('rateLimit', parseInt(e.target.value))}
                fullWidth
              />
            </Grid>
          </Grid>
        </Paper>
      </Grid>

      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Advanced Settings
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                label="Database Connection String"
                value={config.dbConnection || ''}
                onChange={(e) => handleConfigUpdate('dbConnection', e.target.value)}
                fullWidth
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="API Timeout (ms)"
                type="number"
                value={config.apiTimeout || 0}
                onChange={(e) => handleConfigUpdate('apiTimeout', parseInt(e.target.value))}
                fullWidth
              />
            </Grid>
          </Grid>
        </Paper>
      </Grid>
    </Grid>
  );
}

export default Configuration;





