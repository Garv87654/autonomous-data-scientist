import React, { useState, useEffect } from 'react';
import { Loader2, FileText, Download } from 'lucide-react';

export default function ReportTab({ experimentId }) {
  const [report, setReport] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:8000/api/report/${experimentId}`, { method: 'POST' })
      .then(res => res.json())
      .then(data => setReport(data.report))
      .catch(err => setReport("Error generating report: " + err.message))
      .finally(() => setLoading(false));
  }, [experimentId]);

  if (loading) return (
    <div className="flex flex-col items-center justify-center py-20 space-y-4">
      <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
      <p className="text-slate-600 font-medium text-lg">AI is writing your executive report...</p>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-slate-800 flex items-center">
          <FileText className="w-6 h-6 mr-2 text-blue-600" />
          Final Executive Report
        </h2>
        <button 
          onClick={() => {
            const blob = new Blob([report], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'AI_Data_Scientist_Report.md';
            a.click();
          }}
          className="flex items-center px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 text-sm font-medium rounded-lg transition-colors border border-slate-300"
        >
          <Download className="w-4 h-4 mr-2" />
          Export MD
        </button>
      </div>

      <div className="bg-white border border-slate-200 rounded-xl p-8 shadow-sm">
        <div className="prose prose-slate max-w-none prose-headings:text-slate-800 prose-a:text-blue-600">
          <pre className="whitespace-pre-wrap font-sans text-slate-700 text-sm md:text-base leading-relaxed bg-transparent p-0 m-0 border-0">
            {report}
          </pre>
        </div>
      </div>
    </div>
  );
}
