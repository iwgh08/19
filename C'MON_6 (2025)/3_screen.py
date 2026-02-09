# ====== 전설의 농부 - 드래곤 전투 ======
import pygame
import math
pygame.init()

# ====== 화면 설정 ======
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("전설의 농부")

# ====== 폰트 설정 ======
font_path = "C:\\Users\\minih\\Desktop\\C'MON_6\\NanumGothic.ttf"
font = pygame.font.Font(font_path, 40)
large_font = pygame.font.Font(font_path, 80)
small_font = pygame.font.Font(font_path, 25)

# ====== 배경 이미지 ======
altar = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\altar.png")
altar = pygame.transform.scale(altar, (screen_width, screen_height))

# ====== 캐릭터 이미지 ======
player_attack_img = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\player_attack.png").convert_alpha()
PLAYER_COLS = 7
PLAYER_ROWS = 6
PLAYER_FRAME_WIDTH = player_attack_img.get_width() // PLAYER_COLS
PLAYER_FRAME_HEIGHT = player_attack_img.get_height() // PLAYER_ROWS

# ====== 드래곤 이미지 ======
dragon_img = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\dragon.png").convert_alpha()
DRAGON_COLS = 3
DRAGON_ROWS = 4
DRAGON_FRAME_WIDTH = dragon_img.get_width() // DRAGON_COLS
DRAGON_FRAME_HEIGHT = dragon_img.get_height() // DRAGON_ROWS

# ====== 불꽃 이미지 ======
fire_img = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\fire.png").convert_alpha()

# === 플레이어 크기 ===
character_width = int(PLAYER_FRAME_WIDTH * 5)
character_height = int(PLAYER_FRAME_HEIGHT * 5)

# === 드래곤 크기 ===
dragon_width = int(DRAGON_FRAME_WIDTH * 6)
dragon_height = int(DRAGON_FRAME_HEIGHT * 6)

# === 불꽃 크기 ===
fire_width = 60
fire_height = 60

character_x_pos = 25
ground_y = screen_height
character_y_pos = ground_y - character_height + 1
character_speed = 5

# 애니메이션 관련 변수
walk_frame = 0
walk_frame_counter = 0
WALK_FRAME_SPEED = 3

# === 캐릭터 방향 ===
facing = "right"

# === 플레이어 프레임 추출 함수 (무기 소유 상태) ===
def get_player_frame(frame_index, facing_dir="right", state="walk"):
    """player_attack_img에서 프레임 추출 (7x6 그리드)"""
    col = frame_index % PLAYER_COLS

    if state == "walk":
        row = 0 if facing_dir == "right" else 1
    elif state == "jump":
        row = 2 if facing_dir == "right" else 3
    elif state == "attack":
        row = 4 if facing_dir == "right" else 5
    else:
        row = 0

    x = col * PLAYER_FRAME_WIDTH
    y = row * PLAYER_FRAME_HEIGHT

    rect = pygame.Rect(x, y, PLAYER_FRAME_WIDTH, PLAYER_FRAME_HEIGHT)
    try:
        return player_attack_img.subsurface(rect)
    except:
        return player_attack_img.subsurface(pygame.Rect(0, 0, PLAYER_FRAME_WIDTH, PLAYER_FRAME_HEIGHT))

# === 드래곤 프레임 추출 함수 ===
def get_dragon_frame(frame_index, facing_dir="right", is_attacking=False):
    #드래곤 스프라이트 시트에서 프레임 추출 (3x4 그리드)
    #1행: 왼쪽 이동, 2행: 오른쪽 이동, 3행: 왼쪽 공격, 4행: 오른쪽 공격
    col = frame_index % DRAGON_COLS
    
    if is_attacking:
        row = 2 if facing_dir == "left" else 3  # 3행=왼쪽 공격, 4행=오른쪽 공격
    else:
        row = 0 if facing_dir == "left" else 1  # 1행=왼쪽 이동, 2행=오른쪽 이동
    
    x = col * DRAGON_FRAME_WIDTH
    y = row * DRAGON_FRAME_HEIGHT
    
    rect = pygame.Rect(x, y, DRAGON_FRAME_WIDTH, DRAGON_FRAME_HEIGHT)
    try:
        return dragon_img.subsurface(rect)
    except:
        return dragon_img.subsurface(pygame.Rect(0, 0, DRAGON_FRAME_WIDTH, DRAGON_FRAME_HEIGHT))

