import React, { useState } from 'react';
import { Loader2, Wand2, CheckCircle2 } from 'lucide-react';

export default function CleaningTab({ datasetId, onNext }) {
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);

  const handleClean = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8000/api/clean/${datasetId}`, { method: 'POST' });
      if (!response.ok) throw new Error('Cleaning failed');
      const data = await response.json();
      setLogs(data.cleaning_log);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-8">
      <div className="text-center mb-8">
        <div className="mx-auto w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mb-4">
          <Wand2 className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-slate-800">Auto Cleaning & Preprocessing</h2>
        <p className="text-slate-500 mt-2">Let our AI impute missing values, handle outliers, and encode categoricals automatically.</p>
      </div>

      {logs.length === 0 && !loading && (
        <div className="flex justify-center">
          <button onClick={handleClean} className="px-6 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-colors shadow-sm flex items-center">
            <Wand2 className="w-5 h-5 mr-2" />
            Start Auto-Cleaning
          </button>
        </div>
      )}

      {loading && (
        <div className="flex flex-col items-center space-y-4 text-blue-600 py-12">
          <Loader2 className="w-10 h-10 animate-spin" />
          <p className="font-medium">Applying transformations...</p>
        </div>
      )}

      {error && <div className="bg-red-50 text-red-700 p-4 rounded-lg text-center">{error}</div>}

      {logs.length > 0 && (
        <div className="animate-in fade-in slide-in-from-bottom-4">
          <div className="bg-emerald-50 border border-emerald-100 rounded-xl p-6 mb-6">
            <h3 className="font-semibold text-emerald-800 flex items-center mb-4">
              <CheckCircle2 className="w-5 h-5 mr-2" />
              Cleaning Complete
            </h3>
            <ul className="space-y-3">
              {logs.map((log, i) => (
                <li key={i} className="text-sm text-emerald-700 flex items-start">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 mr-2 flex-shrink-0" />
                  {log}
                </li>
              ))}
            </ul>
          </div>
          <div className="flex justify-end">
            <button onClick={onNext} className="px-6 py-2.5 bg-slate-900 text-white rounded-lg font-medium hover:bg-slate-800 transition-colors">
              Proceed to EDA
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
