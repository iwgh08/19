import pygame
import sys
import time
import math
import os
import random
import subprocess
import json

pygame.init()

# 초기 화면 설정
screen_size = 800
h, w = screen_size, screen_size
screen = pygame.display.set_mode((w, h))
NOTE_TRAVEL_TIME = 1.8
game_result = False

main = True
ingame = True

font = pygame.font.Font("Mona12TextKR.ttf", 30)
text_color = (255, 255, 255)

song = "first_glance_Full_Version.mp3"  

running = True
game_start = False
last_direction = 0

# 게임 이미지 설정
background = pygame.image.load("image\\game_background.png").convert()
judgement = pygame.image.load("image\\judgement_line.png").convert_alpha()
note_white = pygame.image.load("image\\white_note.png").convert_alpha()
note_yellow = pygame.image.load("image\\yellow_note.png").convert_alpha()

note_white = pygame.transform.scale(note_white, (100,100))
note_yellow = pygame.transform.scale(note_yellow, (100,100))
judgement = pygame.transform.scale(judgement, (180,180))
background = pygame.transform.scale(background, (800,800))
note_image = note_white

# 왼쪽 오른쪽 위쪽 노트 이미지
note_left_white = pygame.transform.rotate(note_white, 90)
note_right_white = pygame.transform.rotate(note_white, -90)
note_down_white = pygame.transform.rotate(note_white, 180)

note_left_yellow = pygame.transform.rotate(note_yellow, 90)
note_right_yellow = pygame.transform.rotate(note_yellow, -90)
note_down_yellow = pygame.transform.rotate(note_yellow, 180)

# 노트 중심 계산
center_x = w / 2
center_y = h / 2

# 글씨 저장 변수 선언
score = 0
combo = 0
max_combo = 0

# 버튼 설정
button_font = pygame.font.Font("Mona12TextKR.ttf", 32)

