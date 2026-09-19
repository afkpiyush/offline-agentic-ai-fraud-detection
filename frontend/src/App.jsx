import React, { useState, useEffect } from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Box,
  Container,
  Typography,
  Paper,
  Chip,
  Grid,
  Button,
  CircularProgress,
} from '@mui/material';
import { Security, CheckCircle, ErrorOutline, Refresh } from '@mui/icons-material';
import axios from 'axios';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#38bdf8' },
    secondary: { main: '#818cf8' },
    background: { default: '#0f172a', paper: '#1e293b' },
  },
  typography: {
    fontFamily: 'Inter, Roboto, sans-serif',
  },
});

export default function App() {
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchHealth = async () => {
    setLoading(true);
    try {
      const res = await axios.get('/api/health');
      setHealthData(res.data);
    } catch (err) {
      if (err.response?.data) {
        setHealthData(err.response.data);
      } else {
        setHealthData({
          status: 'unhealthy',
          services: { backend: 'unreachable' },
        });
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, minHeight: '100vh', pb: 4 }}>
        <Paper
          elevation={0}
          sx={{
            p: 3,
            borderRadius: 0,
            borderBottom: '1px solid #334155',
            background: 'linear-gradient(90deg, #1e293b 0%, #0f172a 100%)',
          }}
        >
          <Container maxWidth="lg" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Security color="primary" sx={{ fontSize: 36 }} />
              <Box>
                <Typography variant="h5" fontWeight="700" color="white">
                  Offline Agentic AI Platform
                </Typography>
                <Typography variant="subtitle2" color="text.secondary">
                  Financial Fraud Detection & AML Investigation System (VIT TY-I20)
                </Typography>
              </Box>
            </Box>
            <Chip
              label="AIR-GAPPED / OFFLINE"
              color="success"
              variant="outlined"
              sx={{ fontWeight: 'bold' }}
            />
          </Container>
        </Paper>

        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Paper sx={{ p: 3, border: '1px solid #334155' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6" fontWeight="600">
                    Phase 0 — System Infrastructure Health
                  </Typography>
                  <Button
                    variant="outlined"
                    startIcon={loading ? <CircularProgress size={16} /> : <Refresh />}
                    onClick={fetchHealth}
                    disabled={loading}
                  >
                    Refresh Status
                  </Button>
                </Box>

                <Grid container spacing={2}>
                  {healthData?.services ? (
                    Object.entries(healthData.services).map(([service, state]) => (
                      <Grid item xs={12} sm={4} key={service}>
                        <Paper
                          sx={{
                            p: 2,
                            bgcolor: '#0f172a',
                            border: '1px solid #334155',
                            display: 'flex',
                            alignItems: 'center',
                            justify: 'space-between',
                          }}
                        >
                          <Typography variant="subtitle1" sx={{ textTransform: 'capitalize' }}>
                            {service}
                          </Typography>
                          <Chip
                            icon={state === 'connected' ? <CheckCircle /> : <ErrorOutline />}
                            label={state}
                            color={state === 'connected' ? 'success' : 'error'}
                            size="small"
                          />
                        </Paper>
                      </Grid>
                    ))
                  ) : (
                    <Grid item xs={12}>
                      <Typography color="text.secondary">
                        {loading ? 'Checking services...' : 'Unable to connect to backend service.'}
                      </Typography>
                    </Grid>
                  )}
                </Grid>
              </Paper>
            </Grid>
          </Grid>
        </Container>
      </Box>
    </ThemeProvider>
  );
}
