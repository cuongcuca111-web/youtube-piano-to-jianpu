Set WshShell = CreateObject("WScript.Shell")
strDir = WshShell.CurrentDirectory
WshShell.Run "python start.py", 0, False
Set WshShell = Nothing
