import librosa
import json
import random

file_path = "first_glance_Full_Version.wav"

# 파일 불러오기
y, sr = librosa.load(file_path, sr=None)

# hop_length를 512로 설정하여 더 비트 감지
onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=512)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

note_pattern = []
for t in onset_times:
    time_sec = round(float(t), 2)
    direction = random.randint(0, 3) # 0~3 무작위 방향
    note_pattern.append([time_sec, direction])

# JSON 저장
with open("note_pattern.json", "w") as f:
    json.dump(note_pattern, f)