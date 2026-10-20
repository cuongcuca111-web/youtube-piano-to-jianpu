import os
import sys
import time
import socket
import webbrowser
import threading
import uvicorn

def is_server_running(port: int = 8000) -> bool:
    """Checks if the Jianpu server is already running on the port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0

def open_browser(delay: float = 1.0):
    time.sleep(delay)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    # If server is already running in background, just open the browser and exit
    if is_server_running(8000):
        print("Máy chủ đang chạy ngầm sẵn sàng. Đang mở trình duyệt web...")
        open_browser(0.2)
        sys.exit(0)

    print("=" * 60)
    print("  JianpuPiano AI - Đang khởi động máy chủ Web...")
    print("  Trang web sẽ tự động mở tại: http://127.0.0.1:8000")
    print("=" * 60)
    threading.Thread(target=open_browser, args=(1.2,), daemon=True).start()
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)

