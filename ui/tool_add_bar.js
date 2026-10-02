(function() {
  'use strict';
  const API = window.location.origin;

  function findToolPanel() {
    // Find by heading text
    const headings = Array.from(document.querySelectorAll('h1, h2, h3, [class*="title"]'));
    const toolHeading = headings.find(h => /tool\s*hub/i.test(h.textContent));
    if (!toolHeading) return null;
    // Return the panel container (parent)
    let el = toolHeading;
    for (let i = 0; i < 5; i++) { if (el.parentElement) el = el.parentElement; else break; }
    return el;
  }

  function injectAddBar() {
    const panel = findToolPanel();
    if (!panel || panel.querySelector('.ws-add-tool-bar')) return;

    const bar = document.createElement('div');
    bar.className = 'ws-add-tool-bar';
    bar.style.cssText = 'background:#0f172a;border:1px solid #334155;border-radius:8px;padding:14px;margin:14px 0;';
    bar.innerHTML =
      '<div style="font-weight:600;color:#e2e8f0;margin-bottom:8px;">➕ Add Repository / Tool</div>' +
      '<div style="display:flex;gap:8px;flex-wrap:wrap;">' +
        '<input id="ws-tool-url" type="text" placeholder="https://github.com/user/repo" ' +
          'style="flex:1;min-width:260px;padding:8px 10px;border-radius:6px;border:1px solid #334155;background:#1e293b;color:#e2e8f0;">' +
        '<button id="ws-tool-add-btn" style="background:#10b981;color:white;border:0;border-radius:6px;padding:8px 16px;cursor:pointer;">Add</button>' +
        '<button id="ws-tool-list-btn" style="background:#334155;color:#e2e8f0;border:0;border-radius:6px;padding:8px 16px;cursor:pointer;">Refresh List</button>' +
      '</div>' +
      '<div id="ws-tool-status" style="margin-top:10px;color:#94a3b8;font-size:13px;"></div>' +
      '<div id="ws-tool-list" style="margin-top:10px;color:#cbd5e1;font-size:13px;"></div>';

    panel.insertBefore(bar, panel.firstChild.nextSibling);

    const urlIn = document.getElementById('ws-tool-url');
    const status = document.getElementById('ws-tool-status');
    const list = document.getElementById('ws-tool-list');

    document.getElementById('ws-tool-add-btn').onclick = async () => {
      const url = urlIn.value.trim();
      if (!url) { status.textContent = 'Enter a URL.'; return; }
      status.textContent = 'Cloning and registering...';
      try {
        const r = await fetch(API + '/api/tools/add', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ url })
        });
        const d = await r.json();
        status.textContent = 'Status: ' + d.status + (d.detail ? ' — ' + d.detail : '') + (d.tool ? ' (' + d.tool.name + ')' : '');
        urlIn.value = '';
        refreshList();
      } catch (e) { status.textContent = 'Error: ' + e.message; }
    };

    document.getElementById('ws-tool-list-btn').onclick = refreshList;

    async function refreshList() {
      try {
        const r = await fetch(API + '/api/tools/list');
        const d = await r.json();
        if (!d.tools || d.tools.length === 0) {
          list.innerHTML = '<em>No tools registered yet.</em>';
          return;
        }
        list.innerHTML = d.tools.map(t =>
          '<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1e293b;">' +
            '<span>🧩 <b>' + t.name + '</b> — <span style="color:#94a3b8">' + t.status + '</span></span>' +
            '<button data-name="' + t.name + '" class="ws-remove-tool" ' +
              'style="background:#7f1d1d;color:#fecaca;border:0;border-radius:5px;padding:3px 10px;cursor:pointer;font-size:12px;">Remove</button>' +
          '</div>'
        ).join('');
        list.querySelectorAll('.ws-remove-tool').forEach(b => {
          b.onclick = async () => {
            const name = b.dataset.name;
            if (!confirm('Remove ' + name + ' from registry?')) return;
            await fetch(API + '/api/tools/remove', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({ name, delete_files: false })
            });
            refreshList();
          };
        });
      } catch (e) { list.textContent = 'Error: ' + e.message; }
    }

    refreshList();
  }

  const obs = new MutationObserver(() => setTimeout(injectAddBar, 400));
  function boot() {
    obs.observe(document.body, { childList: true, subtree: true });
    setTimeout(injectAddBar, 800);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
