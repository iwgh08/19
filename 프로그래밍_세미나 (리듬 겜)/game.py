import pygame
import sys
import time
import math
import os
import random


pygame.init()

# 정사각형 화면으로 설정
screen_size = 800
h, w = screen_size, screen_size
screen = pygame.display.set_mode((w, h))

main = True
ingame = True

font = pygame.font.SysFont("Courier", 18, True, True)
text_color = (255, 255, 255)

song = "first glance_short.mp3"  

running = True
game_start = False
last_direction = 0

# 음악 재생 지연 설정 (초 단위)
music_delay = 2.0  # 게임 시작하고 2초 뒤에 음악 재생
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

# 라인 별로 노트가 내려오는 길을 리스트 만들기
t1 = []
t2 = []
t3 = []
t4 = []

# 노트 패턴 정의 (시간(초), 방향)
# 방향: 0=위, 1=아래, 2=왼쪽, 3=오른쪽
note_pattern = [
    (0.65, random.randint(0, 3)),
    (1.8, random.randint(0, 3)),
    (2.5, random.randint(0, 3)),
    (3.15, random.randint(0, 3)),

    (4.35, random.randint(0, 3)),
    (5.55, random.randint(0, 3)),
    (5.95, random.randint(0, 3)),
    (6.35, random.randint(0, 3)),
    (7.0, random.randint(0, 3)),

    (7.6, random.randint(0, 3)),
    (8.25, random.randint(0, 3)),
    (9.55, random.randint(0, 3)),
    (10.2, random.randint(0, 3)),
    (11.4, random.randint(0, 3)),
    (12.0, random.randint(0, 3)),

    (13.9, random.randint(0, 3)),
    (16.0, random.randint(0, 3)),
    (17.2, random.randint(0, 3)),
    (17.9, random.randint(0, 3)),

    (19.6, random.randint(0, 3)),
    (20.8, random.randint(0, 3)),
    (21.2, random.randint(0, 3)),
    (21.6 , random.randint(0, 3)),
    (22.3, random.randint(0, 3)),
    (23.5, random.randint(0, 3)),
    (24.8, random.randint(0, 3)),
    (25.5, random.randint(0, 3)),
    (26.7 , random.randint(0, 3)),
    (27.2, random.randint(0, 3)),
    (29.2, random.randint(0, 3)),
]

spawned_notes = set()

def add_note(direction, current_time):
    """노트를 추가하는 함수"""
    direction_names = ["위", "아래", "왼쪽", "오른쪽"]
    
    if direction == 0:  
        t1.append([0, current_time + 2])  # 2초 후에 판정선에 도달
    elif direction == 1:  
        t2.append([h, current_time + 2])
    elif direction == 2:  
        t3.append([0, current_time + 2])
    elif direction == 3:  
        t4.append([w, current_time + 2])
    
def add_score(hit_success):
    """점수와 콤보를 관리하는 함수"""
    global score, combo, max_combo, hits, misses
    
    if hit_success:
        combo += 1
        hits += 1
        base_score = 100
        combo_bonus = min(combo * 10, 500)  # 최대 500점 보너스
        score += base_score + combo_bonus
        
        if combo > max_combo:
            max_combo = combo
        
        print(f"HIT! +{base_score + combo_bonus}점 (콤보: {combo})")
    else:
        combo = 0
        misses += 1

