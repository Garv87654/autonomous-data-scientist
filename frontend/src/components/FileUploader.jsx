import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, FileSpreadsheet, Loader2 } from 'lucide-react';

export default function FileUploader({ onUpload, isUploading }) {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles?.length > 0) {
      onUpload(acceptedFiles[0]);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    },
    maxFiles: 1
  });

  return (
    <div 
      {...getRootProps()} 
      className={`w-full max-w-2xl p-12 border-2 border-dashed rounded-2xl transition-all duration-300 cursor-pointer flex flex-col items-center justify-center group
        ${isDragActive ? 'border-blue-500 bg-blue-50/50' : 'border-slate-300 bg-white hover:border-blue-400 hover:bg-slate-50'}
        ${isDragReject ? 'border-red-500 bg-red-50/50' : ''}
        ${isUploading ? 'opacity-75 pointer-events-none' : 'shadow-sm hover:shadow-md'}
      `}
    >
      <input {...getInputProps()} />
      
      {isUploading ? (
        <div className="flex flex-col items-center space-y-4">
          <Loader2 className="w-16 h-16 text-blue-600 animate-spin" />
          <p className="text-lg font-medium text-slate-700">Analyzing dataset...</p>
          <p className="text-sm text-slate-500">Detecting schema and quality issues</p>
        </div>
      ) : (
        <>
          <div className="mb-6 p-4 bg-blue-100 text-blue-600 rounded-full group-hover:scale-110 transition-transform duration-300">
            {isDragActive ? (
              <FileSpreadsheet className="w-10 h-10" />
            ) : (
              <UploadCloud className="w-10 h-10" />
            )}
          </div>
          <h3 className="text-xl font-semibold text-slate-800 mb-2">
            {isDragActive ? 'Drop your file here' : 'Drag & drop a dataset'}
          </h3>
          <p className="text-slate-500 text-center mb-6 max-w-md">
            Supported formats: CSV, XLS, XLSX. The file will be processed locally and never stored permanently without permission.
          </p>
          <div className="px-6 py-2.5 bg-white border border-slate-200 text-slate-700 rounded-lg shadow-sm font-medium group-hover:border-blue-300 group-hover:text-blue-700 transition-colors">
            Browse Files
          </div>
        </>
      )}
    </div>
  );
}
