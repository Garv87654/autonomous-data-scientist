import React, { useState } from 'react';
import { Loader2, Trophy, Target } from 'lucide-react';

export default function TrainingTab({ datasetId, schema, onComplete }) {
  const [targetColumn, setTargetColumn] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleTrain = async () => {
    if (!targetColumn) {
      setError("Please select a target column.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/train', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dataset_id: datasetId, target_column: targetColumn })
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Training failed');
      }
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8">
      {!results && !loading && (
        <div className="bg-white border border-slate-200 rounded-xl p-8 text-center max-w-lg mx-auto shadow-sm">
          <Target className="w-12 h-12 text-blue-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-slate-800 mb-2">Select Target Variable</h2>
          <p className="text-slate-500 mb-6">Choose the column you want the AI to predict. We will automatically detect if it's a classification or regression problem.</p>
          
          <select 
            value={targetColumn} 
            onChange={(e) => setTargetColumn(e.target.value)}
            className="w-full p-3 border border-slate-300 rounded-lg mb-6 text-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          >
            <option value="">-- Select Target Column --</option>
            {schema.map((col) => (
              <option key={col.name} value={col.name}>{col.name}</option>
            ))}
          </select>

          <button 
            onClick={handleTrain}
            className="w-full py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-sm"
          >
            Start AutoML Training
          </button>
          {error && <p className="mt-4 text-red-500 text-sm">{error}</p>}
        </div>
      )}

      {loading && (
        <div className="flex flex-col items-center justify-center py-20 space-y-4">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin" />
          <h3 className="text-xl font-medium text-slate-800">Training Models</h3>
          <p className="text-slate-500 text-center max-w-md">Running cross-validation on Logistic Regression, Random Forest, and XGBoost. May take a minute...</p>
        </div>
      )}

      {results && (
        <div className="animate-in fade-in slide-in-from-bottom-4">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h2 className="text-2xl font-bold text-slate-800">Training Results</h2>
              <p className="text-slate-500 capitalize">{results.problem_type} Task</p>
            </div>
            <button 
              onClick={() => onComplete(results.experiment_id)}
              className="px-6 py-2.5 bg-slate-900 text-white rounded-lg font-medium hover:bg-slate-800 transition-colors"
            >
              Explain Best Model
            </button>
          </div>

          <div className="grid gap-4">
            {results.all_results.sort((a,b) => {
               // Sort by main metric
               if (results.problem_type === 'classification') {
                   return b.metrics.accuracy - a.metrics.accuracy;
               } else {
                   return a.metrics.rmse - b.metrics.rmse;
               }
            }).map((res, idx) => {
              const isBest = res.model === results.best_model;
              return (
                <div key={res.model} className={`p-6 rounded-xl border flex items-center justify-between ${isBest ? 'bg-blue-50 border-blue-200 shadow-md ring-1 ring-blue-500' : 'bg-white border-slate-200'}`}>
                  <div className="flex items-center space-x-4">
                    <div className="text-2xl font-bold text-slate-400 w-8">{idx + 1}</div>
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 flex items-center">
                        {res.model}
                        {isBest && <Trophy className="w-5 h-5 text-amber-500 ml-2" />}
                      </h3>
                      {isBest && <span className="text-xs font-semibold text-blue-600 uppercase tracking-wider">Best Performing</span>}
                    </div>
                  </div>
                  <div className="flex space-x-8">
                    {Object.entries(res.metrics).map(([mName, mVal]) => (
                      <div key={mName} className="text-right">
                        <p className="text-xs uppercase tracking-wider text-slate-500 font-semibold">{mName}</p>
                        <p className="text-lg font-bold text-slate-800">{mVal.toFixed(4)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
