








import React, { useState, useEffect } from 'react';
import { Paper, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Button, Grid } from '@mui/material';
import axios from 'axios';

function Logs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('');

  // Fetch logs on component mount
  useEffect(() => {
    const fetchLogs = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/api/logs', { params: { limit: 50 } });
        setLogs(response.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchLogs();
  }, []);

  // Filter logs based on search term
  const filteredLogs = logs.filter(log =>
    log.message.toLowerCase().includes(filter.toLowerCase()) ||
    log.level.toLowerCase().includes(filter.toLowerCase())
  );

  if (loading) return <Typography>Loading logs...</Typography>;
  if (error) return <Typography color="error">Error: {error}</Typography>;

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            System Logs
          </Typography>

          {/* Filter controls */}
          <Grid container spacing={2} sx={{ mb: 2 }}>
            <Grid item xs={6}>
              <TextField
                label="Filter logs"
                variant="outlined"
                fullWidth
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
              />
            </Grid>
            <Grid item xs={3}>
              <Button variant="contained" color="primary" fullWidth>
                Refresh
              </Button>
            </Grid>
            <Grid item xs={3}>
              <Button variant="outlined" color="secondary" fullWidth>
                Clear
              </Button>
            </Grid>
          </Grid>

          {/* Logs table */}
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Timestamp</TableCell>
                  <TableCell>Level</TableCell>
                  <TableCell>Service</TableCell>
                  <TableCell>Message</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredLogs.map((log) => (
                  <TableRow key={log.timestamp}>
                    <TableCell>{new Date(log.timestamp).toLocaleString()}</TableCell>
                    <TableCell>{log.level}</TableCell>
                    <TableCell>{log.service}</TableCell>
                    <TableCell>{log.message}</TableCell>
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

export default Logs;









