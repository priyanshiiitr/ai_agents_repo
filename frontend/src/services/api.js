// frontend/src/services/api.js

import axios from 'axios';

const apiClient = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
    headers: {
        'Content-Type': 'application/json',
    }
});

export const evaluateSummary = async (data) => {
    const response = await apiClient.post('/evaluate', data);
    return response.data;
};
