import os
import subprocess
import sys

def verify_and_build():
    print('[*] Starting Self-Sufficient Package Build...')
    # Ensure PyInstaller is available for packaging
    try:
        import PyInstaller
    except ImportError:
        print('[*] Installing PyInstaller for standalone bundling...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

    # Build standalone desktop bundle
    print('[*] Packaging Desktop Standalone Executable (Windows/Linux/macOS)...')
    # Create a spec or run pyinstaller command bundling app files
    subprocess.check_call([
        sys.executable, '-m', 'PyInstaller',
        '--onedir',
        '--name=AI_Workspace_OS',
        'server.py' if os.path.exists('server.py') else 'computer_control.py'
    ])
    print('[+] Standalone desktop package successfully compiled in ./dist/AI_Workspace_OS/')

if __name__ == '__main__':
    verify_and_build()
