import React, { useState, useEffect } from 'react';
import { wsClient } from './api/websocket';
import { useStore } from './store/useStore';
import { Zap } from 'lucide-react';

const PANELS = [
  'Interaction & Chat', 'Research Hub', 'Coding Studio', 'Computer Control',
  'File & Document', 'Image Engine', 'Video Studio', 'Audio Engine',
  'Business & ERP', 'Web & Browser', 'Memory & Learning', 'Tool & Repo Hub',
  'Workflow Automation', 'Security & OSINT', 'Permission Engine', 'Diagnostics & Logs',
  'Device Registry', 'Settings', 'Help & Knowledge', 'Auto-Upgrade Engine'
];

export function App() {
  const [activePanel, setActivePanel] = useState('Interaction & Chat');
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([
    { sender: 'System', text: 'AI Workspace OS connected to Python Event Bus via WebSocket.' }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [selectedMethodology, setSelectedMethodology] = useState('Standard');
  const [repoInput, setRepoInput] = useState('');
  const [toolsState, setToolsState] = useState<Record<string, boolean>>({
    openhands: true,
    crawl4ai: true,
    pyrit: false,
    stirling_pdf: true
  });

  const { agents, updateAgent } = useStore();

  useEffect(() => {
    wsClient.connect((data) => {
      console.log('Event Bus Message:', data);
      if (data.topic === 'agent_update') {
        updateAgent(data.payload.agentId, data.payload.status, data.payload.currentTask);
      }
    });

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'F1') {
        e.preventDefault();
        setActivePanel('Help & Knowledge');
      } else if (e.ctrlKey && e.key === 'f') {
        e.preventDefault();
        setActivePanel('Tool & Repo Hub');
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;
    const newMsg = { sender: 'User', text: '[' + selectedMethodology + '] ' + inputMessage };
    setMessages(prev => [...prev, newMsg]);
    wsClient.send('user_task_submitted', { task: inputMessage, methodology: selectedMethodology });
    setInputMessage('');
  };

  const toggleTool = (toolKey: string) => {
    setToolsState(prev => ({ ...prev, [toolKey]: !prev[toolKey] }));
  };

  const handleAutoUpgrade = () => {
    if (!repoInput.trim()) return;
    wsClient.send('trigger_upgrade', { repo_url: repoInput });
    setMessages(prev => [...prev, { sender: 'System', text: 'Initiated self-upgradation pipeline for: ' + repoInput }]);
    setRepoInput('');
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans overflow-hidden">
      <aside className="w-72 bg-slate-900 border-r border-slate-800 flex flex-col p-4 overflow-y-auto">
        <div className="flex items-center gap-3 text-sky-400 font-bold text-lg mb-6 px-2">
          <Zap className="w-6 h-6 animate-pulse" />
          <span>AI Workspace OS</span>
        </div>
        <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2 px-2">Command Center Panels</div>
        <div className="flex flex-col gap-1">
          {PANELS.map(panel => (
            <button
              key={panel}
              onClick={() => setActivePanel(panel)}
              className={'flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors text-left ' + (activePanel === panel ? 'bg-sky-500/10 text-sky-400 font-medium border border-sky-500/25' : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200')}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-current opacity-75"></span>
              {panel}
            </button>
          ))}
        </div>
      </aside>

      <main className="flex-1 flex flex-col bg-slate-950 overflow-hidden">
        <header className="h-16 border-b border-slate-800 flex items-center justify-between px-6 bg-slate-900/50 backdrop-blur">
          <h1 className="text-lg font-semibold text-slate-200">{activePanel}</h1>
          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
              Event Bus Active (Port 8000)
            </span>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-6">
          {activePanel === 'Interaction & Chat' && (
            <div className="max-w-4xl mx-auto h-full flex flex-col gap-4">
              <div className="flex-1 bg-slate-900/60 border border-slate-800 rounded-xl p-4 overflow-y-auto flex flex-col gap-3">
                {messages.map((m, idx) => (
                  <div key={idx} className={'p-3 rounded-lg max-w-[80%] ' + (m.sender === 'User' ? 'ml-auto bg-sky-600 text-white' : 'mr-auto bg-slate-800 text-slate-200')}>
                    <div className="text-xs opacity-70 mb-1">{m.sender}</div>
                    <div className="text-sm whitespace-pre-wrap">{m.text}</div>
                  </div>
                ))}
              </div>
              <div className="flex flex-col gap-2 bg-slate-900 border border-slate-800 p-3 rounded-xl">
                <div className="flex items-center justify-between">
                  <select
                    value={selectedMethodology}
                    onChange={(e) => setSelectedMethodology(e.target.value)}
                    className="bg-slate-950 border border-slate-700 text-xs text-slate-300 rounded px-2 py-1 outline-none"
                  >
                    <option value="Standard">Methodology: Standard Execution</option>
                    <option value="Understand Like a Genius">Understand Like a Genius</option>
                    <option value="Master Any Skill">Master Any Skill for Free</option>
                    <option value="Fix Mental Blocks">Fix Mental Blocks</option>
                    <option value="PhD-Level Breakdown">PhD-Level Breakdown</option>
                  </select>
                </div>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Enter command, query, or coding task (Press Enter to execute)..."
                    className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-100 outline-none focus:border-sky-500"
                  />
                  <button onClick={handleSendMessage} className="bg-sky-500 hover:bg-sky-400 text-slate-950 font-semibold px-5 py-2 rounded-lg text-sm transition-colors">
                    Execute
                  </button>
                </div>
              </div>
            </div>
          )}

          {activePanel === 'Tool & Repo Hub' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-5xl mx-auto">
              {Object.entries(toolsState).map(([tool, enabled]) => (
                <div key={tool} className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-slate-200 capitalize">{tool.replace('_', ' ')}</h3>
                    <p className="text-xs text-slate-400">Integrated autonomous capability runner.</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" checked={enabled} onChange={() => toggleTool(tool)} className="sr-only peer" />
                    <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-sky-500"></div>
                  </label>
                </div>
              ))}
            </div>
          )}

          {activePanel === 'Auto-Upgrade Engine' && (
            <div className="max-w-2xl mx-auto bg-slate-900 border border-slate-800 p-6 rounded-xl flex flex-col gap-4">
              <h3 className="font-semibold text-slate-200">Self-Upgradation & Repository Ingestion</h3>
              <p className="text-xs text-slate-400">Paste any GitHub repository URL or package name below. The autonomous pipeline will ingest, sandbox test, and register the tool.</p>
              <input
                type="text"
                value={repoInput}
                onChange={(e) => setRepoInput(e.target.value)}
                placeholder="https://github.com/organization/repository"
                className="bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-100 outline-none focus:border-sky-500"
              />
              <button onClick={handleAutoUpgrade} className="bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-2 rounded-lg text-sm transition-colors">
                Auto-Incorporate Repository
              </button>
            </div>
          )}

          {!['Interaction & Chat', 'Tool & Repo Hub', 'Auto-Upgrade Engine'].includes(activePanel) && (
            <div className="max-w-3xl mx-auto bg-slate-900 border border-slate-800 p-6 rounded-xl">
              <h3 className="font-semibold text-slate-200 mb-2">{activePanel} Workspace</h3>
              <p className="text-sm text-slate-400">Panel operational and synchronized with the PyPubSub Event Bus and Permission Engine.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
