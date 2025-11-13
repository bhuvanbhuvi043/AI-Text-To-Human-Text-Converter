import os
import subprocess
import webbrowser
import time

# Launch Streamlit app
subprocess.Popen(["streamlit", "run", "app.py"])

# Wait for Streamlit to start, then open in browser
time.sleep(5)
webbrowser.open("http://localhost:8501")
