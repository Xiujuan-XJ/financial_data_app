import PropTypes from 'prop-types';
import { Pie } from 'react-chartjs-2';
import { Box, Typography } from '@mui/material';
import { Chart, registerables } from 'chart.js';
import { hexToRgbA, getRandomColor } from '../utils/colorManipulators';

// Register the necessary components with Chart.js
Chart.register(...registerables);

const PieChart = ({ summary, title }) => {
  const categories = Object.values(summary.category);
  const amounts = Object.values(summary.amount);

  const backgroundColors = categories.map(() => getRandomColor());

  const data = {
    labels: categories,
    datasets: [
      {
        label: 'Amount',
        data: amounts,
        backgroundColor: backgroundColors,
        borderColor: backgroundColors.map(color => hexToRgbA(color, 0.2)),
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            return `${context.label}: ${context.raw}`;
          },
        },
      },
    },
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 500, margin: '0 auto', padding: '2rem' }}>
      {title && (
        <Typography variant="h6" align="center" gutterBottom>
          {title}
        </Typography>
      )}
      <Pie data={data} options={options} />
    </Box>
  );
};

PieChart.propTypes = {
  summary: PropTypes.shape({
    amount: PropTypes.objectOf(PropTypes.number).isRequired,
    category: PropTypes.objectOf(PropTypes.string).isRequired,
  }).isRequired,
  title: PropTypes.string,
};

export default PieChart;
