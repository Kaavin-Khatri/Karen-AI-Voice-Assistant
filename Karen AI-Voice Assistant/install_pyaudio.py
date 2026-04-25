import sys
import os
import subprocess

# Find pipwin executable path
pipwin_path = os.path.join(sys.prefix, 'Scripts', 'pipwin.exe')
print(f"Trying to run {pipwin_path}")

try:
    subprocess.run([pipwin_path, 'install', 'pyaudio'], check=True)
    print("PyAudio installation successful.")
except Exception as e:
    print(f"Failed to run pipwin: {e}")
