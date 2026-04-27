import subprocess
import time
import sys

print("Starting FastAPI Backend (Port 8000)...")
backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--reload", "--port", "8000"])

# Give backend a moment to start
time.sleep(2)

print("Starting Streamlit Frontend (Port 8501)...")
frontend = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8501"])

try:
    print("System is running! Press Ctrl+C to exit.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down servers...")
    backend.terminate()
    frontend.terminate()
    print("Done.")
