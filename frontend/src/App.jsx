import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import DataSummary from './components/DataSummary';
import CleaningTab from './components/CleaningTab';
import EdaTab from './components/EdaTab';
import TrainingTab from './components/TrainingTab';
import ExplainTab from './components/ExplainTab';
import ReportTab from './components/ReportTab';
import { Database, LayoutDashboard, Wand2, BarChart3, BrainCircuit, Lightbulb, FileText } from 'lucide-react';

const TABS = [
  { id: 'profile', name: 'Profile', icon: LayoutDashboard },
  { id: 'clean', name: 'Clean', icon: Wand2 },
  { id: 'eda', name: 'EDA', icon: BarChart3 },
  { id: 'train', name: 'Train', icon: BrainCircuit },
  { id: 'explain', name: 'Explain', icon: Lightbulb },
  { id: 'report', name: 'Report', icon: FileText }
];

function App() {
  const [datasetId, setDatasetId] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [experimentId, setExperimentId] = useState(null);
  const [activeTab, setActiveTab] = useState('profile');
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = async (file) => {
    setIsUploading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Failed to upload file');
      const data = await response.json();
      setDatasetId(data.dataset_id);
      setAnalysisData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  };

  const reset = () => {
    setDatasetId(null);
    setAnalysisData(null);
    setExperimentId(null);
    setActiveTab('profile');
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      <header className="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={reset}>
            <div className="bg-blue-600 p-2 rounded-lg">
              <Database className="h-6 w-6 text-white" />
            </div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-700 to-indigo-600">
              Autonomous Data Scientist
            </h1>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!analysisData ? (
          <div className="flex flex-col items-center justify-center min-h-[60vh]">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-extrabold text-slate-800 tracking-tight mb-2">Drop your data. Get insights.</h2>
              <p className="text-lg text-slate-500 max-w-2xl mx-auto">Upload a dataset, and our AI will clean it, explore it, train models, and generate a full report automatically.</p>
            </div>
            <FileUploader onUpload={handleUpload} isUploading={isUploading} />
            {error && <div className="mt-6 bg-red-50 text-red-700 px-6 py-4 rounded-xl shadow-sm">{error}</div>}
          </div>
        ) : (
          <div className="space-y-6">
            {/* Tabs Navigation */}
            <div className="bg-white p-2 rounded-xl shadow-sm border border-slate-200 flex space-x-2 overflow-x-auto">
              {TABS.map(tab => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center px-4 py-2.5 rounded-lg font-medium text-sm transition-colors ${isActive ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}
                  >
                    <Icon className={`w-4 h-4 mr-2 ${isActive ? 'text-blue-600' : 'text-slate-400'}`} />
                    {tab.name}
                  </button>
                );
              })}
              <div className="flex-1"></div>
              <button onClick={reset} className="px-4 py-2 text-sm text-rose-600 hover:bg-rose-50 rounded-lg transition-colors font-medium">Start Over</button>
            </div>

            {/* Tab Content */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 min-h-[500px]">
              {activeTab === 'profile' && <DataSummary data={analysisData} />}
              {activeTab === 'clean' && <CleaningTab datasetId={datasetId} onNext={() => setActiveTab('eda')} />}
              {activeTab === 'eda' && <EdaTab datasetId={datasetId} onNext={() => setActiveTab('train')} />}
              {activeTab === 'train' && <TrainingTab datasetId={datasetId} schema={analysisData.analysis.schema} onComplete={(expId) => { setExperimentId(expId); setActiveTab('explain'); }} />}
              {activeTab === 'explain' && <ExplainTab experimentId={experimentId} onNext={() => setActiveTab('report')} />}
              {activeTab === 'report' && <ReportTab experimentId={experimentId} />}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
