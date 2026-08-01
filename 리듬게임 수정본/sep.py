import subprocess
import os

# 분리할 원본 음악 파일 이름
song_file = "first_glance_short.mp3"

print(f"'{song_file}' 음원 분리를 시작합니다...")

try:
    # 수정된 부분: "demucs" 대신 ["python", "-m", "demucs"]로 실행
    subprocess.run(["python", "-m", "demucs", "-n", "htdemucs_6s", song_file], check=True)

    print("\n분리 완료!")
    print(f"👉 피아노 파일 위치: separated/htdemucs_6s/{song_file.split('.')[0]}/piano.wav")

except Exception as e:
    print(f"\n에러가 발생했습니다: {e}")