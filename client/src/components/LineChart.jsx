import PropTypes from 'prop-types';
import { Line } from 'react-chartjs-2';
import { Box, Typography } from '@mui/material';
import { Chart, registerables } from 'chart.js';
import { hexToRgbA, getRandomColor } from '../utils/colorManipulators';

// Register the necessary components with Chart.js
Chart.register(...registerables);

const LineChart = ({ summary, title }) => {
  const categories = Object.values(summary.category);
  const amounts = Object.values(summary.amount);

  const borderColor = getRandomColor();
  const backgroundColor = hexToRgbA(borderColor, 0.2);

  const data = {
    labels: categories,
    datasets: [
      {
        label: 'Amount',
        data: amounts,
        backgroundColor,
        borderColor,
        borderWidth: 2,
        fill: true,
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 800, margin: '0 auto', padding: '2rem' }}>
      {title && (
        <Typography variant="h6" align="center" gutterBottom>
          {title}
        </Typography>
      )}
      <Line data={data} options={options} />
    </Box>
  );
};

LineChart.propTypes = {
  summary: PropTypes.shape({
    amount: PropTypes.objectOf(PropTypes.number).isRequired,
    category: PropTypes.objectOf(PropTypes.string).isRequired,
  }).isRequired,
  title: PropTypes.string,
};

export default LineChart;
