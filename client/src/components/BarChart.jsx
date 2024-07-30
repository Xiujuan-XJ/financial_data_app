import PropTypes from 'prop-types';
import { Bar } from 'react-chartjs-2';
import { Box, Typography } from '@mui/material';
import { Chart, registerables } from 'chart.js';
import { hexToRgbA, getRandomColor } from '../utils/colorManipulators';

// Register the necessary components with Chart.js
Chart.register(...registerables);

const BarChart = ({ summary, title }) => {
  const categories = Object.values(summary.category);
  const amounts = Object.values(summary.amount);

  const backgroundColors = categories.map(() => hexToRgbA(getRandomColor(), 0.2));
  const borderColors = backgroundColors.map(color => color.replace('0.2', '1'));

  const data = {
    labels: categories,
    datasets: [
      {
        label: 'Amount',
        data: amounts,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        borderWidth: 1,
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
      <Bar data={data} options={options} />
    </Box>
  );
};

BarChart.propTypes = {
  summary: PropTypes.shape({
    amount: PropTypes.objectOf(PropTypes.number).isRequired,
    category: PropTypes.objectOf(PropTypes.string).isRequired,
  }).isRequired,
  title: PropTypes.string,
};

export default BarChart;
