









import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, Alert } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

function Trends() {
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch trend analysis on component mount
  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/api/trends');
        setTrends(response.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchTrends();
  }, []);

  if (loading) return <Typography>Loading trend analysis...</Typography>;
  if (error) return <Typography color="error">Error: {error}</Typography>;

  // Prepare chart data from trends
  const prepareChartData = (trend) => {
    const forecast = trend.forecast.forecast || [];
    return forecast.map((item, index) => ({
      time: new Date(item.timestamp).toLocaleDateString(),
      actual: trend.trend.mean || 0,
      predicted: item.predicted,
      lower: item.lower,
      upper: item.upper
    }));
  };

  return (
    <Grid container spacing={3}>
      {trends.map((trend) => (
        <Grid item xs={12} md={6} key={trend.metric}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              {trend.metric} Trend Analysis
            </Typography>

            {/* Risk level */}
            <Alert severity={
              trend.risk_level === 'high' ? 'error' :
              trend.risk_level === 'medium' ? 'warning' : 'info'
            } sx={{ mb: 2 }}>
              Risk Level: {trend.risk_level}
            </Alert>

            {/* Recommendations */}
            {trend.recommendations.length > 0 && (
              <Paper sx={{ p: 2, mb: 2 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Recommendations:
                </Typography>
                <ul>
                  {trend.recommendations.map((rec, index) => (
                    <li key={index}>{rec}</li>
                  ))}
                </ul>
              </Paper>
            )}

            {/* Trend chart */}
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={prepareChartData(trend)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="actual" stroke="#8884d8" name="Actual" />
                <Line type="monotone" dataKey="predicted" stroke="#82ca9d" name="Predicted" />
                <Line type="monotone" dataKey="lower" stroke="#ff7300" strokeDasharray="5 5" name="Lower Bound" />
                <Line type="monotone" dataKey="upper" stroke="#ff7300" strokeDasharray="5 5" name="Upper Bound" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      ))}
    </Grid>
  );
}

export default Trends;











