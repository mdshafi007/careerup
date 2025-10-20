import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// API Base URL - automatically uses environment variable or falls back to localhost
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState('');
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  const [dragging, setDragging] = useState(false);

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please select a valid PDF file');
      setFile(null);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === 'application/pdf') {
      setFile(droppedFile);
      setError(null);
    } else {
      setError('Please drop a valid PDF file');
      setFile(null);
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please select a resume file first');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    formData.append('resume', file);

    try {
      // Stage 1: Uploading
      setLoadingStage('Uploading resume...');
      await new Promise(resolve => setTimeout(resolve, 800));

      // Stage 2: Extracting
      setLoadingStage('Extracting text from PDF...');
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Stage 3: Analyzing
      setLoadingStage('Analyzing skills with AI...');
      
      const response = await axios.post(`${API_BASE_URL}/api/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Stage 4: Finding jobs
      setLoadingStage('Finding matching jobs & internships...');
      await new Promise(resolve => setTimeout(resolve, 1200));

      if (response.data.success) {
        setLoadingStage('Almost done...');
        await new Promise(resolve => setTimeout(resolve, 500));
        setResults(response.data);
      } else {
        setError(response.data.error || 'Analysis failed');
      }
    } catch (err) {
      setError(
        err.response?.data?.error || 
        err.message || 
        'Failed to analyze resume. Please try again.'
      );
    } finally {
      setLoading(false);
      setLoadingStage('');
    }
  };

  const handleReset = () => {
    setFile(null);
    setResults(null);
    setError(null);
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1 className="logo">🎯 CareerUp</h1>
          <p className="tagline">AI-Powered Resume Analysis & Job Matching</p>
        </div>
      </header>

      <div className="container">
        {/* Upload Section */}
        {!results && !loading && (
          <div className="upload-section">
            <div
              className={`upload-area ${dragging ? 'dragging' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => document.getElementById('file-input').click()}
            >
              <input
                id="file-input"
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                className="file-input"
              />
              <div className="upload-icon">📄</div>
              <div className="upload-text">
                <h3>Upload Your Resume</h3>
                <p>Drag & drop your PDF resume here, or click to browse</p>
                <p className="upload-hint">Maximum file size: 10MB</p>
              </div>
            </div>

            {file && (
              <div className="selected-file">
                <span className="file-icon">✓</span>
                <span className="file-name">{file.name}</span>
              </div>
            )}

            {error && <div className="error-message">{error}</div>}

            <button
              className="analyze-btn"
              onClick={handleAnalyze}
              disabled={!file || loading}
            >
              {loading ? 'Processing...' : 'Analyze Resume'}
            </button>
          </div>
        )}

        {/* Loading Section with Stages */}
        {loading && (
          <div className="loading-section">
            <div className="loading-card">
              <div className="loading-spinner">
                <div className="spinner-circle"></div>
              </div>
              <h3 className="loading-title">Processing Your Resume</h3>
              <p className="loading-stage">{loadingStage}</p>
              <div className="loading-bar">
                <div className="loading-progress"></div>
              </div>
            </div>
          </div>
        )}

        {/* Results Section */}
        {results && (
          <div className="results-section">
            {/* Analysis Summary */}
            <div className="summary-header">
              <h2 className="section-title">📊 Resume Analysis</h2>
              <button className="reset-btn" onClick={handleReset}>
                ← Analyze Another
              </button>
            </div>

            <div className="analysis-cards">
              {/* Skills Card */}
              <div className="info-card skills-card">
                <div className="card-header">
                  <h3>💡 Skills Identified</h3>
                  <span className="count-badge">{results.analysis.skills.length}</span>
                </div>
                <div className="card-content">
                  <div className="skills-grid">
                    {results.analysis.skills.map((skill, index) => (
                      <span key={index} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Suitable Roles Card */}
              <div className="info-card roles-card">
                <div className="card-header">
                  <h3>🎯 Suitable Roles</h3>
                  <span className="exp-badge">{results.analysis.experience_level}</span>
                </div>
                <div className="card-content">
                  <ul className="roles-list">
                    {results.analysis.suitable_roles.map((role, index) => (
                      <li key={index} className="role-item">
                        <span className="role-icon">💼</span>
                        {role}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Areas to Improve Card */}
              <div className="info-card improve-card">
                <div className="card-header">
                  <h3>📈 Areas to Improve</h3>
                  <span className="count-badge">{results.analysis.weaknesses.length}</span>
                </div>
                <div className="card-content">
                  <ul className="improve-list">
                    {results.analysis.weaknesses.map((weakness, index) => (
                      <li key={index} className="improve-item">
                        <span className="improve-icon">⚠️</span>
                        {weakness}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Jobs Section */}
            <div className="jobs-section">
              <div className="section-header">
                <h2 className="section-title">🚀 Matching Jobs & Internships</h2>
                <span className="jobs-count">{results.jobs.length} opportunities found</span>
              </div>

              {results.jobs.length > 0 ? (
                <div className="jobs-list">
                  {results.jobs.map((job, index) => (
                    <div key={index} className="job-card">
                      <div className="job-card-header">
                        <div className="job-info">
                          <h3 className="job-title">{job.title}</h3>
                          <p className="job-company">🏢 {job.company}</p>
                        </div>
                        <span className={`job-type-badge ${job.employment_type.toLowerCase()}`}>
                          {job.employment_type}
                        </span>
                      </div>
                      
                      <div className="job-meta">
                        <span className="job-location">📍 {job.location}</span>
                      </div>
                      
                      <p className="job-description">{job.description}</p>
                      
                      <a 
                        href={job.apply_link} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="apply-button"
                      >
                        Apply Now
                        <span className="arrow">→</span>
                      </a>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="no-jobs">
                  <p>No matching jobs found. Try updating your resume with more relevant keywords.</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
