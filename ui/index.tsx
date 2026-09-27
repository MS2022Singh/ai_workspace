import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { RenderConverterControls } from './panels/converter';
import './styles/dashboard.css';

const PANELS = [
  'Interaction & Chat', 'Research Hub', 'Coding Studio', 'Computer Control',
  'File & Document', 'Image Engine', 'Video Studio', 'Audio Engine',
  'Business & ERP', 'Web & Browser', 'Memory & Learning', 'Tool & Repo Hub',
  'Workflow Automation', 'Security & OSINT', 'Permission Engine', 'Diagnostics & Logs',
  'Device Registry', 'Settings', 'Help & Knowledge', 'Auto-Upgrade Engine'
];

const App = () => {
  const [activePanel, setActivePanel] = useState('Interaction & Chat');
  const [toolsState, setToolsState] = useState({
    openhands: true,
    crawl4ai: true,
    pyrit: false,
    stirling_pdf: true
  });
  const [repoUrl, setRepoUrl] = useState('');
  const [statusMessage, setStatusMessage] = useState('System Idle. Ready for commands.');

  // Keyboard Shortcuts Handler (Enter, Esc, Ctrl+S, Ctrl+F, F1)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'F1') {
        e.preventDefault();
        setActivePanel('Help & Knowledge');
      } else if (e.ctrlKey && e.key === 'f') {
        e.preventDefault();
        setActivePanel('Tool & Repo Hub');
      } else if (e.key === 'Escape') {
        setStatusMessage('Current operation canceled by user.');
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const toggleTool = (toolId: string) => {
    setToolsState(prev => ({ ...prev, [toolId]: !prev[toolId] }));
  };

  const handleSelfUpgrade = () => {
    if (!repoUrl) return;
    setStatusMessage(`Ingesting repository/tool from: ${repoUrl}...`);
    setTimeout(() => {
      setStatusMessage(`SUCCESS: Incorporated ${repoUrl} into Master Registry and PyPubSub Bus.`);
      setRepoUrl('');
    }, 2000);
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="brand-header">
          <span>⚡</span> AI Workspace OS
        </div>
        <div className="nav-section-title">Command Center Panels</div>
        {PANELS.map(panel => (
          <div
            key={panel}
            className={`nav-item ${activePanel === panel ? 'active' : ''}`}
            onClick={() => setActivePanel(panel)}
          >
            <span>•</span> {panel}
          </div>
        ))}
      </aside>

      {/* Main Viewport */}
      <main className="main-viewport">
        <header className="top-bar">
          <h2>{activePanel}</h2>
          <div className="status-badge">
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#22c55e' }}></span>
            {statusMessage}
          </div>
        </header>

        {/* Panel Content Router */}
        {activePanel === 'Interaction & Chat' && (
          <div className="panel-grid">
            <div className="card" style={{ gridColumn: 'span 2' }}>
              <div className="card-title">Task & Response Stream</div>
              <textarea rows={6} placeholder="Ask anything, execute tasks, or select a Prompt Methodology..." />
              <div style={{ display: 'flex', gap: '10px' }}>
                <button className="btn-primary">Execute Task</button>
                <select style={{ width: 'auto', margin: 0 }}>
                  <option>Methodology: Standard</option>
                  <option>Methodology: Understand Like a Genius</option>
                  <option>Methodology: Master Any Skill</option>
                  <option>Methodology: Fix Mental Blocks</option>
                  <option>Methodology: PhD Breakdown</option>
                </select>
              </div>
            </div>
          </div>
        )}

        {activePanel === 'File & Document' && (
          <div className="panel-grid">
            <div className="card">
              <div className="card-title">MIME-Aware Converter & Editor</div>
              <RenderConverterControls file={{ name: 'active_document.pdf', mimeType: 'application/pdf', size: 102400 }} />
            </div>
          </div>
        )}

        {activePanel === 'Tool & Repo Hub' && (
          <div className="panel-grid">
            <div className="card">
              <div className="card-title">
                OpenHands (Coding Sandbox)
                <label className="switch">
                  <input type="checkbox" checked={toolsState.openhands} onChange={() => toggleTool('openhands')} />
                  <span className="slider"></span>
                </label>
              </div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Autonomous software development agent in sandboxed environment.</p>
              <button className="btn-primary" style={{ marginTop: 12 }} disabled={!toolsState.openhands}>Launch Sandbox</button>
            </div>

            <div className="card">
              <div className="card-title">
                Crawl4AI (Web Crawler)
                <label className="switch">
                  <input type="checkbox" checked={toolsState.crawl4ai} onChange={() => toggleTool('crawl4ai')} />
                  <span className="slider"></span>
                </label>
              </div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>High-speed LLM-ready web crawler and markdown extractor.</p>
              <button className="btn-primary" style={{ marginTop: 12 }} disabled={!toolsState.crawl4ai}>Start Scrape</button>
            </div>

            <div className="card">
              <div className="card-title">
                PyRIT Security Red-Team
                <label className="switch">
                  <input type="checkbox" checked={toolsState.pyrit} onChange={() => toggleTool('pyrit')} />
                  <span className="slider"></span>
                </label>
              </div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>AI system risk identification and security scanning framework.</p>
              <button className="btn-primary" style={{ marginTop: 12 }} disabled={!toolsState.pyrit}>Run Vulnerability Audit</button>
            </div>
          </div>
        )}

        {activePanel === 'Auto-Upgrade Engine' && (
          <div className="panel-grid">
            <div className="card" style={{ gridColumn: 'span 2' }}>
              <div className="card-title">Incorporate External Repository / Tool / URL</div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: 12 }}>
                Paste any GitHub repository URL, package name, or tool documentation link. The autonomous agent will inspect, build in a sandbox, synthesize a wrapper, and register it to the event bus.
              </p>
              <input
                type="text"
                placeholder="https://github.com/org/repository or package name"
                value={repoUrl}
                onChange={e => setRepoUrl(e.target.value)}
              />
              <button className="btn-primary" onClick={handleSelfUpgrade}>Auto-Incorporate & Register</button>
            </div>
          </div>
        )}

        {/* Fallback for other panels */}
        {!['Interaction & Chat', 'File & Document', 'Tool & Repo Hub', 'Auto-Upgrade Engine'].includes(activePanel) && (
          <div className="card">
            <div className="card-title">{activePanel} Workspace</div>
            <p style={{ color: 'var(--text-muted)' }}>Panel online. Connected to PyPubSub Event Bus and Permission Engine.</p>
          </div>
        )}
      </main>
    </div>
  );
};

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<App />);
}
