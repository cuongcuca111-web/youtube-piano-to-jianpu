@echo off
chcp 65001 >nul
echo ========================================================
echo   Cài đặt Jianpu Piano AI khởi động cùng Windows
echo ========================================================
set "TARGET_DIR=%~dp0"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTUP_FOLDER%\JianpuPianoAI.lnk'); $Shortcut.TargetPath = 'wscript.exe'; $Shortcut.Arguments = '\"%TARGET_DIR%run_hidden.vbs\"'; $Shortcut.WorkingDirectory = '%TARGET_DIR%'; $Shortcut.Description = 'Jianpu Piano AI Background Server'; $Shortcut.Save()"

echo [Thành công] Đã cài đặt! Mỗi khi bạn bật máy tính:
echo - Máy chủ sẽ tự động chạy ngầm sẵn sàng.
echo - Bạn chỉ cần mở trình duyệt vào http://127.0.0.1:8000 là dùng được ngay!
echo ========================================================
pause
