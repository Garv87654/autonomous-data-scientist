import React from 'react';
import { AlertCircle, FileText, CheckCircle2, AlertTriangle, Hash, Calendar, Type, MoreHorizontal } from 'lucide-react';

export default function DataSummary({ data }) {
  if (!data || !data.analysis) return null;

  const { filename, analysis } = data;
  const { dataset_stats, schema, quality_issues } = analysis;

  const getTypeIcon = (type) => {
    switch(type) {
      case 'numeric': return <Hash className="w-4 h-4 text-blue-500" />;
      case 'datetime': return <Calendar className="w-4 h-4 text-purple-500" />;
      case 'categorical': return <MoreHorizontal className="w-4 h-4 text-amber-500" />;
      case 'text': return <Type className="w-4 h-4 text-emerald-500" />;
      default: return <FileText className="w-4 h-4 text-slate-500" />;
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Left Column: Stats & Issues */}
      <div className="space-y-6 lg:col-span-1">
        {/* Overview Card */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center">
            <FileText className="w-5 h-5 mr-2 text-slate-400" />
            Dataset Overview
          </h3>
          <div className="bg-slate-50 rounded-xl p-4 mb-4 border border-slate-100">
            <p className="text-sm font-medium text-slate-500 truncate" title={filename}>
              File: <span className="text-slate-800">{filename}</span>
            </p>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50/50 rounded-xl p-4 border border-blue-100">
              <p className="text-xs font-semibold text-blue-600 uppercase tracking-wider mb-1">Rows</p>
              <p className="text-2xl font-bold text-slate-800">{dataset_stats.row_count.toLocaleString()}</p>
            </div>
            <div className="bg-emerald-50/50 rounded-xl p-4 border border-emerald-100">
              <p className="text-xs font-semibold text-emerald-600 uppercase tracking-wider mb-1">Columns</p>
              <p className="text-2xl font-bold text-slate-800">{dataset_stats.col_count}</p>
            </div>
            <div className="col-span-2 bg-amber-50/50 rounded-xl p-4 border border-amber-100 flex justify-between items-center">
              <div>
                <p className="text-xs font-semibold text-amber-700 uppercase tracking-wider mb-1">Duplicate Rows</p>
                <p className="text-2xl font-bold text-slate-800">{dataset_stats.duplicate_count}</p>
              </div>
              {dataset_stats.duplicate_count > 0 ? (
                <AlertTriangle className="w-8 h-8 text-amber-400" />
              ) : (
                <CheckCircle2 className="w-8 h-8 text-emerald-400" />
              )}
            </div>
          </div>
        </div>

        {/* Data Quality Report Card */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center">
            <AlertCircle className="w-5 h-5 mr-2 text-rose-500" />
            Data Quality Issues
          </h3>
          {quality_issues.length === 0 ? (
            <div className="flex flex-col items-center justify-center p-6 text-center bg-emerald-50 rounded-xl border border-emerald-100">
              <CheckCircle2 className="w-10 h-10 text-emerald-500 mb-2" />
              <p className="text-emerald-800 font-medium">Dataset looks clean!</p>
              <p className="text-emerald-600 text-sm">No major quality issues detected.</p>
            </div>
          ) : (
            <ul className="space-y-3">
              {quality_issues.map((issue, idx) => (
                <li key={idx} className="flex items-start text-sm text-slate-700 bg-rose-50 p-3 rounded-lg border border-rose-100">
                  <span className="w-1.5 h-1.5 rounded-full bg-rose-500 mt-1.5 mr-2 flex-shrink-0" />
                  <span>{issue}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* Right Column: Schema Table */}
      <div className="lg:col-span-2">
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden h-full flex flex-col">
          <div className="px-6 py-5 border-b border-slate-200 bg-slate-50 flex justify-between items-center">
            <h3 className="text-lg font-semibold text-slate-800">Schema Inference</h3>
            <span className="text-xs font-medium text-slate-500 bg-white px-2.5 py-1 rounded-full border border-slate-200 shadow-sm">
              {schema.length} features
            </span>
          </div>
          <div className="overflow-x-auto flex-1">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-white border-b border-slate-200 text-xs uppercase tracking-wider text-slate-500 font-semibold">
                  <th className="px-6 py-4">Column Name</th>
                  <th className="px-6 py-4">Inferred Type</th>
                  <th className="px-6 py-4">Missing</th>
                  <th className="px-6 py-4">Unique</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {schema.map((col, idx) => (
                  <tr key={idx} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4">
                      <span className="font-medium text-slate-800">{col.name}</span>
                      <span className="block text-xs text-slate-400 font-mono mt-0.5">{col.pandas_type}</span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        {getTypeIcon(col.inferred_type)}
                        <span className="text-sm text-slate-700 capitalize font-medium">{col.inferred_type}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      {col.missing_count > 0 ? (
                        <div className="flex flex-col">
                          <span className="text-sm font-semibold text-rose-600">{col.missing_percent}%</span>
                          <span className="text-xs text-slate-500">{col.missing_count} rows</span>
                        </div>
                      ) : (
                        <span className="text-sm text-slate-400">None</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-700">
                      {col.unique_count.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
