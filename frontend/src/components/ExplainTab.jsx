import React, { useState, useEffect } from 'react';
import { Loader2, Lightbulb } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function ExplainTab({ experimentId, onNext }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/explain/${experimentId}`)
      .then(res => res.json())
      .then(resData => {
        if (resData.error) throw new Error(resData.error);
        setData(resData);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [experimentId]);

  if (loading) return <div className="flex justify-center py-20"><Loader2 className="w-8 h-8 text-blue-500 animate-spin" /></div>;
  if (error) return <div className="text-red-500 text-center py-10">{error}</div>;

  return (
    <div className="space-y-8 max-w-5xl mx-auto py-4">
      <div className="flex items-center justify-between border-b border-slate-200 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-amber-100 rounded-lg"><Lightbulb className="w-6 h-6 text-amber-600" /></div>
          <div>
            <h2 className="text-2xl font-bold text-slate-800">Model Explainability (SHAP)</h2>
            <p className="text-slate-500 text-sm">Understand what drives the model's predictions.</p>
          </div>
        </div>
        <button onClick={onNext} className="px-6 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-sm">
          Generate Final Report
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white border border-slate-200 shadow-sm rounded-xl p-6">
          <h3 className="text-lg font-semibold text-slate-800 mb-2">Global Feature Importance</h3>
          <p className="text-sm text-slate-500 mb-6">Features that have the largest impact on predictions across all data points.</p>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart layout="vertical" data={data.global_importance} margin={{ top: 0, right: 30, left: 60, bottom: 0 }}>
                <XAxis type="number" hide />
                <YAxis dataKey="feature" type="category" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#475569'}} />
                <Tooltip cursor={{fill: '#f8fafc'}} contentStyle={{borderRadius: '8px', border: '1px solid #e2e8f0'}} />
                <Bar dataKey="importance" fill="#8b5cf6" radius={[0, 4, 4, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white border border-slate-200 shadow-sm rounded-xl p-6">
          <h3 className="text-lg font-semibold text-slate-800 mb-2">Local Explanation (Sample Row)</h3>
          <p className="text-sm text-slate-500 mb-6">How individual feature values contributed to a specific prediction.</p>
          <div className="space-y-4">
            {data.local_explanation_sample.map((item, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
                <div>
                  <span className="font-semibold text-slate-700">{item.feature}</span>
                  <span className="ml-2 text-xs text-slate-500 font-mono bg-white px-2 py-0.5 rounded border border-slate-200">Value: {item.actual_value.toFixed(2)}</span>
                </div>
                <div className={`font-bold ${item.contribution > 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                  {item.contribution > 0 ? '+' : ''}{item.contribution.toFixed(4)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
