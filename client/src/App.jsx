import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Box, CssBaseline } from '@mui/material';
import Upload from './pages/Upload';
import ViewCharts from './pages/ViewCharts';

function App() {
  const [data, setData] = useState([]);
  
  return (
    <Box
      className="App"
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        width: '100vw',
        padding: '1rem',
        backgroundColor: 'FBFEF9',  // Ensures the background color is set globally
      }}
    >
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Upload data={data} setData={setData} />} />
          <Route path="/view" element={<ViewCharts data={data} />} />
        </Routes>
      </Router>
    </Box>
  );
}

export default App;
