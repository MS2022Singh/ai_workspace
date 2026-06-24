' Silent launcher used by the desktop shortcut.
' Runs the app with no console window. Requires that "run.bat" has been
' run at least once already (so the venv + dependencies exist).
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

Set shell = CreateObject("WScript.Shell")
pythonw = scriptDir & "\venv\Scripts\pythonw.exe"

If fso.FileExists(pythonw) Then
    shell.CurrentDirectory = scriptDir
    shell.Run """" & pythonw & """ main.py", 0, False
Else
    MsgBox "Setup hasn't run yet." & vbCrLf & vbCrLf & _
           "Please double-click run.bat once first (it installs everything), " & _
           "then use this shortcut from now on.", vbExclamation, "AI Workspace"
End If
