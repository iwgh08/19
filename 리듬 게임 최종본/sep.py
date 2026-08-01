import subprocess
import os

# 분리할 원본 음악 파일 이름
song_file = "first_glance_short.mp3"

try:
    subprocess.run(["python", "-m", "demucs", "-n", "htdemucs_6s", song_file], check=True)
except Exception as e:
    pass