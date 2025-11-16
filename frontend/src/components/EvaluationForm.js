// frontend/src/components/EvaluationForm.js

import React, { useState } from 'react';

const AVAILABLE_PARAMS = ['Coverage', 'Clarity', 'Conciseness', 'Accuracy'];

const sampleTranscript = `Photosynthesis is a process used by plants, algae, and certain bacteria to harness energy from sunlight and turn it into chemical energy. This process is crucial for life on Earth as it produces most of the oxygen in the atmosphere. The chemical equation is 6CO2 + 6H2O + Light Energy -> C6H12O6 + 6O2. There are two main stages: the light-dependent reactions and the light-independent reactions, also known as the Calvin cycle. The light-dependent reactions capture light energy to make ATP and NADPH, while the Calvin cycle uses this energy to convert carbon dioxide into glucose.`;
const sampleSummary = `Plants use photosynthesis to convert sunlight into energy. This creates oxygen. The process involves light and dark reactions to make glucose from CO2 and water.`;

function EvaluationForm({ onEvaluate, isLoading }) {
    const [transcript, setTranscript] = useState(sampleTranscript);
    const [summary, setSummary] = useState(sampleSummary);
    const [parameters, setParameters] = useState(['Coverage', 'Clarity', 'Conciseness']);

    const handleCheckboxChange = (param) => {
        setParameters(prev => 
            prev.includes(param) 
                ? prev.filter(p => p !== param) 
                : [...prev, param]
        );
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!transcript.trim() || !summary.trim() || parameters.length === 0) {
            alert('Please fill in the transcript, summary, and select at least one parameter.');
            return;
        }
        onEvaluate({ transcript, summary, parameters, weights: null }); // Weights can be added here if UI is extended
    };

    return (
        <form onSubmit={handleSubmit} className="evaluation-form">
            <div className="form-group">
                <label htmlFor="transcript">Lecture Transcript</label>
                <textarea 
                    id="transcript"
                    value={transcript}
                    onChange={(e) => setTranscript(e.target.value)}
                    rows="10"
                    placeholder="Paste the full lecture transcript here..."
                    required
                />
            </div>
            <div className="form-group">
                <label htmlFor="summary">Student Summary</label>
                <textarea 
                    id="summary"
                    value={summary}
                    onChange={(e) => setSummary(e.target.value)}
                    rows="5"
                    placeholder="Paste the student's summary here..."
                    required
                />
            </div>
            <div className="form-group">
                <label>Evaluation Parameters</label>
                <div className="checkbox-group">
                    {AVAILABLE_PARAMS.map(param => (
                        <label key={param}>
                            <input 
                                type="checkbox" 
                                checked={parameters.includes(param)} 
                                onChange={() => handleCheckboxChange(param)} 
                            />
                            {param}
                        </label>
                    ))}
                </div>
            </div>
            <button type="submit" disabled={isLoading}>
                {isLoading ? 'Evaluating...' : 'Evaluate Summary'}
            </button>
        </form>
    );
}

export default EvaluationForm;
