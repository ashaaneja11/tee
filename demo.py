import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, Database, Download, AlertCircle, ChevronRight, Loader2, Sparkles, BarChart3, Zap } from 'lucide-react';
import Papa from 'papaparse';

const SAP_TEST_CASE_CONVERTER = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [csvData, setCsvData] = useState([]);
  const [evaluatedTests, setEvaluatedTests] = useState([]);
  const [sapQueries, setSapQueries] = useState([]);
  const [queryResults, setQueryResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const steps = [
    { id: 0, name: 'Upload', icon: Upload, color: 'from-violet-500 to-purple-500' },
    { id: 1, name: 'Evaluate', icon: Sparkles, color: 'from-blue-500 to-cyan-500' },
    { id: 2, name: 'Generate', icon: Zap, color: 'from-emerald-500 to-teal-500' },
    { id: 3, name: 'Results', icon: BarChart3, color: 'from-pink-500 to-rose-500' }
  ];

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        setCsvData(results.data);
        setError('');
      },
      error: (error) => {
        setError(`Error parsing CSV: ${error.message}`);
      }
    });
  };

  const evaluateTestCases = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-20250514',
          max_tokens: 1000,
          messages: [{
            role: 'user',
            content: `Evaluate these test cases for quality, completeness, and clarity. Return ONLY a JSON array with no preamble or markdown:\n\n${JSON.stringify(csvData)}\n\nFormat: [{"testCase": "...", "evaluation": "pass/fail", "score": 0-100, "feedback": "..."}]`
          }]
        })
      });

      const data = await response.json();
      const content = data.content[0].text.trim();
      const cleanContent = content.replace(/```json|```/g, '').trim();
      const evaluated = JSON.parse(cleanContent);
      
      setEvaluatedTests(evaluated);
      setCurrentStep(2);
    } catch (err) {
      setError(`Evaluation failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const generateSAPQueries = async () => {
    setLoading(true);
    setError('');
    
    try {
      const passedTests = evaluatedTests.filter(t => t.evaluation === 'pass');
      
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-20250514',
          max_tokens: 1000,
          messages: [{
            role: 'user',
            content: `Convert these test cases to SAP queries. Return ONLY a JSON array:\n\n${JSON.stringify(passedTests)}\n\nFormat: [{"testCase": "...", "sapQuery": "SELECT ...", "description": "..."}]`
          }]
        })
      });

      const data = await response.json();
      const content = data.content[0].text.trim();
      const cleanContent = content.replace(/```json|```/g, '').trim();
      const queries = JSON.parse(cleanContent);
      
      setSapQueries(queries);
      
      const mockResults = queries.map(q => ({
        query: q.sapQuery,
        rows: Math.floor(Math.random() * 100) + 1,
        status: 'success'
      }));
      
      setQueryResults(mockResults);
      setCurrentStep(3);
    } catch (err) {
      setError(`Query generation failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const exportResults = () => {
    const exportData = {
      evaluatedTests,
      sapQueries,
      queryResults,
      timestamp: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sap-test-results-${Date.now()}.json`;
    a.click();
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden">
      {/* Animated Background Effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-pink-500/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
      </div>

      {/* Header */}
      <header className="relative border-b border-white/5 backdrop-blur-xl bg-white/5">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center">
                  <Database className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent">
                  SAP Test Converter
                </h1>
              </div>
              <p className="text-sm text-slate-400 ml-13">AI-Powered Test Case Analysis & Query Generation</p>
            </div>
            <div className="flex items-center gap-3 px-5 py-3 bg-gradient-to-r from-violet-500/20 to-purple-500/20 rounded-2xl border border-violet-500/30 backdrop-blur-sm">
              <Sparkles className="w-5 h-5 text-violet-400" />
              <span className="text-sm font-semibold text-white">Enterprise AI</span>
            </div>
          </div>
        </div>
      </header>

      {/* Progress Steps */}
      <div className="max-w-7xl mx-auto px-6 py-12 relative">
        <div className="backdrop-blur-xl bg-white/5 rounded-3xl border border-white/10 p-8">
          <div className="flex items-center justify-between">
            {steps.map((step, idx) => {
              const Icon = step.icon;
              const isActive = currentStep === step.id;
              const isCompleted = currentStep > step.id;
              
              return (
                <React.Fragment key={step.id}>
                  <div className="flex flex-col items-center flex-1 group">
                    <div className={`relative w-16 h-16 rounded-2xl flex items-center justify-center transition-all duration-500 ${
                      isActive ? `bg-gradient-to-br ${step.color} shadow-2xl scale-110` :
                      isCompleted ? 'bg-gradient-to-br from-emerald-500 to-teal-500 shadow-xl' :
                      'bg-white/10 backdrop-blur-sm border border-white/20'
                    }`}>
                      <Icon className={`w-8 h-8 transition-all ${
                        isActive || isCompleted ? 'text-white' : 'text-slate-500'
                      }`} />
                      {isActive && (
                        <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-white/20 to-transparent animate-pulse"></div>
                      )}
                    </div>
                    <span className={`mt-3 text-sm font-semibold transition-all ${
                      isActive ? 'text-white scale-105' :
                      isCompleted ? 'text-emerald-400' :
                      'text-slate-500'
                    }`}>
                      {step.name}
                    </span>
                  </div>
                  {idx < steps.length - 1 && (
                    <div className="flex-1 h-1 mx-6 rounded-full overflow-hidden bg-white/10 relative">
                      <div className={`h-full transition-all duration-700 ${
                        currentStep > step.id ? 'bg-gradient-to-r from-emerald-500 to-teal-500 w-full' : 'w-0'
                      }`}></div>
                    </div>
                  )}
                </React.Fragment>
              );
            })}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 pb-12 relative">
        <div className="backdrop-blur-xl bg-white/5 rounded-3xl border border-white/10 p-10">
          {error && (
            <div className="mb-8 p-5 bg-red-500/10 border border-red-500/30 rounded-2xl flex items-start gap-4 backdrop-blur-sm">
              <AlertCircle className="w-6 h-6 text-red-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold text-red-300">Error Occurred</p>
                <p className="text-sm text-red-400 mt-1">{error}</p>
              </div>
            </div>
          )}

          {/* Step 0: Upload CSV */}
          {currentStep === 0 && (
            <div className="text-center">
              <div className="w-24 h-24 bg-gradient-to-br from-violet-500 to-purple-600 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-2xl shadow-violet-500/30 relative">
                <Upload className="w-12 h-12 text-white" />
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-white/20 to-transparent animate-pulse"></div>
              </div>
              <h2 className="text-4xl font-bold text-white mb-3">Upload Test Cases</h2>
              <p className="text-slate-400 text-lg mb-12">Drop your CSV file to begin the AI analysis</p>
              
              <label className="inline-flex items-center gap-4 px-10 py-5 bg-gradient-to-r from-violet-500 to-purple-600 text-white rounded-2xl font-semibold cursor-pointer hover:shadow-2xl hover:shadow-violet-500/50 transition-all duration-300 hover:scale-105">
                <Upload className="w-6 h-6" />
                Select CSV File
                <input type="file" accept=".csv" onChange={handleFileUpload} className="hidden" />
              </label>

              {csvData.length > 0 && (
                <div className="mt-12 p-8 bg-gradient-to-br from-emerald-500/10 to-teal-500/10 border border-emerald-500/30 rounded-3xl backdrop-blur-sm">
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-4">
                      <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-xl">
                        <CheckCircle className="w-8 h-8 text-white" />
                      </div>
                      <div className="text-left">
                        <p className="font-bold text-white text-xl">File Loaded</p>
                        <p className="text-emerald-400">{csvData.length} test cases detected</p>
                      </div>
                    </div>
                    <button
                      onClick={() => setCurrentStep(1)}
                      className="flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-emerald-500 to-teal-600 text-white rounded-xl font-semibold hover:shadow-2xl hover:shadow-emerald-500/50 transition-all duration-300 hover:scale-105"
                    >
                      Continue
                      <ChevronRight className="w-6 h-6" />
                    </button>
                  </div>
                  <div className="bg-slate-900/50 rounded-2xl p-6 max-h-80 overflow-auto border border-white/10 backdrop-blur-sm">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-white/10">
                          {Object.keys(csvData[0] || {}).map((key) => (
                            <th key={key} className="px-4 py-3 text-left font-semibold text-violet-400">{key}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {csvData.slice(0, 5).map((row, idx) => (
                          <tr key={idx} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                            {Object.values(row).map((val, i) => (
                              <td key={i} className="px-4 py-3 text-slate-300">{val}</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Step 1: Evaluate Tests */}
          {currentStep === 1 && (
            <div className="text-center">
              <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-2xl shadow-blue-500/30 relative">
                <Sparkles className="w-12 h-12 text-white" />
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-white/20 to-transparent animate-pulse"></div>
              </div>
              <h2 className="text-4xl font-bold text-white mb-3">AI Evaluation</h2>
              <p className="text-slate-400 text-lg mb-12">Let AI analyze your test cases for quality and completeness</p>
              
              <button
                onClick={evaluateTestCases}
                disabled={loading}
                className="inline-flex items-center gap-4 px-10 py-5 bg-gradient-to-r from-blue-500 to-cyan-600 text-white rounded-2xl font-semibold hover:shadow-2xl hover:shadow-blue-500/50 transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-6 h-6 animate-spin" />
                    Analyzing with AI...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-6 h-6" />
                    Start AI Analysis
                  </>
                )}
              </button>

              <div className="mt-12 p-8 bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/30 rounded-3xl backdrop-blur-sm">
                <div className="flex items-center justify-center gap-4">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center">
                    <FileText className="w-6 h-6 text-white" />
                  </div>
                  <p className="text-lg">
                    <span className="font-bold text-white text-2xl">{csvData.length}</span>
                    <span className="text-slate-400 ml-2">test cases ready</span>
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Generate SAP Queries */}
          {currentStep === 2 && (
            <div>
              <div className="text-center mb-12">
                <div className="w-24 h-24 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-2xl shadow-emerald-500/30">
                  <CheckCircle className="w-12 h-12 text-white" />
                </div>
                <h2 className="text-4xl font-bold text-white mb-3">Evaluation Complete</h2>
                <p className="text-slate-400 text-lg">Review results and generate SAP queries</p>
              </div>

              <div className="grid grid-cols-3 gap-6 mb-10">
                <div className="p-6 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-2xl backdrop-blur-sm hover:scale-105 transition-transform">
                  <p className="text-4xl font-bold text-emerald-400 mb-2">
                    {evaluatedTests.filter(t => t.evaluation === 'pass').length}
                  </p>
                  <p className="text-sm text-emerald-300 font-semibold">Passed Tests</p>
                </div>
                <div className="p-6 bg-gradient-to-br from-red-500/20 to-pink-500/20 border border-red-500/30 rounded-2xl backdrop-blur-sm hover:scale-105 transition-transform">
                  <p className="text-4xl font-bold text-red-400 mb-2">
                    {evaluatedTests.filter(t => t.evaluation === 'fail').length}
                  </p>
                  <p className="text-sm text-red-300 font-semibold">Failed Tests</p>
                </div>
                <div className="p-6 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border border-blue-500/30 rounded-2xl backdrop-blur-sm hover:scale-105 transition-transform">
                  <p className="text-4xl font-bold text-blue-400 mb-2">
                    {Math.round(evaluatedTests.reduce((sum, t) => sum + (t.score || 0), 0) / evaluatedTests.length)}%
                  </p>
                  <p className="text-sm text-blue-300 font-semibold">Average Score</p>
                </div>
              </div>

              <div className="max-h-96 overflow-auto mb-10 rounded-2xl border border-white/10">
                {evaluatedTests.map((test, idx) => (
                  <div key={idx} className={`p-6 border-b border-white/10 last:border-b-0 backdrop-blur-sm transition-all hover:bg-white/5 ${
                    test.evaluation === 'pass' ? 'bg-emerald-500/5' : 'bg-red-500/5'
                  }`}>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="font-semibold text-white text-lg">{test.testCase}</p>
                        <p className="text-sm text-slate-400 mt-2">{test.feedback}</p>
                      </div>
                      <div className="flex items-center gap-3 ml-6">
                        <span className={`px-4 py-2 rounded-xl text-xs font-bold ${
                          test.evaluation === 'pass' ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-white' : 'bg-gradient-to-r from-red-500 to-pink-600 text-white'
                        }`}>
                          {test.evaluation.toUpperCase()}
                        </span>
                        <span className="px-4 py-2 bg-white/10 text-white rounded-xl text-xs font-bold backdrop-blur-sm">
                          {test.score}%
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="text-center">
                <button
                  onClick={generateSAPQueries}
                  disabled={loading || evaluatedTests.filter(t => t.evaluation === 'pass').length === 0}
                  className="inline-flex items-center gap-4 px-10 py-5 bg-gradient-to-r from-violet-500 to-purple-600 text-white rounded-2xl font-semibold hover:shadow-2xl hover:shadow-violet-500/50 transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-6 h-6 animate-spin" />
                      Generating SAP Queries...
                    </>
                  ) : (
                    <>
                      <Zap className="w-6 h-6" />
                      Generate SAP Queries
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {/* Step 3: View Results */}
          {currentStep === 3 && (
            <div>
              <div className="text-center mb-12">
                <div className="w-24 h-24 bg-gradient-to-br from-pink-500 to-rose-600 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-2xl shadow-pink-500/30">
                  <BarChart3 className="w-12 h-12 text-white" />
                </div>
                <h2 className="text-4xl font-bold text-white mb-3">Results Ready</h2>
                <p className="text-slate-400 text-lg">SAP queries generated successfully</p>
              </div>

              <div className="space-y-6 mb-10">
                {sapQueries.map((query, idx) => (
                  <div key={idx} className="rounded-2xl overflow-hidden border border-white/10 backdrop-blur-sm hover:border-violet-500/50 transition-all">
                    <div className="bg-gradient-to-r from-violet-500/20 to-purple-500/20 px-8 py-6 border-b border-white/10">
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <h3 className="font-bold text-white text-xl mb-2">{query.testCase}</h3>
                          <p className="text-sm text-slate-300">{query.description}</p>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className="px-5 py-2 bg-gradient-to-r from-emerald-500 to-teal-600 text-white rounded-xl text-sm font-bold shadow-lg">
                            {queryResults[idx]?.rows} rows
                          </span>
                          <button
                            onClick={() => copyToClipboard(query.sapQuery)}
                            className="px-6 py-3 bg-gradient-to-r from-violet-500 to-purple-600 text-white rounded-xl text-sm font-bold hover:shadow-2xl hover:shadow-violet-500/50 transition-all hover:scale-105"
                          >
                            Copy Query
                          </button>
                        </div>
                      </div>
                    </div>
                    <div className="p-8 bg-slate-950/80 backdrop-blur-sm">
                      <pre className="text-sm text-emerald-400 font-mono overflow-x-auto">{query.sapQuery}</pre>
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex justify-center gap-6">
                <button
                  onClick={exportResults}
                  className="inline-flex items-center gap-4 px-10 py-5 bg-gradient-to-r from-violet-500 to-purple-600 text-white rounded-2xl font-semibold hover:shadow-2xl hover:shadow-violet-500/50 transition-all duration-300 hover:scale-105"
                >
                  <Download className="w-6 h-6" />
                  Export Results
                </button>
                <button
                  onClick={() => {
                    setCsvData([]);
                    setEvaluatedTests([]);
                    setSapQueries([]);
                    setQueryResults([]);
                    setCurrentStep(0);
                    setError('');
                  }}
                  className="px-10 py-5 bg-white/10 text-white rounded-2xl font-semibold hover:bg-white/20 transition-all duration-300 hover:scale-105 backdrop-blur-sm border border-white/20"
                >
                  Start Over
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SAP_TEST_CASE_CONVERTER;
