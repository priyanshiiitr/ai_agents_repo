// frontend/src/components/ResultDisplay.js

import React from 'react';

function ResultDisplay({ result }) {
    if (!result) return null;

    const { final_score, scores, explanation } = result;

    return (
        <div className="result-display">
            <h2>Evaluation Result</h2>
            <div className="final-score-container">
                <div className="score-label">Final Score</div>
                <div className="score-value">{final_score.toFixed(1)} / 10</div>
            </div>
            
            <h3>Score Breakdown</h3>
            <ul className="score-breakdown">
                {Object.entries(scores).map(([param, score]) => (
                    <li key={param}>
                        <strong>{param}:</strong> {score} / 10
                    </li>
                ))}
            </ul>

            <h3>Explanation</h3>
            <p className="explanation-text">
                {explanation}
            </p>
        </div>
    );
}

export default ResultDisplay;
