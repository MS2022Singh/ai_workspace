# AI Workspace

A private, local "AI team" for coding, debugging, documentation, research,
analysis, writing, and more. It runs entirely on your Windows PC using
**free, local AI models** (via [Ollama](https://ollama.com)) — nothing you
type or generate is sent to any cloud service by default. Tasks run in the
background, in a multi-agent pipeline:

```
You → Coordinator (plans the work, picks the right teammates)
        ├─ Coder            ├─ Researcher
        ├─ Reviewer         ├─ Analyst
        ├─ Documenter       ├─ Economist
        ├─ Proofreader      ├─ Writer
                             ├─ Historian
                             ├─ Archaeologist
                             ├─ Scientist
                             └─ Engineer
```

Every role is a generalist, not a narrow specialist — the Historian isn't
limited to one century, the Coder isn't limited to one language. The
Coordinator picks whichever teammates actually fit the task — only the ones
genuinely needed, not the whole roster every time — whether that's "build
me a script" or "explain the economics of the 1929 crash."

If none of the fixed team members are the right fit — say, a task needs
music/audio expertise, or law, medicine, or some other niche field — the
Coordinator can invent a one-off specialist on the spot (e.g. "Audio
Engineer," "Patent Attorney") instead of forcing a poor match. These don't
show up in the permanent roster (they're created per-task), but you'll see
them by name in that task's activity log. There's a "Specialist" model
setting in Settings that's used for whichever ad hoc expert gets invented.

Multiple projects, multiple tasks per project, and several tasks can run
concurrently in the background while you keep using the app (or do
something else on your PC) — queued tasks pick up automatically.

---

## 1. One-time setup (about 10–15 minutes)

### Step 1 — Install Python
If you don't already have it: install **Python 3.10+** from
https://python.org/downloads (tick "Add Python to PATH" during install).

### Step 2 — Install Ollama (the free local AI engine)
Download and install from **https://ollama.com/download/windows**.
This installs a background service that runs AI models entirely on your
own machine — no account, no API key, no data leaves your PC.

### Step 3 — Download at least one model
Open Command Prompt and run:

```
ollama pull llama3.2:3b
ollama pull qwen2.5-coder:7b
```

- `llama3.2:3b` — small, fast, good for planning/docs/proofreading even on CPU-only laptops. Used as the default for every knowledge role (Researcher, Analyst, Economist, Writer, Historian, Archaeologist, Scientist, Engineer) too.
- `qwen2.5-coder:7b` — a strong free coding model, used for the Coder/Reviewer roles.

For better depth on research/analysis/writing tasks, you can optionally also pull a stronger generalist model and assign it to those roles in Settings:
```
ollama pull qwen2.5:7b
```

If you want to attach images and have the team describe/use them, also pull a vision model (used by the "Vision" role):
```
ollama pull llava
```

**Retrying a task** — if a task fails (e.g. a model wasn't pulled yet) or
you just want to run it again, click "🔁 Retry" on it. It reuses the exact
same description and attachments — no need to retype the prompt or
re-upload anything.

**Editing a task** — click "✏️ Edit & retry" on a finished task to change
its description in place and run it again, without losing its attachments.

**Continuing a conversation** — every finished task has a "Continue this
conversation" box at the bottom. Use it to ask a follow-up or request a
change; the team keeps the context from the original task (and anything
already discussed) instead of starting from scratch.

**Copying & downloading responses** — every team response has a
"📋 Copy" button, and the task as a whole has "📋 Copy full transcript" and
"⬇ Download transcript (.txt)" at the top.

**Deleting** — hover the "×" on any task or project in the sidebar/list to
remove it (and everything in it) permanently. Handy for clearing out test
runs.

**Not sure if you have a GPU, or these feel slow?** Swap to smaller models —
`qwen2.5-coder:1.5b` and `llama3.2:1b` — they run fine on CPU-only machines,
just with somewhat lower quality. You can change the model assigned to each
role any time in the app's Settings panel, with no need to edit code.

### Step 4 — Install this app's dependencies
Double-click **`run.bat`** in this folder. The first run will:
- create a private Python virtual environment (`venv/`) inside this folder,
- install the required packages,
- launch the app window.

(If Windows blocks the script, right-click `run.bat` → Properties → Unblock.)

### Step 5 — Add a desktop icon (optional, recommended)
After `run.bat` has successfully launched the app at least once, double-click
**`Create Desktop Shortcut.bat`**. This adds an **"AI Workspace"** icon to
your Desktop. From now on, just double-click that icon — no console window,
no need to open `run.bat` again. (Only re-run `run.bat` if you change/add
dependencies, or delete `venv`.)

Want a fully standalone app (its own name and icon in the Task Manager,
no trace of "python" anywhere)? Run **`Build Standalone App.bat`** once —
it produces `dist\AI Workspace\AI Workspace.exe`, which you can pin to
your taskbar or Start menu like any other program.

---

## 2. Using it on your phone too

The phone doesn't run any AI itself — your PC keeps doing all the work.
Your phone just opens the same dashboard over your home WiFi, like a remote
screen for it.

1. In the app, open **Settings → Mobile access** and turn on
   *"Allow access from other devices on this network"*.
2. It'll show you a URL like `http://192.168.1.42:8765/?code=123456` —
   open that in your phone's browser (Chrome/Safari) while your phone is on
   the **same WiFi network** as the PC.
3. Add it to your phone's home screen for an app-like icon: in the browser's
   share/menu, choose "Add to Home Screen".

This is off by default, and even when on, a device needs the access code
shown in Settings to get in — simply being on the same WiFi isn't enough.
This only works on your local network; it does not expose the app to the
internet, and the PC needs to stay turned on and running the app for your
phone to reach it. True on-device mobile AI (running models on the phone
itself, fully offline) isn't practical yet with free local models at
usable quality — this LAN approach is the practical middle ground.

**If your phone says "the site can't be reached":** that's almost always
Windows Firewall blocking *incoming* connections from other devices (a
different thing from any outbound restrictions) — by default it only
allows this automatically on networks marked "Private." Fix it in order:

1. Make sure your WiFi network is set to **Private**, not Public: Windows
   Settings → Network & Internet → WiFi → click your network → Network
   profile type → **Private**.
2. Run **`Allow Mobile Access (run as admin).bat`** once (it'll ask for
   admin permission) — this opens the right port through Windows Firewall.
3. Restart the app, then **test from the PC itself first**: open a normal
   browser on the PC and visit the exact URL Settings shows you (the
   `192.168.x.x` one, not `127.0.0.1`). If that doesn't load either, the
   problem is confirmed to be the firewall/network, not your phone.
4. Still stuck, and this is a work/managed laptop? A separate
   security product (not Windows Firewall) may be blocking it, and IT
   may need to add an exception.

---

## 3. Using it

1. Click **+** next to "Projects" to create a project (e.g. "Inventory App").
2. Type a task in the box, e.g.:
   > Build a Python CLI that converts CSV to JSON, with unit tests and a README.
3. Click **Assign to team**. Watch the **Team** panel light up as each role
   works, and the task move from `queued` → `running` → `done`.
4. Generated files appear as chips on the task and are saved for real on disk at:
   ```
   C:\Users\<you>\.ai_workspace\projects\<project_id>\task_<task_id>\
   ```
5. Submit more tasks any time — they queue up and run in the background
   (default: 2 at once) even while you keep working in other tasks/projects.

### Settings
- **Background concurrency** — how many tasks run at once. Higher = faster
  throughput but more CPU/RAM load. Start at 1–2 on a laptop.
- **Encrypt stored task data at rest** — encrypts everything written to the
  local database file using a key stored only on your machine.
- **Model per role** — assign any locally-installed Ollama model to each
  team role independently.

---

## 4. Privacy & security, in plain terms

- **No cloud calls, with one explicit, opt-in exception.** By default, the
  only network request this app ever makes is to `localhost:11434` (your
  own Ollama installation). If you turn on **Settings → "Allow live web
  research"**, the Researcher/Analyst/Economist/Scientist roles can send
  the specific search text for a step to a search engine, so they can
  answer questions about current events or fields beyond their training
  data. This is **off by default**, and even when on, only that short
  search query leaves your machine — not your task description, files, or
  anything else. Turn it off any time in Settings.
- **Voice input** also stays fully local — it uses an offline speech model
  on your own PC, never a cloud speech service, and your voice is never
  transmitted anywhere. **Read-aloud** uses your operating system's own
  built-in voice and likewise never leaves your machine.
- **No accounts, no telemetry, no analytics.**
- **All data stays on disk on your machine**, under `~\.ai_workspace\`:
  - `workspace.db` — projects, tasks, agent activity logs
  - `projects\` — the actual generated files, as plain files you can open
  - `local.key` — only present/used if you turn on at-rest encryption
- **Optional at-rest encryption** protects the database file itself (handy
  if this machine is backed up to cloud sync, or shared with others) — this
  is separate from, and in addition to, the "no data leaves the machine"
  guarantee above.

---

## 5. Multitasking & background completion

- A scheduler thread inside the app continuously looks for queued tasks and
  runs them on a background thread pool, independent of which task/project
  you're currently looking at in the UI.
- You can submit a task, switch to a different project, submit another task,
  and both will progress in the background — the task list polls live status.
- If you close the app while a task is mid-run, that task resumes from a
  clean state next time you start the app (it goes back to `queued` and
  reruns automatically — partial output before that point isn't reused, to
  keep the pipeline simple and reliable).

---

## 6. Attaching files & downloading results

**Attach reference files to a task** — click "📎 Attach files" in the task
box before assigning it to the team. Supported formats the team can
actually *read*: `.txt .md .py .js .json .csv .html .css .yaml .xml` and
similar code/text files, plus `.pdf`, `.docx`, and `.xlsx`. Other formats
(images, etc.) are still saved alongside the task, but the team will only
see the filename, not the contents — there's a note in the activity log
when that happens.

**Download what the team produces** — every file chip under "Files
produced" on a task is a direct download link. If a task produced more
than one file, a "Download all (.zip)" link appears too. Ask for a
`.docx`, `.xlsx`, or `.pptx` and you'll get a real Word/Excel/PowerPoint
file, not a text file with that extension slapped on — see "Generating
real Office documents" below.

You don't need to create a project before assigning a task — one ("General")
is created for you automatically the first time. Projects are just there if
you want to organize separate efforts later (click "+" to add more).

**Images** — attach a `.png/.jpg/.gif/.webp/.bmp` and the team can actually
*see* it: a Vision step automatically describes it first (using a separate
vision-capable model), and that description gets handed to everyone else,
since the rest of the team works in text. One-time setup:
```
ollama pull llava
```
(or a lighter option: `ollama pull moondream`, then set it as the Vision
model in Settings). Without a vision model pulled, attaching an image still
works, but the team will tell you it can't analyze it instead of guessing.

## 7. Voice input & read-aloud

**🎤 Voice** (next to "Attach files") lets you speak a task instead of
typing it. Click it, talk, click it again to stop — your speech is
transcribed and dropped into the task box for you to review/edit before
sending. This uses a small, completely offline speech model that runs on
your PC; your voice is never sent anywhere, including to Google or any
cloud speech service (which is what the browser's *built-in* voice input
would otherwise do — deliberately avoided here for that reason).

One-time setup: run **`Download Speech Model.bat`** once (~50MB, free).
Until you do, clicking 🎤 will tell you it's missing instead of failing
silently.

**🔊 Read aloud** on any team-activity entry reads that response out loud
using your operating system's own built-in voice — also fully local, no
network call involved.

**🔁 Conversation mode** turns the two features above into an actual back-
and-forth: turn it on, then use 🎤 Voice — your spoken task is transcribed
*and sent automatically* (no need to click "Assign to team"), and once the
team finishes, the final result is read back to you automatically too.
Turn it off any time to go back to manual control.

---

## 8. Optional: a fully standalone app, no Python window at all

`Build Standalone App.bat` packages everything into a real `.exe` with
its own icon and its own name in the Task Manager — no "python.exe"
anywhere:

```
dist\AI Workspace\AI Workspace.exe
```

Pin that to your taskbar or Start menu. (Run it once from `run.bat` first
so the `venv` exists, then run `Build Standalone App.bat`.)

---

## 9. Generating real Office documents

Ask for a deliverable ending in `.docx`, `.xlsx`, or `.pptx` (e.g. "write
this up as a Word document," "put this data in a spreadsheet," "make a
PowerPoint summary") and the file you get back is a genuine native Office
file — opens correctly in Word/Excel/PowerPoint, not a text file wearing
that extension.

**What it can do**: clean headings, bullet/numbered lists, and paragraphs
in Word docs; multi-sheet spreadsheets with real cells in Excel; one slide
per section with a title and bullets in PowerPoint.

**What it can't do**: reproduce complex original formatting from a file
you uploaded (fonts, colors, exact layout, embedded images/charts, merged
cells). If you upload a heavily-formatted `.docx` and ask for edits, you'll
get a new, cleanly-formatted document with the corrected content — not
that same file with your original styling preserved. If pixel-perfect
fidelity to an original document matters, treat this as a strong first
draft to finish in Word/Excel/PowerPoint yourself.

## 10. Media tools (image editing, collage splitting, logos, slideshows)

Click **🎨 Media Tools** at the top to switch out of the team-chat view.
These are direct, instant tools (no AI model, no waiting on a model
response) — plain local image processing:

- **Split a collage** — upload a grid-style image (e.g. a contact sheet or
  collage of equal tiles), tell it how many rows/columns, and download
  each tile as its own file in a `.zip`. Works best on a regular,
  even grid; very irregular/overlapping collages won't split cleanly with
  this tool.
- **Edit an image** — resize, crop, rotate, flip, grayscale, blur, sharpen,
  brightness/contrast, and format conversion (PNG/JPEG/WEBP/BMP).
- **Generate a logo** — a clean templated logo (accent mark + your text)
  in a few color styles. This is a designed template, not a creative AI
  generator — good for quick placeholders, not a replacement for a
  designer.
- **Make a slideshow/reel** — combine several images into a GIF (always
  works) or MP4 (needs one optional one-time install: run
  **`Install Media Tools (optional).bat`** once).

**What this section deliberately does not include**: real AI-generated
images or video from a text description (e.g. "generate a photo of..." or
"make a video of..."). Genuine local image generation (Stable-Diffusion-
style) is possible but needs a multi-gigabyte model download and is slow
without a dedicated GPU; genuine local video generation from text isn't
realistically achievable yet on typical consumer hardware for free. If you
want AI image generation added as a clearly-optional, separate install
despite the size/speed trade-off, that can be added — just ask.

## 11. Troubleshooting

- **"Ollama not detected" in the sidebar** — make sure Ollama is installed
  and running (it usually starts automatically; you can verify by opening
  http://localhost:11434 in a browser — it should say "Ollama is running").
- **Settings shows no models** — run `ollama pull llama3.2:3b` in a terminal,
  then reopen Settings.
- **Tasks stay "queued" forever** — check the concurrency setting isn't 0,
  and that Ollama is actually running.
- **A role's output looks like garbage / didn't follow the format** — smaller
  models occasionally ignore formatting instructions. Try a slightly larger
  model for that role in Settings, or simply re-submit the task.
- **Phone can't reach the app** — confirm the phone is on the *same WiFi*
  as the PC (not mobile data), that Mobile access is turned on in Settings,
  and that the URL includes `?code=...`. Some public/office WiFi networks
  block devices from seeing each other ("AP isolation") — a home network
  usually works fine.
- **Windows Firewall pops up the first time you enable Mobile access** —
  check "Private networks" only (leave "Public networks" unchecked), then
  click Allow; this just lets other devices on your own WiFi reach the app.
- **"AI Workspace couldn't start" with a generic timeout message** — the
  app now bypasses any system-wide network proxy for its own local
  traffic (common on managed/corporate Windows machines that can otherwise
  silently stall `127.0.0.1` requests). If you still see this, check
  Task Manager for a leftover `pythonw.exe` process from a previous run
  and end it, then try again — the most common other cause is a stale
  process still holding the port.
- **"A task fails with "404 ... model not found"** — that exact model isn't
  pulled yet on this machine. Run `ollama pull <model name>` (the error
  message tells you the exact name), or change that role's model in
  Settings to one you've already pulled.
- **Downloads / Read aloud didn't seem to do anything** — downloads now
  show a native "Save As" dialog (look for it, it can appear behind the
  main window) instead of silently saving somewhere; if no dialog
  appeared, the actual error now shows in the red banner at the top
  instead of failing silently. Read-aloud now tells you directly if no
  system voice was available rather than doing nothing.
- **Editing a task description used to get wiped out while typing** —
  fixed; the panel no longer auto-refreshes out from under you while a
  text box in it has focus.
- **Buttons/Settings seem to do nothing, but the page itself loads** — this
  usually means Windows fell back to an old, limited browser engine instead
  of the modern one. Install the **Microsoft Edge WebView2 Runtime** from
  https://developer.microsoft.com/microsoft-edge/webview2/ (free, takes a
  minute), then restart the app.
- **The app window shows "couldn't start" but the log says uvicorn IS
  running** — this means the server is fine, but something on this
  specific machine is blocking the app's own loopback connection to
  itself (most commonly antivirus/endpoint-security software intercepting
  network traffic on managed/work laptops). Double-click
  **`Open in Browser (diagnostic).bat`** instead — it skips the desktop
  window entirely and opens the app in your normal browser (Edge/Chrome),
  with a console left open showing live logs. If that works, just use
  this script going forward. If your normal browser *also* can't reach
  it, that confirms something outside this app (security software, a
  VPN client, etc.) is blocking local connections — worth asking your
  IT/security team about an exclusion for Python/this folder if it's a
  managed machine.

---

## Project structure

```
ai_workspace/
├── main.py                       # desktop launcher (pywebview + local server)
├── run.bat                       # first-time setup + manual run (console)
├── Create Desktop Shortcut.bat   # adds the "AI Workspace" desktop icon
├── Allow Mobile Access (run as admin).bat  # opens the firewall port for phone access
├── Install Media Tools (optional).bat  # adds MP4 export to Media Tools
├── Build Standalone App.bat      # optional: packages a real .exe
├── Open in Browser (diagnostic).bat  # fallback: skip pywebview, use your normal browser
├── Download Speech Model.bat     # one-time: fetch the offline voice model
├── assets/
│   └── icon.ico                  # app icon
├── backend/
│   ├── app.py             # FastAPI routes + LAN access + no-cache middleware
│   ├── orchestrator.py    # background scheduler + multi-agent pipeline
│   ├── agents.py          # role definitions / system prompts
│   ├── ollama_client.py   # the ONLY always-local network code
│   ├── web_search.py       # OPTIONAL, opt-in web search (off by default)
│   ├── speech.py           # local, offline speech-to-text (Vosk)
│   ├── download_speech_model.py  # one-time voice model fetch
│   ├── doc_writer.py       # generates real .docx/.xlsx/.pptx output
│   ├── media_tools.py      # image editing, collage splitting, logos, slideshows
│   ├── file_extract.py    # best-effort text extraction from uploads
│   ├── storage.py         # SQLite persistence
│   └── security.py        # optional local at-rest encryption + access codes
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── requirements.txt
```
