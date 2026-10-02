(function() {
  'use strict';
  const API = window.location.origin;

  window.wsToast = function(msg, type) {
    const t = document.createElement('div');
    t.textContent = msg;
    t.style.cssText = 'position:fixed;top:20px;right:20px;z-index:99999;background:' +
      (type === 'error' ? '#dc2626' : '#10b981') +
      ';color:white;padding:12px 20px;border-radius:8px;font-family:system-ui;box-shadow:0 10px 25px rgba(0,0,0,0.3);transition:opacity 0.3s;';
    document.body.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; setTimeout(() => t.remove(), 300); }, 2500);
  };

  window.wsSave = async function(content, name) {
    try {
      const r = await fetch(API + '/api/output/save', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ content, name: name || ('output_' + Date.now()) })
      });
      const d = await r.json();
      if (d.status === 'saved') { wsToast('Saved: ' + d.filename); return d; }
      wsToast('Save failed', 'error');
    } catch (e) { wsToast('Save error: ' + e.message, 'error'); }
  };

  window.wsDownload = function(content, name) {
    let blob;
    if (content.startsWith('data:')) {
      const parts = content.split(';base64,');
      const mime = parts[0].split(':')[1];
      const binary = atob(parts[1]);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
      blob = new Blob([bytes], { type: mime });
      if (!name) name = 'download_' + Date.now() + '.' + mime.split('/')[1];
    } else {
      blob = new Blob([content], { type: 'text/plain' });
      if (!name) name = 'download_' + Date.now() + '.txt';
    }
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    wsToast('Downloaded: ' + name);
  };

  function mkBtn(label, title, color, handler) {
    const b = document.createElement('button');
    b.textContent = label;
    b.title = title;
    b.style.cssText = 'background:' + color + ';color:#e2e8f0;border:1px solid #475569;' +
      'border-radius:6px;padding:4px 10px;font-size:12px;cursor:pointer;margin-right:6px;';
    b.onclick = handler;
    b.onmouseover = () => b.style.opacity = '0.8';
    b.onmouseout = () => b.style.opacity = '1';
    return b;
  }

  function attachToolbar(container) {
    if (container.dataset.wsToolbar || container.tagName !== 'DIV') return;
    const text = (container.innerText || '').trim();
    if (text.length < 20) return;
    container.dataset.wsToolbar = '1';

    const bar = document.createElement('div');
    bar.className = 'ws-toolbar';
    bar.style.cssText = 'display:flex;gap:0;margin:8px 0;flex-wrap:wrap;';

    const getContent = () => container.dataset.rawContent || container.innerText || '';

    bar.appendChild(mkBtn('📋 Copy', 'Copy to clipboard', '#334155', async () => {
      try {
        await navigator.clipboard.writeText(getContent());
        wsToast('Copied to clipboard');
      } catch(e) { wsToast('Copy failed', 'error'); }
    }));
    bar.appendChild(mkBtn('💾 Save', 'Save on server', '#1e40af', async () => {
      const name = prompt('Save as (no extension):', 'output_' + Date.now());
      if (name) await wsSave(getContent(), name);
    }));
    bar.appendChild(mkBtn('⬇️ Download', 'Download to computer', '#166534', () => {
      const name = prompt('Download as:', 'download_' + Date.now() + '.txt');
      if (name) wsDownload(getContent(), name);
    }));
    bar.appendChild(mkBtn('🔄 Refresh', 'Reload panel', '#7c2d12', () => location.reload()));
    bar.appendChild(mkBtn('✖️ Clear', 'Clear output', '#7f1d1d', () => {
      container.innerHTML = '';
      container.dataset.rawContent = '';
      container.dataset.wsToolbar = '';
    }));

    container.parentNode.insertBefore(bar, container);
  }

  function scanToolbars() {
    const sels = ['.output-box', '.result-box', '.response-box',
                  '[data-output]', '[class*="output"]', '[class*="result"]', '[class*="response"]'];
    sels.forEach(sel => {
      document.querySelectorAll(sel).forEach(el => {
        if (el.tagName === 'DIV' && !el.dataset.wsToolbar) attachToolbar(el);
      });
    });
  }

  function enableDragDrop() {
    document.querySelectorAll('input[type="text"], textarea').forEach(el => {
      if (el.dataset.wsDd) return;
      el.dataset.wsDd = '1';
      el.addEventListener('dragover', e => { e.preventDefault(); el.style.outline = '2px solid #3b82f6'; });
      el.addEventListener('dragleave', () => el.style.outline = '');
      el.addEventListener('drop', async e => {
        e.preventDefault();
        el.style.outline = '';
        const text = e.dataTransfer.getData('text');
        const file = e.dataTransfer.files[0];
        if (text) { el.value = text; wsToast('URL/text dropped'); return; }
        if (file) {
          const reader = new FileReader();
          reader.onload = ev => {
            el.value = ev.target.result;
            wsToast(file.type.startsWith('image/') ? 'Image loaded as base64' : 'File loaded as text');
          };
          if (file.type.startsWith('image/')) reader.readAsDataURL(file);
          else reader.readAsText(file);
        }
      });
    });
  }

  function addHelpIcons() {
    document.querySelectorAll('h1, h2, h3, .panel-title, [class*="panel-title"], [class*="header"]').forEach(h => {
      if (h.dataset.wsHelp || h.tagName.match(/^(INPUT|BUTTON)$/)) return;
      h.dataset.wsHelp = '1';
      const i = document.createElement('span');
      i.textContent = ' ⓘ';
      i.title = 'Click for panel help';
      i.style.cssText = 'margin-left:8px;cursor:help;opacity:0.55;font-size:13px;';
      i.onclick = () => alert(
        'PANEL HELP\n\n' +
        '📋 Copy — copy output to clipboard\n' +
        '💾 Save — save output on server (storage_outputs/)\n' +
        '⬇️ Download — download output to your computer\n' +
        '🔄 Refresh — reload this panel\n' +
        '✖️ Clear — clear this output\n\n' +
        'DRAG & DROP: drop URLs, text files, or images\n' +
        'into any input field to auto-fill it.\n\n' +
        'KEYBOARD: Enter = submit · Esc = cancel · F1 = help'
      );
      h.appendChild(i);
    });
  }

  const observer = new MutationObserver(() => {
    setTimeout(() => { scanToolbars(); enableDragDrop(); addHelpIcons(); }, 250);
  });

  function boot() {
    observer.observe(document.body, { childList: true, subtree: true });
    setTimeout(() => { scanToolbars(); enableDragDrop(); addHelpIcons(); }, 600);
    console.log('[AI-Workspace] Universal toolbar + drag-drop + help icons active');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
