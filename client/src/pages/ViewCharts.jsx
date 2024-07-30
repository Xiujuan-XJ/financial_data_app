import { useEffect, useState, Fragment } from 'react';
import axios from 'axios';
import { useSnackbar } from 'notistack';
import { Box, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import BarChart from "../components/BarChart";
import LineChart from '../components/LineChart';
import PieChart from '../components/PieChart';

const hardcodedResponseData = {
    "category_totals": {
        "amount": {
            "0": 33407.86,
            "1": 30209.94,
            "2": 32965.54,
            "3": 34812.27,
            "4": 35263.36,
            "5": 34830.48
        },
        "category": {
            "0": "Dining Out",
            "1": "Entertainment",
            "2": "Groceries",
            "3": "Health",
            "4": "Transportation",
            "5": "Utilities"
        }
    },
    "yearly_expenses": {
        "amount": {
            "2019": 100000,
            "2020": 120000,
            "2021": 150000
        },
        "category": {
            "2019": "2019",
            "2020": "2020",
            "2021": "2021"
        }
    },
    "monthly_expenses": {
        // Add appropriate data structure here
    },
    "daily_expenses": {
        // Add appropriate data structure here
    },
    "xiujuan_expenses": {
        // Add appropriate data structure here
    }
};

const titleize = (str) => {
  return str
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

const ViewCharts = () => {
    const [summaryData, setSummaryData] = useState(null);
    const [chartType, setChartType] = useState('bar');
    const [dataSet, setDataSet] = useState('');
    const { enqueueSnackbar } = useSnackbar();
    const API_URL = 'http://127.0.0.1:8000/read';

    const retrieveSummary = async () => {
        try {
            const response = await axios.get(API_URL,{
                headers: {
                  "Access-Control-Allow-Origin": '*' ,
                },
              });
            console.log('Response', response);
            console.log('Response data', response.data);
            setSummaryData(response.data);
            // setSummaryData(hardcodedResponseData);
            setDataSet(Object.keys(hardcodedResponseData)[0]); // Set default dataset to the first key
            enqueueSnackbar('Summary retrieved successfully', { variant: 'success' });
        } catch (error) {
            enqueueSnackbar('Error retrieving summary', { variant: 'error' });
            console.error('Error retrieving summary', error);
        }
    }

    useEffect(() => {
        retrieveSummary();
    }, []); // Empty dependency array ensures this runs only once

    const handleChartTypeChange = (event) => {
        setChartType(event.target.value);
    };

    const handleDataSetChange = (event) => {
        setDataSet(event.target.value);
    };

    const renderChart = () => {
        const selectedData = summaryData[dataSet];
        // check if selectedData is empty
        if (!selectedData || Object.keys(selectedData).length === 0) {
            return (
                <div>No data available</div>
            );
        }
        switch (chartType) {
            case 'bar':
                return <BarChart summary={selectedData} title={titleize(dataSet)} />;
            case 'line':
                return <LineChart summary={selectedData} title={titleize(dataSet)} />;
            case 'pie':
                return <PieChart summary={selectedData} title={titleize(dataSet)} />;
            default:
                return <BarChart summary={selectedData} title={titleize(dataSet)} />;
        }
    };

    return (
        <Fragment>
            <Box sx={{ display: 'flex', justifyContent: 'center', marginBottom: '1rem', gap: '1rem' }}>
                <FormControl sx={{ minWidth: 200 }}>
                    <InputLabel id="data-set-label">Data Set</InputLabel>
                    <Select
                        labelId="data-set-label"
                        id="data-set-select"
                        value={dataSet}
                        label="Data Set"
                        onChange={handleDataSetChange}
                    >
                        {summaryData && Object.keys(summaryData).map((key) => (
                            <MenuItem key={key} value={key}>
                                {titleize(key)}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <FormControl sx={{ minWidth: 200 }}>
                    <InputLabel id="chart-type-label">Chart Type</InputLabel>
                    <Select
                        labelId="chart-type-label"
                        id="chart-type-select"
                        value={chartType}
                        label="Chart Type"
                        onChange={handleChartTypeChange}
                    >
                        <MenuItem value="bar">Bar Chart</MenuItem>
                        <MenuItem value="line">Line Chart</MenuItem>
                        <MenuItem value="pie">Pie Chart</MenuItem>
                    </Select>
                </FormControl>
            </Box>
            {summaryData ? (
                renderChart()
            ) : (
                <div>Loading...</div>
            )}
        </Fragment>
    );
};

export default ViewCharts;