# === 불꽃 클래스 ===
class Fireball:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 5
        # 플레이어 위치로 가는 방향 계산
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            self.vel_x = (dx / dist) * self.speed
            self.vel_y = (dy / dist) * self.speed
        else:
            self.vel_x = 0
            self.vel_y = 0
        self.alive = True
        self.hit = False

    def update(self):
        if not self.alive:
            return
        self.x += self.vel_x
        self.y += self.vel_y
        
        # 화면 밖으로 나가면 제거
        if self.x < -100 or self.x > screen_width + 100 or self.y < -100 or self.y > screen_height + 100:
            self.alive = False

    def draw(self, screen):
        if self.alive:
            fire_scaled = pygame.transform.scale(fire_img, (fire_width, fire_height))
            screen.blit(fire_scaled, (int(self.x), int(self.y)))

# === 드래곤 클래스 ===
class Dragon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = dragon_width
        self.height = dragon_height
        self.hp = 50
        self.alive = True
        self.state = "move"  # move, attack
        self.facing_dir = "left"
        self.maintain_distance = 150
        self.move_speed = 2
        self.attack_cooldown = 0
        self.attack_cooldown_time = 120
        self.attack_duration = 30
        self.attack_timer = 0
        # 애니메이션
        self.frame_index = 0
        self.frame_counter = 0
        self.frame_speed = 8

    def update(self, px, py, fireballs):
        if not self.alive:
            return

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # 플레이어와의 거리 계산
        dx = px - self.x
        dy = py - self.y
        dist = math.sqrt(dx*dx + dy*dy)

        if self.state == "move":
            # 플레이어 방향 결정
            if dx < 0:
                self.facing_dir = "left"
            else:
                self.facing_dir = "right"
            
            # 일정 거리 유지
            if dist > self.maintain_distance:
                # 플레이어에게 가까이
                move_dx = (dx / dist) * self.move_speed
                self.x += move_dx
            elif dist < self.maintain_distance:
                # 플레이어에게서 멀어지기
                move_dx = -(dx / dist) * self.move_speed
                self.x += move_dx
            
            # 공격 가능 시 공격 상태로 전환
            if self.attack_cooldown == 0:
                self.state = "attack"
                self.attack_timer = self.attack_duration
                self.attack_cooldown = self.attack_cooldown_time
                # 불꽃 생성
                fire_x = self.x + (self.width if self.facing_dir == "right" else 0)
                fire_y = self.y + self.height // 2
                fireballs.append(Fireball(fire_x, fire_y, px + character_width // 2, py + character_height // 2))
            
            # 애니메이션 프레임 업데이트
            self.frame_counter += 1
            if self.frame_counter >= self.frame_speed:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % DRAGON_COLS

        elif self.state == "attack":
            # 공격 중에는 움직이지 않음
            if self.attack_timer > 0:
                self.attack_timer -= 1
                # 공격 애니메이션
                self.frame_counter += 1
                if self.frame_counter >= self.frame_speed:
                    self.frame_counter = 0
                    self.frame_index = (self.frame_index + 1) % DRAGON_COLS
            else:
                self.state = "move"
                self.frame_index = 0

    def draw(self, screen):
        if not (self.alive and self.hp > 0):
            return
        is_attacking = (self.state == "attack")
        dragon_frame = get_dragon_frame(self.frame_index, self.facing_dir, is_attacking)
        dragon_scaled = pygame.transform.scale(dragon_frame, (self.width, self.height))
        screen.blit(dragon_scaled, (int(self.x), int(self.y)))
        
        # 드래곤 이름 표시
        name_text = small_font.render("드래곤", True, (255, 255, 255))
        screen.blit(name_text, (int(self.x), int(self.y) - 55))
        
        hp_text = small_font.render(f"HP: {self.hp}", True, (255, 255, 255))
        screen.blit(hp_text, (int(self.x), int(self.y) - 30))

# === HP 관련 ===
hp = 100
max_hp = 100

# === 점프 관련 ===
jumping = False
jump_start = 0
jump_duration = 500
jump_peak = screen_height - (screen_height // 4) - character_height

# === 표시 상태 ===
show_character = True
show_hp = True

# === 드래곤 처치 후 상태 ===
dragon_defeated = False
player_dying = False
dying_start_time = 0
player_disappeared = False
disappear_wait_time = 3000  # 3초
game_over = False  # 일반 게임 오버 (드래곤에게 패배)

# === 모션 상태 정의 ===
character_normal = "normal"
character_attack = "attack"
character_motion = character_normal

# 공격 모션 시간
attack_duration = 450
attack_cooldown_time = attack_duration
attack_start_time = 0
attack_hit = False
attack_frame = 0
attack_frame_counter = 0
ATTACK_FRAME_SPEED = 2
attack_cooldown = 0

running = True
clock = pygame.time.Clock()

# 드래곤 초기화
dragon = Dragon(screen_width * 0.7, ground_y - dragon_height - 80)
fireballs = []

# === 게임 초기화 함수 ===
def reset_game():
    global character_x_pos, character_y_pos, hp, jumping, jump_start
    global character_motion, attack_start_time, attack_hit, attack_frame, attack_frame_counter, attack_cooldown
    global walk_frame, walk_frame_counter, facing
    global dragon, fireballs, dragon_defeated, player_dying, dying_start_time, player_disappeared
    global game_over, show_character
    
    # 플레이어 위치 및 상태 초기화
    character_x_pos = 25
    character_y_pos = ground_y - character_height + 1
    hp = max_hp
    jumping = False
    jump_start = 0
    
    # 공격 상태 초기화
    character_motion = character_normal
    attack_start_time = 0
    attack_hit = False
    attack_frame = 0
    attack_frame_counter = 0
    attack_cooldown = 0
    
    # 애니메이션 초기화
    walk_frame = 0
    walk_frame_counter = 0
    facing = "right"
    
    # 드래곤 및 게임 상태 초기화
    dragon = Dragon(screen_width * 0.7, ground_y - dragon_height - 80)
    fireballs.clear()
    dragon_defeated = False
    player_dying = False
    dying_start_time = 0
    player_disappeared = False
    game_over = False
    show_character = True

# === 게임 오버 화면 ===
def draw_game_over(screen):
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    go_text = large_font.render("GAME OVER", True, (255, 0, 0))
    go_rect = go_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(go_text, go_rect)

    restart_text = font.render("Press R to Restart or ESC to Exit", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(restart_text, restart_rect)

# === 스토리 화면 함수들 ===
def show_ending_story_1():
    # 엔딩 스토리: 아레인의 전투와 죽음
    story_lines = [
        "아레인은 영주, 사제, 드래곤과",
        "용맹하게 맞서 싸웠다.",
        "",
        "하지만 누적된 피로와 상처로 인해",
        "아레인은 결국 쓰러지게된다..."
    ]
    
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        
        y_offset = screen_height // 2 - (len(story_lines) * 30)
        for i, line in enumerate(story_lines):
            if line:
                text_surface = font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset + i * 60))
                screen.blit(text_surface, text_rect)
        
        instruction = small_font.render("Press ENTER to Continue", True, (150, 150, 150))
        instruction_rect = instruction.get_rect(center=(screen_width // 2, screen_height - 100))
        screen.blit(instruction, instruction_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
        
        pygame.display.update()
        clock.tick(60)

def show_ending_story_2():
    # 2차 엔딩 스토리: 몇 년 후...
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        
        # 큰 글자로 "몇년후..." 표시
        time_skip_font = pygame.font.Font(font_path, 100)
        text_surface = time_skip_font.render("몇년후...", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surface, text_rect)
        
        instruction = small_font.render("Press ENTER to Continue", True, (150, 150, 150))
        instruction_rect = instruction.get_rect(center=(screen_width // 2, screen_height - 100))
        screen.blit(instruction, instruction_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
        
        pygame.display.update()
        clock.tick(60)
    
    # 4_screen.py로 전환
    import subprocess
    import sys
    pygame.quit()
    subprocess.run(["python", "C:\\Users\\minih\\Desktop\\C'MON_6\\4_screen.py"])
    sys.exit()

# === 메인 루프 ===
while running:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 게임오버 상태에서 키 입력 처리
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                continue
            
            # 점프
            if event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE) and not jumping and not player_dying:
                jumping = True
                jump_start = current_time

        # 공격
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not player_dying and not game_over:
            if attack_cooldown == 0:
                character_motion = character_attack
                attack_start_time = current_time
                attack_cooldown = attack_cooldown_time

    # === 게임 오버 상태 처리 ===
    if game_over:
        draw_game_over(screen)
        pygame.display.update()
        continue
    
    # 이동
    keys = pygame.key.get_pressed()
    moving = False

    if not player_dying:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if character_x_pos > 0:
                character_x_pos -= character_speed
            moving = True
            facing = "left"

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if character_x_pos < screen_width - character_width:
                character_x_pos += character_speed
            moving = True
            facing = "right"
    
    # 걷기 애니메이션 업데이트
    if moving and character_motion == character_normal:
        walk_frame_counter += 1
        if walk_frame_counter >= WALK_FRAME_SPEED:
            walk_frame_counter = 0
            walk_frame = (walk_frame + 1) % 7
    else:
        walk_frame = 0
        walk_frame_counter = 0

    # Alt+F4 종료
    if keys[pygame.K_LALT] and keys[pygame.K_F4]:
        running = False

    # === 점프 처리 ===
    if jumping:
        elapsed = current_time - jump_start
        if elapsed < jump_duration:
            progress = elapsed / jump_duration
            jump_top = ground_y - character_height + 1 - ((ground_y - character_height + 1) - jump_peak) * (progress * 2) if progress <= 0.5 else jump_peak + ((ground_y - character_height + 1) - jump_peak) * ((progress - 0.5) * 2)
            character_y_pos = jump_top
        else:
            jumping = False
            character_y_pos = ground_y - character_height + 1
    else:
        character_y_pos = ground_y - character_height + 1

    # 공격 모션 종료
    if character_motion == character_attack and current_time - attack_start_time > attack_duration:
        character_motion = character_normal
        attack_hit = False
        attack_frame = 0
        attack_frame_counter = 0

    # 공격 쿨타임 감소
    if attack_cooldown > 0:
        attack_cooldown -= dt
        if attack_cooldown < 0:
            attack_cooldown = 0

    # 공격 애니메이션 프레임 업데이트
    if character_motion == character_attack:
        elapsed_attack = current_time - attack_start_time
        attack_frame = int((elapsed_attack / attack_duration) * 7) % 7

    # === 드래곤 업데이트 ===
    if dragon is not None:
        dragon.update(character_x_pos, character_y_pos, fireballs)
        if dragon.hp <= 0 and not dragon_defeated:
            dragon.alive = False
            dragon_defeated = True
            player_dying = True
            dying_start_time = current_time
    
    # === 드래곤 처치 후 플레이어 사망 연출 ===
    if player_dying and not player_disappeared:
        # 드래곤 처치 후 2초 대기
        elapsed_since_defeat = current_time - dying_start_time
        if elapsed_since_defeat >= 2000:  # 2초 대기
            # HP를 점진적으로 감소 (1초당 30씩)
            hp = max(0, hp - 0.5)
            
            # HP가 0이 되면 캐릭터 사라짐
            if hp <= 0:
                show_character = False
                if not player_disappeared:
                    player_disappeared = True
                    dying_start_time = current_time  # 사라진 시간 기록
    
    # === 캐릭터가 사라진 후 3초 대기 후 스토리 화면 ===
    if player_disappeared:
        elapsed_since_disappear = current_time - dying_start_time
        if elapsed_since_disappear >= disappear_wait_time:
            show_ending_story_1()
            show_ending_story_2()
            running = False
            continue
    
    # === HP 0으로 일반 게임오버 체크 (드래곤 처치 후가 아닌 경우) ===
    if hp <= 0 and not dragon_defeated and not game_over:
        game_over = True
    
    # === 불꽃 업데이트 ===
    for fireball in fireballs[:]:
        fireball.update()
        if not fireball.alive:
            fireballs.remove(fireball)
        elif not fireball.hit:
            # 플레이어와 충돌 체크 
            player_hitbox_width = character_width * 0.6
            player_hitbox_height = character_height * 0.6
            player_hitbox_offset_x = (character_width - player_hitbox_width) / 2
            player_hitbox_offset_y = (character_height - player_hitbox_height) / 2
            player_rect = pygame.Rect(
                character_x_pos + player_hitbox_offset_x,
                character_y_pos + player_hitbox_offset_y,
                player_hitbox_width,
                player_hitbox_height
            )
            hitbox_width = fire_width * 0.25
            hitbox_height = fire_height * 0.25
            fire_rect = pygame.Rect(fireball.x + hitbox_width * 0.5, fireball.y + hitbox_height * 0.5, hitbox_width, hitbox_height)
            if player_rect.colliderect(fire_rect):
                hp = max(0, hp - 20)
                fireball.hit = True
                fireball.alive = False
    
    # === 플레이어 공격 판정 ===
    if character_motion == character_attack and not attack_hit and not player_dying:
        elapsed_attack = current_time - attack_start_time
        if elapsed_attack < attack_duration:
            attack_range = character_width * 1.5
            if facing == "right":
                attack_x = character_x_pos + character_width
            else:
                attack_x = character_x_pos - attack_range
            attack_y = character_y_pos + character_height * 0.3
            attack_rect = pygame.Rect(attack_x, attack_y, attack_range, character_height * 0.4)
            
            # 드래곤 충돌 감지
            if dragon is not None and dragon.alive:
                dragon_rect = pygame.Rect(dragon.x, dragon.y, dragon.width, dragon.height)
                if attack_rect.colliderect(dragon_rect):
                    dragon.hp -= 3
                    attack_hit = True
                    if dragon.hp <= 0:
                        dragon.alive = False
            
    # === 화면 그리기 ===
    screen.blit(altar, (0, 0))

    # 캐릭터 그리기
    if show_character:
        # 상태 결정
        if character_motion == character_attack:
            state = "attack"
            frame = attack_frame
        elif jumping:
            state = "jump"
            frame = walk_frame
        else:
            state = "walk"
            frame = walk_frame
        
        img = get_player_frame(frame, facing_dir=facing, state=state)
        char_scaled = pygame.transform.scale(img, (character_width, character_height))
        screen.blit(char_scaled, (character_x_pos, character_y_pos))
        name_text = small_font.render("아레인", True, (255, 255, 255))
        screen.blit(name_text, (character_x_pos, character_y_pos - 30))

    # 드래곤 그리기
    if dragon is not None and dragon.alive and dragon.hp > 0:
        dragon.draw(screen)
    
    # 불꽃 그리기
    for fireball in fireballs:
        fireball.draw(screen)

    # HP
    if show_hp:
        hp_text = font.render(f"HP: {hp}/{max_hp}", True, (255, 0, 0))
        screen.blit(hp_text, (20, 20))
        bar_width = 200
        bar_height = 20
        fill = (hp / max_hp) * bar_width
        pygame.draw.rect(screen, (255, 0, 0), (20, 60, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (20, 60, fill, bar_height))

    # 공격 쿨타임 바 표시
    if attack_cooldown > 0:
        bar_width = 120
        bar_height = 12
        x, y = 20, 130
        pygame.draw.rect(screen, (180, 180, 180), (x, y, bar_width, bar_height), 1)
        fill = bar_width * (1 - attack_cooldown / attack_cooldown_time)
        pygame.draw.rect(screen, (0, 200, 255), (x, y, fill, bar_height))
        cooldown_text = small_font.render("Attack Cooldown", True, (0, 200, 255))
        screen.blit(cooldown_text, (x + bar_width + 10, y - 2))

    pygame.display.update()

pygame.quit()
