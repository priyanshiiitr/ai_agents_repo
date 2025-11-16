// frontend/src/App.js

import React, { useState } from 'react';
import './App.css';
import EvaluationForm from './components/EvaluationForm';
import ResultDisplay from './components/ResultDisplay';
import { evaluateSummary } from './services/api';

function App() {
    const [result, setResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleEvaluate = async (formData) => {
        setIsLoading(true);
        setError('');
        setResult(null);
        try {
            const data = await evaluateSummary(formData);
            setResult(data);
        } catch (err) {
            setError(err.response?.data?.detail || 'An unexpected error occurred. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>AI Summary Evaluator</h1>
                <p>Paste a transcript and a student's summary to get an AI-powered evaluation.</p>
            </header>
            <main>
                <EvaluationForm onEvaluate={handleEvaluate} isLoading={isLoading} />
                {isLoading && <div className="loading">Evaluating...</div>}
                {error && <div className="error">Error: {error}</div>}
                {result && <ResultDisplay result={result} />}
            </main>
            <footer>
                <p>Powered by AI</p>
            </footer>
        </div>
    );
}

export default App;
