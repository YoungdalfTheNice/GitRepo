import os
import subprocess
from setup_yt_channel_transcripts import zielverzeichnis

script_path = os.path.join(zielverzeichnis, "streamlit.py")

subprocess.run(['streamlit', 'run', script_path])