restart_button = pygame.Rect(w//2 - 130, 560, 260, 60)
exit_button = pygame.Rect(w//2 - 130, 640, 260, 60)

judge_text = ""
judge_time = 0

# 음악 재생 지연 설정 
music_delay = NOTE_TRAVEL_TIME -5
music_scheduled = False
music_playing = False

maxframe = 60
fps = 0

clock = pygame.time.Clock()

# 게임 시작 시간
game_start_time = 0

# 점수 관련 변수
score = 0
combo = 0
max_combo = 0
hits = 0
misses = 0

# 라인 별로 노트가 내려오는 길 리스트 
t1 = []
t2 = []
t3 = []
t4 = []

with open("note_pattern.json", "r") as f:
    note_pattern = json.load(f)

spawned_notes = set()

def add_note(direction, note_time):
    """노트를 추가하는 함수"""
    direction_names = ["위", "아래", "왼쪽", "오른쪽"]
    
    if direction == 0:  
        t1.append([0, note_time])
    elif direction == 1:  
        t2.append([h, note_time])
    elif direction == 2:  
        t3.append([0, note_time])
    elif direction == 3:  
        t4.append([w, note_time])
    
def add_score(hit_success):
    """점수와 콤보를 관리하는 함수"""
    global score, combo, max_combo, hits, misses
    
    if hit_success:
        combo += 1
        hits += 1
        base_score = 100
        combo_bonus = min(combo * 10, 500)
        score += base_score + combo_bonus
        
        if combo > max_combo:
            max_combo = combo
    else:
        combo = 0
        misses += 1

def check_hit(direction, current_time):
    """키 입력 시 노트 판정을 확인하는 함수"""
    size = 60
    hit_tolerance = 30  # 판정 허용 범위 (픽셀)
    speed = ((screen_size / 2) - 50) / NOTE_TRAVEL_TIME  # 노트 이동 속도
    
    # 정확도 판정의 구간 설정
    perfect_tolerance = 10  # 퍼펙트 판정 범위
    good_tolerance = 30    # 굿 판정 범위
    
    if direction == 0:  # 위 방향
        judgment_line = h / 2 - 5 - size
        for i, note_data in enumerate(t1[:]):
            note_y = note_data[0] + (current_time - note_data[1] + NOTE_TRAVEL_TIME) * speed
            distance = abs(note_y - judgment_line)
            if distance < hit_tolerance:
                t1.remove(note_data)
                if distance < perfect_tolerance:
                    add_score(True)
                    return "PERFECT"
                elif distance < good_tolerance:
                    add_score(True)
                    return "GOOD"
                else:
                    add_score(True)
                    return "OK"
    
    elif direction == 1:  # 아래 방향
        judgment_line = h / 2 - 5 + size
        for i, note_data in enumerate(t2[:]):
            note_y = note_data[0] - (current_time - note_data[1] + NOTE_TRAVEL_TIME) * speed
            distance = abs(note_y - judgment_line)
            if distance < hit_tolerance:
                t2.remove(note_data)
                if distance < perfect_tolerance:
                    add_score(True)
                    return "PERFECT"
                elif distance < good_tolerance:
                    add_score(True)
                    return "GOOD"
                else:
                    add_score(True)
                    return "OK"
    
    elif direction == 2:  # 왼쪽 방향
        judgment_line = w/2 - 5 - size
        for i, note_data in enumerate(t3[:]):
            note_x = note_data[0] + (current_time - note_data[1] + NOTE_TRAVEL_TIME) * speed
            distance = abs(note_x - judgment_line)
            if distance < hit_tolerance:
                t3.remove(note_data)
                if distance < perfect_tolerance:
                    add_score(True)
                    return "PERFECT"
                elif distance < good_tolerance:
                    add_score(True)
                    return "GOOD"
                else:
                    add_score(True)
                    return "OK"
    
    elif direction == 3:  # 오른쪽 방향
        judgment_line = w/2 - 5 + size
        for i, note_data in enumerate(t4[:]):
            note_x = note_data[0] - (current_time - note_data[1] + NOTE_TRAVEL_TIME) * speed
            distance = abs(note_x - judgment_line)
            if distance < hit_tolerance:
                t4.remove(note_data)
                if distance < perfect_tolerance:
                    add_score(True)
                    return "PERFECT"
                elif distance < good_tolerance:
                    add_score(True)
                    return "GOOD"
                else:
                    add_score(True)
                    return "OK"
    
    add_score(False)
    return "MISS"

while running:
    # 현재 게임 시간 계산
    if game_start:
        current_time = time.time() - game_start_time
    elif game_result:
        screen.blit(background,(0,0))

        accuracy = (hits/(hits+misses)*100) if (hits+misses)>0 else 100

        title = button_font.render("게임 결과", True, (255,255,255))
        screen.blit(title, title.get_rect(center=(w/2,80)))

        y = 180

        infos = [
            f"점수 : {score}",
            f"정확도 : {accuracy:.2f}%",
            f"최대 콤보 : {max_combo}",
            f"Hit : {hits}",
            f"Miss : {misses}"
        ]

        for txt in infos:
            img = font.render(txt, True, (255,255,255))
            screen.blit(img, img.get_rect(center=(w/2,y)))
            y += 50

        pygame.draw.rect(screen,(70,170,70),restart_button,border_radius=12)
        pygame.draw.rect(screen,(180,70,70),exit_button,border_radius=12)

        restart = button_font.render("다시하기",True,(255,255,255))
        quit_text = button_font.render("게임 종료",True,(255,255,255))

        screen.blit(restart,restart.get_rect(center=restart_button.center))
        screen.blit(quit_text,quit_text.get_rect(center=exit_button.center))
    else:
        current_time = 0
    
    # 노트 생성
    if game_start:
        for note_time, direction in note_pattern:
            note_key = (note_time, direction)
            if current_time >= note_time - NOTE_TRAVEL_TIME and note_key not in spawned_notes:
                add_note(direction, note_time)
                spawned_notes.add(note_key)

    # 음악 예약이 있고 지연 시간이 지났으면 재생 시작
    if game_start and music_scheduled and not music_playing:
        if current_time >= music_delay:
            try:
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                music_playing = True
                music_scheduled = False
            except Exception as e:
                music_scheduled = False
        # 노래 종료 확인
    if game_start and music_playing and not pygame.mixer.music.get_busy():
        if not pygame.mixer.music.get_busy():
            game_start = False
            game_result = True
            music_playing = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_result:

                if restart_button.collidepoint(event.pos):

                    game_result = False
                    game_start = False
                    game_start = True
                    game_start_time = time.time()

                    music_scheduled = True
                    music_playing = False

                    score = 0
                    combo = 0
                    max_combo = 0
                    hits = 0
                    misses = 0

                    judge_text = ""

                    spawned_notes.clear()

                    t1.clear()
                    t2.clear()
                    t3.clear()
                    t4.clear()

                elif exit_button.collidepoint(event.pos):

                    pygame.quit()
                    sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_start == False:
                    game_start = True
                    game_start_time = time.time()  # 게임 시작 시간 기록
                    # 점수 초기화
                    score = 0
                    combo = 0
                    max_combo = 0
                    hits = 0
                    misses = 0
                    spawned_notes.clear()
                    t1.clear()
                    t2.clear()
                    t3.clear()
                    t4.clear()
                    # 스페이스바를 누르면 즉시 재생하지 않고 지연 재생 예약
                    music_scheduled = True
                    music_playing = False
            
            # R키로 게임 재시작
            if event.key == pygame.K_r and game_start:
                # 중간 재시작: 정지하고 음악 상태 초기화
                game_start = False
                if music_playing:
                    try:
                        pygame.mixer.music.stop()
                    except Exception:
                        pass
                music_scheduled = False
                music_playing = False
            
            # 키 누를 때 방향 확인 및 판정
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                last_direction = 0
                # 위 방향 노트 판정
                judge_text = check_hit(0, current_time)
                judge_time = time.time()
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                last_direction = 1
                # 아래 방향 노트 판정
                judge_text = check_hit(1, current_time)
                judge_time = time.time()
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                last_direction = 2
                # 왼쪽 방향 노트 판정
                judge_text = check_hit(2, current_time)
                judge_time = time.time()
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                last_direction = 3
                # 오른쪽 방향 노트 판정
                judge_text = check_hit(3, current_time)
                judge_time = time.time()
        
    if  game_start:
        screen.blit(background,(0,0))

    size = 60

    # 노트 그리기 및 이동
    if game_start == True:
        travel_distance = (screen_size / 2) - 50  # 중심에서 판정선까지의 거리
        speed = travel_distance / NOTE_TRAVEL_TIME  # 2초에 도달하는 속도
        

        # 위에서 아래로 움직이는 노트들 (t1)
        judgment_line_top = h / 2 - 5 - size  # 위쪽 판정선 위치
        for note_data in t1[:]:
            note_y = note_data[0] + (current_time - note_data[1] + NOTE_TRAVEL_TIME) * speed
            # 판정선을 지나가면 제거
            if note_y > judgment_line_top + 30:  # 노트가 판정선을 완전히 지나감
                t1.remove(note_data)
                add_score(False)  
            else:
                # 판정선 근처에서 노트 색상 변경
                if abs(note_y - judgment_line_top) < 40:
                    note_image = note_yellow
                else:
                    note_image = note_white
                screen.blit(note_image,(center_x - note_image.get_width() / 2, note_y - note_image.get_height() / 2))
        
        # 아래에서 위로 움직이는 노트들 (t2)
        judgment_line_bottom = h / 2 - 5 + size  
        for note_data in t2[:]:
            note_y = note_data[0] - (current_time - note_data[1] + NOTE_TRAVEL_TIME) * speed
            # 판정선을 지나가면 제거
            if note_y < judgment_line_bottom - 30:  
                t2.remove(note_data)
                add_score(False)  
            else:
                # 판정선 근처에서 노트 색상 변경
                if abs(note_y - judgment_line_bottom) < 40:
                    note_image = note_down_yellow
                else:
                    note_image = note_down_white
                screen.blit(note_image,(center_x - note_image.get_width() / 2, note_y - note_image.get_height() / 2))
        
        # 왼쪽에서 오른쪽으로 움직이는 노트들 (t3)
        judgment_line_left = w/2 - 5 - size  # 왼쪽 판정선 위치
        for note_data in t3[:]:
            note_x = note_data[0] + (current_time - note_data[1] + NOTE_TRAVEL_TIME) * speed
            # 판정선을 지나가면 제거
            if note_x > judgment_line_left + 30: 
                t3.remove(note_data)
                add_score(False) 
            else:
                # 판정선 근처에서 노트 색상 변경
                if abs(note_x - judgment_line_left) < 40:
                    note_image = note_left_yellow
                else:
                    note_image = note_left_white
                screen.blit(note_image,(note_x - note_image.get_width()/2, h/2 - note_image.get_height()/2))
        
        # 오른쪽에서 왼쪽으로 움직이는 노트들 (t4)
        judgment_line_right = w/2 - 5 + size  # 오른쪽 판정선 위치
        for note_data in t4[:]:
            note_x = note_data[0] - (current_time - note_data[1] + NOTE_TRAVEL_TIME) * speed
            # 판정선을 지나가면 제거
            if note_x < judgment_line_right - 30:  
                t4.remove(note_data)
                add_score(False)  
            else:
                # 판정선 근처에서 노트 색상 변경
                if abs(note_x - judgment_line_right) < 40:
                    note_image = note_right_yellow
                else:
                    note_image = note_right_white
            screen.blit(note_image,(note_x - note_image.get_width()/2, h/2 - note_image.get_height()/2))
    

    # 판정선 이미지 그리기
    if game_start:
        screen.blit(judgement, (w/2 - judgement.get_width()//2, h/2 - judgement.get_height()//2))

    if judge_text != "" and time.time() - judge_time < 0.4:

        judge_font = pygame.font.Font("Mona12TextKR.ttf",40)

        if judge_text == "PERFECT":
            color = (255, 255, 0)

        elif judge_text == "GOOD":
            color = (0, 255, 0)

        elif judge_text == "OK":
            color = (100, 200, 255)

        else:
            color = (255, 80, 80)

        text = judge_font.render(judge_text, True, color)

        rect = text.get_rect(center=(w/2, h/2))

        screen.blit(text, rect)
    # UI 표시 (점수, 콤보 등)
    if game_start:
        score_text = font.render(f"Score : {score:,}", True, text_color)
        screen.blit(score_text, (20, 20))

        # 콤보
        combo_text = font.render(f"Combo : {combo}", True, text_color)
        screen.blit(combo_text, (20, 50))

        # 정확도
        accuracy = (hits / (hits + misses) * 100) if (hits + misses) > 0 else 100
        accuracy_text = font.render(f"Accuracy : {accuracy:.1f}%", True, text_color)
        screen.blit(accuracy_text, (20, 80))
    elif not game_result:
        # 게임 시작 안내
        start_text = font.render("Start to press space!", True, text_color)
        text_rect = start_text.get_rect(center=(w/2, h/2 + 100))
        screen.blit(start_text, text_rect)

    pygame.display.flip()
    clock.tick(maxframe)  # FPS 제한