def check_hit(direction, current_time):
    """키 입력 시 노트 판정을 확인하는 함수"""
    size = 60
    hit_tolerance = 30  # 판정 허용 범위 (픽셀)
    speed = ((screen_size / 2) - 50) / 2  # 노트 이동 속도
    
    # 정확도 판정의 구간 설정
    perfect_tolerance = 10  # 퍼펙트 판정 범위
    good_tolerance = 20    # 굿 판정 범위
    
    if direction == 0:  # 위 방향
        judgment_line = h / 2 - 5 - size
        for i, note_data in enumerate(t1[:]):
            note_y = note_data[0] + (current_time - note_data[1] + 2) * speed
            distance = abs(note_y - judgment_line)
            if distance < hit_tolerance:
                t1.remove(note_data)
                if distance < perfect_tolerance:
                    print("PERFECT!")
                    add_score(True)
                    return "PERFECT"
                elif distance < good_tolerance:
                    print("GOOD!")
                    add_score(True)
                    return "GOOD"
                else:
                    print("OK!")
                    add_score(True)
                    return "OK"
    
    elif direction == 1:  # 아래 방향
        judgment_line = h / 2 - 5 + size
        for i, note_data in enumerate(t2[:]):
            note_y = note_data[0] - (current_time - note_data[1] + 2) * speed
            distance = abs(note_y - judgment_line)
            if distance < hit_tolerance:
                t2.remove(note_data)
                if distance < perfect_tolerance:
                    print("PERFECT!")
                    add_score(True)
                    return "PERFECT"
                elif distance < good_tolerance:
                    print("GOOD!")
                    add_score(True)
                    return "GOOD"
                else:
                    print("OK!")
                    add_score(True)
                    return "OK"
    
    elif direction == 2:  # 왼쪽 방향
        judgment_line = w/2 - 5 - size
        for i, note_data in enumerate(t3[:]):
            note_x = note_data[0] + (current_time - note_data[1] + 2) * speed
            distance = abs(note_x - judgment_line)
            if distance < hit_tolerance:
                t3.remove(note_data)
                if distance < perfect_tolerance:
                    print("PERFECT!")
                    add_score(True)
                    return "PERFECT"
                elif distance < good_tolerance:
                    print("GOOD!")
                    add_score(True)
                    return "GOOD"
                else:
                    print(" OK!")
                    add_score(True)
                    return "OK"
    
    elif direction == 3:  # 오른쪽 방향
        judgment_line = w/2 - 5 + size
        for i, note_data in enumerate(t4[:]):
            note_x = note_data[0] - (current_time - note_data[1] + 2) * speed
            distance = abs(note_x - judgment_line)
            if distance < hit_tolerance:
                t4.remove(note_data)
                if distance < perfect_tolerance:
                    print("PERFECT!")
                    add_score(True)
                    return "PERFECT"
                elif distance < good_tolerance:
                    print("GOOD!")
                    add_score(True)
                    return "GOOD"
                else:
                    print("OK!")
                    add_score(True)
                    return "OK"
    
    add_score(False)
    return "MISS"

