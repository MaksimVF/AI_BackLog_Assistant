









import React, { useState } from 'react';
import { Grid, Paper, Typography, TextField, Button, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import axios from 'axios';

function Settings() {
  const [config, setConfig] = useState({
    logLevel: 'INFO',
    alertThreshold: 80,
    autoRecovery: true
  });

  const [newConfig, setNewConfig] = useState({
    parameter: '',
    value: ''
  });

  // Handle config update
  const handleConfigUpdate = async () => {
    try {
      const response = await axios.post('/api/config', newConfig);
      alert(`Configuration updated: ${response.data.message}`);
      // Update local config state
      setConfig({ ...config, [newConfig.parameter]: newConfig.value });
    } catch (err) {
      alert(`Failed to update configuration: ${err.message}`);
    }
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            System Configuration
          </Typography>

          {/* Current configuration */}
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                label="Log Level"
                value={config.logLevel}
                onChange={(e) => setConfig({ ...config, logLevel: e.target.value })}
                fullWidth
                margin="normal"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Alert Threshold (%)"
                type="number"
                value={config.alertThreshold}
                onChange={(e) => setConfig({ ...config, alertThreshold: e.target.value })}
                fullWidth
                margin="normal"
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth margin="normal">
                <InputLabel>Auto Recovery</InputLabel>
                <Select
                  value={config.autoRecovery}
                  onChange={(e) => setConfig({ ...config, autoRecovery: e.target.value })}
                  label="Auto Recovery"
                >
                  <MenuItem value={true}>Enabled</MenuItem>
                  <MenuItem value={false}>Disabled</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>

          <Button
            variant="contained"
            color="primary"
            sx={{ mt: 2 }}
            onClick={() => alert('Configuration saved locally')}
          >
            Save Configuration
          </Button>
        </Paper>
      </Grid>

      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Update Configuration
          </Typography>

          {/* Update configuration form */}
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                label="Parameter Name"
                value={newConfig.parameter}
                onChange={(e) => setNewConfig({ ...newConfig, parameter: e.target.value })}
                fullWidth
                margin="normal"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Parameter Value"
                value={newConfig.value}
                onChange={(e) => setNewConfig({ ...newConfig, value: e.target.value })}
                fullWidth
                margin="normal"
              />
            </Grid>
          </Grid>

          <Button
            variant="contained"
            color="primary"
            sx={{ mt: 2 }}
            onClick={handleConfigUpdate}
          >
            Update Configuration
          </Button>
        </Paper>
      </Grid>
    </Grid>
  );
}

export default Settings;











