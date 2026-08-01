import librosa
import json
import random

file_path = "first_glance_Full_Version.wav"

print(f"'{file_path}' 파일을 분석 중입니다... 잠시만 기다려주세요!")

# 파일 불러오기
y, sr = librosa.load(file_path, sr=None)

# hop_length를 512로 설정하여 더 세밀한 비트 감지
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

print(f"완료! 총 {len(note_pattern)}개의 노트가 note_pattern.json에 저장되었습니다.")