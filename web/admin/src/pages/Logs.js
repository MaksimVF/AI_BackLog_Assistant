





import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, CircularProgress, TextField, Button, Grid } from '@mui/material';

function Logs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        // Mock log data for demonstration
        const mockLogs = [];
        for (let i = 0; i < 50; i++) {
          mockLogs.push({
            id: i + 1,
            timestamp: new Date(Date.now() - i * 60000).toISOString(),
            level: i % 5 === 0 ? 'ERROR' : i % 3 === 0 ? 'WARNING' : 'INFO',
            service: `service_${i % 5}`,
            message: `Log message ${i + 1} - This is a ${i % 5 === 0 ? 'critical error' : i % 3 === 0 ? 'warning' : 'informational'} message`
          });
        }
        setLogs(mockLogs);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch logs:', error);
        setLoading(false);
      }
    };

    fetchLogs();
  }, []);

  const filteredLogs = logs.filter(log =>
    log.level.toLowerCase().includes(filter.toLowerCase()) ||
    log.service.toLowerCase().includes(filter.toLowerCase()) ||
    log.message.toLowerCase().includes(filter.toLowerCase())
  );

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
        Log Management
      </Typography>

      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={12} md={6}>
          <TextField
            label="Filter logs"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            fullWidth
            placeholder="Filter by level, service, or message..."
          />
        </Grid>
        <Grid item xs={12} md={6} sx={{ display: 'flex', alignItems: 'center' }}>
          <Button variant="contained" color="primary">
            Refresh Logs
          </Button>
        </Grid>
      </Grid>

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
            {filteredLogs.length > 0 ? (
              filteredLogs.map((log) => (
                <TableRow key={log.id} sx={{ backgroundColor: log.level === 'ERROR' ? '#ffebee' : log.level === 'WARNING' ? '#fff3e0' : 'inherit' }}>
                  <TableCell>{new Date(log.timestamp).toLocaleString()}</TableCell>
                  <TableCell>{log.level}</TableCell>
                  <TableCell>{log.service}</TableCell>
                  <TableCell>{log.message}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={4} align="center">
                  No logs found matching your filter
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}

export default Logs;