while running:
    # 현재 게임 시간 계산
    if game_start:
        current_time = time.time() - game_start_time
    else:
        current_time = 0
    
    # 노트 생성
    if game_start:
        for note_time, direction in note_pattern:
            note_key = (note_time, direction)
            if current_time >= note_time and note_key not in spawned_notes:
                add_note(direction, current_time)
                spawned_notes.add(note_key)

    # 음악 예약이 있고 지연 시간이 지났으면 재생 시작
    if game_start and music_scheduled and not music_playing:
        if current_time >= music_delay:
            try:
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                music_playing = True
                music_scheduled = False
                print(f"음악 재생 시작 (지연 {music_delay}s 이후)")
            except Exception as e:
                print(f"음악 재생 실패: {e}")
                music_scheduled = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
                print("게임 재시작!")
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
                check_hit(0, current_time)
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                last_direction = 1
                # 아래 방향 노트 판정
                check_hit(1, current_time)
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                last_direction = 2
                # 왼쪽 방향 노트 판정
                check_hit(2, current_time)
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                last_direction = 3
                # 오른쪽 방향 노트 판정
                check_hit(3, current_time)
        
    screen.fill((0, 0, 0)) 
    pygame.draw.circle(screen, (255, 255, 255), (int(w/2), int(h/2)), 30)

    size = 60

    # 노트 그리기 및 이동
    if game_start == True:
        travel_distance = (screen_size / 2) - 50  # 중심에서 판정선까지의 거리
        speed = travel_distance / 2  # 2초에 도달하는 속도
         
        # 위에서 아래로 움직이는 노트들 (t1)
        judgment_line_top = h / 2 - 5 - size  # 위쪽 판정선 위치
        for note_data in t1[:]:
            note_y = note_data[0] + (current_time - note_data[1] + 2) * speed
            # 판정선을 지나가면 제거
            if note_y > judgment_line_top + 30:  # 노트가 판정선을 완전히 지나감
                t1.remove(note_data)
                add_score(False)  
                print("위 방향 노트 미스")
            else:
                # 판정선 근처에서 노트 색상 변경
                if abs(note_y - judgment_line_top) < 20:
                    color = (255, 255, 100)  # 판정 가능 구간에서 노란색
                else:
                    color = (255, 255, 255)  
                pygame.draw.rect(screen, color, (w/2 - 10, note_y, 20, 20))
        
        # 아래에서 위로 움직이는 노트들 (t2)
        judgment_line_bottom = h / 2 - 5 + size  
        for note_data in t2[:]:
            note_y = note_data[0] - (current_time - note_data[1] + 2) * speed
            # 판정선을 지나가면 제거
            if note_y < judgment_line_bottom - 30:  
                t2.remove(note_data)
                add_score(False)  
                print("아래 방향 노트 미스")
            else:
                # 판정선 근처에서 노트 색상 변경
                if abs(note_y - judgment_line_bottom) < 20:
                    color = (255, 255, 100)  # 판정 가능 구간에서 노란색
                else:
                    color = (255, 255, 255)  # 기본 흰색
                pygame.draw.rect(screen, color, (w/2 - 10, note_y, 20, 20))
        
        # 왼쪽에서 오른쪽으로 움직이는 노트들 (t3)
        judgment_line_left = w/2 - 5 - size  # 왼쪽 판정선 위치
        for note_data in t3[:]:
            note_x = note_data[0] + (current_time - note_data[1] + 2) * speed
            # 판정선을 지나가면 제거
            if note_x > judgment_line_left + 30: 
                t3.remove(note_data)
                add_score(False) 
                print("왼쪽 방향 노트 미스")
            else:
                # 판정선 근처에서 노트 색상 변경
                if abs(note_x - judgment_line_left) < 20:
                    color = (255, 255, 100)  # 판정 가능 구간에서 노란색
                else:
                    color = (255, 255, 255) 
                pygame.draw.rect(screen, color, (note_x, h/2 - 10, 20, 20))
        
        # 오른쪽에서 왼쪽으로 움직이는 노트들 (t4)
        judgment_line_right = w/2 - 5 + size  # 오른쪽 판정선 위치
        for note_data in t4[:]:
            note_x = note_data[0] - (current_time - note_data[1] + 2) * speed
            # 판정선을 지나가면 제거
            if note_x < judgment_line_right - 30:  
                t4.remove(note_data)
                add_score(False)  
                print("오른쪽 방향 노트 미스")
            else:
                # 판정선 근처에서 노트 색상 변경
                if abs(note_x - judgment_line_right) < 20:
                    color = (255, 255, 100)  # 판정 가능 구간에서 노란색
                else:
                    color = (255, 255, 255) 
                pygame.draw.rect(screen, color, (note_x, h/2 - 10, 20, 20))
    
    # 테두리 그리기
    pygame.draw.rect(screen, (100, 100, 255), (0, 0, w, 10))
    pygame.draw.rect(screen, (100, 100, 255), (0, h - 10, w, 10))
    pygame.draw.rect(screen, (100, 100, 255), (0, 0, 10, h))
    pygame.draw.rect(screen, (100, 100, 255), (w - 10, 0, 10, h))

    # gamebar 미리보기 선
    pygame.draw.rect(screen, (255, 255, 255), (w/2 - 65, h / 2 - 5 - size, 130, 10))
    pygame.draw.rect(screen, (255, 255, 255), (w/2 - 65, h / 2 - 5 + size, 130, 10))
    pygame.draw.rect(screen, (255, 255, 255), (w/2 - 5 - size, h / 2 - 65, 10, 130))
    pygame.draw.rect(screen, (255, 255, 255), (w/2 - 5 + size, h / 2 - 65, 10, 130))

    # UI 표시 (점수, 콤보 등)
    if game_start:
        # 점수 표시
        score_text = font.render(f"Score: {score:,}", True, text_color)
        screen.blit(score_text, (20, 20))
        
        # 콤보 표시
        combo_text = font.render(f"Combo: {combo}", True, text_color)
        screen.blit(combo_text, (20, 50))
        
        # 최대 콤보 표시
        max_combo_text = font.render(f"Max Combo: {max_combo}", True, text_color)
        screen.blit(max_combo_text, (20, 80))
        
        # HIT/MISS 통계
        accuracy = (hits / (hits + misses) * 100) if (hits + misses) > 0 else 0
        stats_text = font.render(f"HIT: {hits} | MISS: {misses} | Accuracy: {accuracy:.1f}%", True, text_color)
        screen.blit(stats_text, (20, 110))
        
        # 현재 시간 표시
        time_text = font.render(f"Time: {current_time:.1f}s", True, text_color)
        screen.blit(time_text, (w - 150, 20))
    else:
        # 게임 시작 안내
        start_text = font.render("Press SPACE to Start!", True, text_color)
        text_rect = start_text.get_rect(center=(w/2, h/2 + 100))
        screen.blit(start_text, text_rect)

    pygame.display.flip()
    clock.tick(maxframe)  # FPS 제한