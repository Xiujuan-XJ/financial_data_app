import { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  CircularProgress,
  FormControl,
  FormHelperText,
  Input,
} from '@mui/material';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useSnackbar } from 'notistack';

const Upload = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { enqueueSnackbar } = useSnackbar();
  const API_URL = 'http://127.0.0.1:8000/upload';
  
  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile && selectedFile.type === 'text/csv') {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please select a valid CSV file');
    }
  };

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!file) {
      setError('No file selected');
      enqueueSnackbar('No file selected', { variant: 'error' });
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(API_URL, formData, {
        headers: {
          "Access-Control-Allow-Origin": '*' ,
          'Content-Type': 'multipart/form-data',
        },
      });
      enqueueSnackbar('File uploaded successfully', { variant: 'success' });
      console.log('File uploaded successfully', response.data);
    } catch (error) {
      setError('Error uploading file');
      enqueueSnackbar('Error uploading file', { variant: 'error' });
      console.error('Error uploading file', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        padding: '2rem',
      }}
    >
      <Typography
        variant="h4"
        component="h4"
        sx={{
          marginBottom: '2rem',
        }}
      >
        Upload CSV File
      </Typography>
      <FormControl
        error={Boolean(error)}
        sx={{
          display: 'flex',
          alignItems: 'center',
          width: '100%',
          maxWidth: '500px',
          marginBottom: '1rem',
        }}
      >
        <Box
          component="label"
          sx={{
            display: 'flex',
            alignItems: 'center',
            width: '100%',
          }}
        >
          <Button
            component="span"
            variant="outlined"
            sx={{ marginRight: '1rem' }}
          >
            Choose File
          </Button>
          <Input
            type="file"
            onChange={handleFileChange}
            sx={{
              display: 'none',
            }}
            inputProps={{ accept: '.csv' }}
          />
          <Typography
            variant="body2"
            sx={{
              flexGrow: 1,
            }}
          >
            {file ? file.name : 'No file chosen'}
          </Typography>
        </Box>
      </FormControl>
      {error && <FormHelperText error>{error}</FormHelperText>}
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          gap: '1rem',
          marginTop: '2rem',
        }}
      >
        <Button
          onClick={handleUpload}
          variant="contained"
          color="primary"
          disabled={loading}
          startIcon={loading ? <CircularProgress size={20} /> : null}
        >
          {loading ? 'Uploading...' : 'Upload'}
        </Button>
        <Button
          component={Link}
          to="/view"
          variant="contained"
        >
          View Summary
        </Button>
      </Box>
    </Box>
  );
};

export default Upload;
