# ====== 전설의 농부 - 메인 게임 (씬 1-3) ======
import pygame
import os
pygame.init()

# ====== 씬 번호 ======
Game_Scene = 0  # 0: 시작 스토리, 1: 메인 게임 (scene 1-3), 2: 엔딩 스토리

# ====== 화면 설정 ======
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("전설의 농부")

# ====== 폰트 설정 ======
font_path = os.path.join("C:\\Users\\minih\\Desktop\\C'MON_6\\NanumGothic.ttf")
font = pygame.font.Font(font_path, 40)
large_font = pygame.font.Font(font_path, 80)
title_font = pygame.font.Font(font_path, 120)
small_font = pygame.font.Font(font_path, 25)

# ====== 배경 이미지 ======
houses = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\houses.png")
Trees = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\Trees.png")
forest_castle = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\forest_castle.png")
houses = pygame.transform.scale(houses, (screen_width, screen_height))
Trees = pygame.transform.scale(Trees, (screen_width, screen_height))
forest_castle = pygame.transform.scale(forest_castle, (screen_width, screen_height))

# ====== 캐릭터 이미지 ======
sprite_sheet = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\player.png").convert_alpha()
player_attack_img = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\player_attack.png").convert_alpha()
SPRITE_COLS = 7
SPRITE_ROWS = 4
FRAME_WIDTH = sprite_sheet.get_width() // SPRITE_COLS
FRAME_HEIGHT = sprite_sheet.get_height() // SPRITE_ROWS

weapon_img = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\weapon.png")
weapon_size = weapon_img.get_rect().size
weapon_width, weapon_height = int(weapon_size[0] * 1.8), int(weapon_size[1] * 1.8)
weapon_img = pygame.transform.scale(weapon_img, (weapon_width, weapon_height))
weapon_x_pos = 400  # Scene 1의 무기 위치
weapon_y_pos = screen_height - weapon_height - 30
weapon_owned = False  # 무기 소유 여부
weapon_pickup_distance = 100  # 무기 주울 수 있는 거리

# ====== 기사단 이미지 ======
knight_img = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\KnightSquad.png").convert_alpha()
KNIGHT_COLS = 3
KNIGHT_ROWS = 4
KNIGHT_FRAME_WIDTH = knight_img.get_width() // KNIGHT_COLS
KNIGHT_FRAME_HEIGHT = knight_img.get_height() // KNIGHT_ROWS

# ====== 영주 이미지 ======
lord_img = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\lord.png").convert_alpha()

# ====== 주민 이미지 ======
resident_img = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\resident1.png")
resident_width, resident_height = 128, 128
resident_img = pygame.transform.scale(resident_img, (resident_width, resident_height))
resident_x_pos = 700
resident_y_pos = screen_height - resident_height
show_resident = True
resident_interacted = False

character_width = int(FRAME_WIDTH * 5)
character_height = int(FRAME_HEIGHT * 5)

# === 몬스터 크기 ===
enemy_width = int(FRAME_WIDTH * 2)
enemy_height = int(FRAME_HEIGHT * 2)

# === 기사단 크기 ===
knight_width = int(FRAME_WIDTH * 3)
knight_height = int(FRAME_HEIGHT * 3)

# === 영주 크기 ===
lord_width = int(FRAME_WIDTH * 4)
lord_height = int(FRAME_HEIGHT * 4)

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

# === 스프라이트 시트에서 프레임 추출 함수 ===
def get_player_frame(frame_index, facing_dir="right", is_attacking=False):
    col = frame_index % 7
    if is_attacking:
        row = 0 if facing_dir == "right" else 1
    else:
        row = 0 if facing_dir == "right" else 1
    rect = pygame.Rect(col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)
    return sprite_sheet.subsurface(rect)

# === 공격 이미지에서 프레임 추출 함수 ===
def get_attack_frame(frame_index, facing_dir="right"):
    #player_attack_img 스프라이트 시트에서 프레임 추출 (7x6 그리드)
    attack_frame_width = player_attack_img.get_width() // 7
    attack_frame_height = player_attack_img.get_height() // 6
    col = frame_index % 7
    row = 0 if facing_dir == "right" else 1
    
    # 범위 체크
    x = col * attack_frame_width
    y = row * attack_frame_height
    
    rect = pygame.Rect(x, y, attack_frame_width, attack_frame_height)
    try:
        return player_attack_img.subsurface(rect)
    except:
        # 범위 오류 시 첫 번째 프레임 반환
        return player_attack_img.subsurface(pygame.Rect(0, 0, attack_frame_width, attack_frame_height))

# === 무기 소유 시 프레임 추출 함수 ===
def get_weapon_frame(frame_index, facing_dir="right", state="walk"):
    #weapon_owned일 때 player_attack_img에서 프레임 추출 (7x6 그리드)
    attack_frame_width = player_attack_img.get_width() // 7
    attack_frame_height = player_attack_img.get_height() // 6
    col = frame_index % 7

    # state와 facing_dir에 따라 row 결정
    if state == "walk":
        row = 0 if facing_dir == "right" else 1
    elif state == "jump":
        row = 2 if facing_dir == "right" else 3
    elif state == "attack":
        row = 4 if facing_dir == "right" else 5
    else:
        row = 0

    x = col * attack_frame_width
    y = row * attack_frame_height

    rect = pygame.Rect(x, y, attack_frame_width, attack_frame_height)
    try:
        return player_attack_img.subsurface(rect)
    except:
        return player_attack_img.subsurface(pygame.Rect(0, 0, attack_frame_width, attack_frame_height))

# === 기사단 프레임 추출 함수 ===
def get_knight_frame(frame_index, facing_dir="right", is_attacking=False):
    """기사단 스프라이트 시트에서 프레임 추출 (3x4 그리드)
    1행: 왼쪽 이동, 2행: 오른쪽 이동, 3행: 왼쪽 점프, 4행: 오른쪽 점프
    """
    col = frame_index % KNIGHT_COLS
    
    if is_attacking:
        # 공격(점프) 프레임
        row = 2 if facing_dir == "left" else 3
    else:
        # 이동 프레임
        row = 0 if facing_dir == "left" else 1
    
    x = col * KNIGHT_FRAME_WIDTH
    y = row * KNIGHT_FRAME_HEIGHT
    
    rect = pygame.Rect(x, y, KNIGHT_FRAME_WIDTH, KNIGHT_FRAME_HEIGHT)
    try:
        return knight_img.subsurface(rect)
    except:
        return knight_img.subsurface(pygame.Rect(0, 0, KNIGHT_FRAME_WIDTH, KNIGHT_FRAME_HEIGHT))

# === Entity 기본 클래스 ===
class Entity:
    def __init__(self, x, y, width, height, hp, color, gravity=1, speed=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp
        self.color = color
        self.vel_y = 0
        self.gravity = gravity
        self.speed = speed
        self.alive = True

    def draw(self, screen, hp_label="HP"):
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), self.width, self.height))
        hp_text = font.render(f"{hp_label}:{self.hp}", True, (255,255,255))
        screen.blit(hp_text, (int(self.x), int(self.y) - 22))

# === KnightSquad 클래스 ===
class KnightSquad(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, knight_width, knight_height, 30, (80, 80, 200))
        self.state = "patrol"
        self.home_x = x
        self.patrol_speed = 2
        self.patrol_dir = 1
        self.patrol_distance = 0
        self.patrol_move_distance = 30
        self.chase_range = 400
        self.attack_range = knight_width * 1.2
        self.charge_speed = 6
        self.attack_damage = 1
        self.attack_cooldown = 0
        self.attack_cooldown_time = 90
        self.attack_timer = 0
        self.attack_duration = 18
        self.vel_x = 0
        # 애니메이션 변수
        self.frame_index = 0
        self.frame_counter = 0
        self.frame_speed = 8
        self.facing_dir = "right"

    def update(self, px, py):
        if not self.alive:
            return

        dx = px - self.x
        dist = (dx*dx + (py - self.y)*(py - self.y))**0.5

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.vel_x = 0

        if self.state == "patrol":
            if dist < self.chase_range:
                self.state = "chase"
            else:
                self.vel_x = self.patrol_dir * self.patrol_speed
                self.patrol_distance += abs(self.vel_x)
                if self.patrol_distance >= self.patrol_move_distance:
                    self.patrol_distance = 0
                    self.patrol_dir *= -1

        elif self.state == "chase":
            if dist > self.chase_range * 1.1:
                self.state = "patrol"
                self.patrol_distance = 0
            else:
                if dx > 0:
                    move_dir = 1
                else:
                    move_dir = -1
                self.vel_x = move_dir * self.patrol_speed * 1.5
                if abs(dx) < self.attack_range and self.attack_cooldown <= 0:
                    self.state = "attack"
                    self.attack_timer = self.attack_duration
                    self.attack_cooldown = self.attack_cooldown_time

        elif self.state == "attack":
            if dx > 0:
                move_dir = 1
            else:
                move_dir = -1
            self.vel_x = move_dir * self.charge_speed
            if self.attack_timer > 0:
                self.attack_timer -= 1
                attack_width = knight_width * 1.4
                attack_height = knight_height * 0.6
                attack_x = self.x + (self.width if move_dir > 0 else -attack_width)
                attack_y = self.y + self.height * 0.2
                attack_rect = pygame.Rect(int(attack_x), int(attack_y), int(attack_width), int(attack_height))
                player_rect = pygame.Rect(int(px), int(py), character_width, character_height)
                if attack_rect.colliderect(player_rect):
                    global hp
                    hp -= self.attack_damage
            else:
                self.state = "cooldown"

        elif self.state == "cooldown":
            if self.attack_cooldown <= 0:
                self.state = "chase"

        self.x += self.vel_x
        
        # 이동 방향에 따라 facing_dir 업데이트
        if self.vel_x > 0:
            self.facing_dir = "right"
        elif self.vel_x < 0:
            self.facing_dir = "left"
        
        # 애니메이션 프레임 업데이트 (이동 중일 때만)
        if abs(self.vel_x) > 0 or self.state == "attack":
            self.frame_counter += 1
            if self.frame_counter >= self.frame_speed:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % KNIGHT_COLS
        else:
            self.frame_index = 0
            self.frame_counter = 0

    def draw(self, screen):
        if not (self.alive and self.hp > 0):
            return
        # 공격 중이면 점프 프레임, 아니면 이동 프레임
        is_attacking = (self.state == "attack")
        knight_frame = get_knight_frame(self.frame_index, self.facing_dir, is_attacking)
        knight_scaled = pygame.transform.scale(knight_frame, (self.width, self.height))
        screen.blit(knight_scaled, (int(self.x), int(self.y)))
        
        # 기사단 이름 표시
        name_text = small_font.render("기사단", True, (255, 255, 255))
        screen.blit(name_text, (int(self.x), int(self.y) - 55))
        
        hp_text = small_font.render(f"HP: {self.hp}", True, (255, 255, 255))
        screen.blit(hp_text, (int(self.x), int(self.y) - 30))

# === Lord 클래스 ===
class Lord(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, lord_width, lord_height, 50, (128, 0, 128))
        self.state = "idle"
        self.jump_power = 19
        self.jump_velocity = 0
        self.attack_range = 500
        self.attack_cooldown = 0
        self.attack_cooldown_time = 60
        self.target_x = None
        self.target_y = None
        self.attack_hit = False
        self.initial_y = y

    def update(self, px=None, py=None):
        if not self.alive:
            return

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.state == "idle":
            if px is not None and py is not None:
                if abs(px - self.x) <= self.attack_range and py <= self.y and self.attack_cooldown == 0:
                    self.state = "jump_attack"
                    self.jump_velocity = -self.jump_power
                    self.target_x = px
                    self.target_y = self.initial_y
                    self.attack_hit = False

        elif self.state == "jump_attack":
            move_speed = 8
            if abs(self.x - self.target_x) > 4:
                if self.x < self.target_x:
                    self.x += min(move_speed, self.target_x - self.x)
                else:
                    self.x -= min(move_speed, self.x - self.target_x)
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity
            if self.jump_velocity > 0 and self.y >= self.target_y - lord_height:
                self.jump_velocity = self.jump_power * 1.5
            if self.jump_velocity > 0 and self.y >= self.target_y and not self.attack_hit:
                attack_width = enemy_width // 2
                attack_height = enemy_height // 2
                attack_x = self.x + (self.width // 2) - (attack_width // 2)
                attack_y = self.y + self.height - attack_height
                attack_rect = pygame.Rect(int(attack_x), int(attack_y), attack_width, attack_height)
                player_rect = pygame.Rect(int(px), int(py), character_width, character_height)
                if attack_rect.colliderect(player_rect):
                    global hp
                    hp = max(0, hp - 10)
                    self.attack_hit = True
                self.y = self.target_y
                self.state = "cooldown"
                self.attack_cooldown = self.attack_cooldown_time
            elif self.jump_velocity > 0 and self.y >= self.target_y and not self.attack_hit:
                self.y = self.target_y
                self.state = "cooldown"
                self.attack_cooldown = self.attack_cooldown_time

        elif self.state == "cooldown":
            if self.attack_cooldown == 0:
                self.state = "idle"

    def draw(self, screen):
        if not (self.alive and self.hp > 0):
            return
        lord_scaled = pygame.transform.scale(lord_img, (self.width, self.height))
        screen.blit(lord_scaled, (int(self.x), int(self.y)))
        
        # 영주 이름 표시
        name_text = small_font.render("영주", True, (255, 255, 255))
        screen.blit(name_text, (int(self.x), int(self.y) - 55))
        
        hp_text = small_font.render(f"HP: {self.hp}", True, (255, 255, 255))
        screen.blit(hp_text, (int(self.x), int(self.y) - 30))

# === 적 초기화 ===
enemies = []
knight_squad = None
lord = None
knight_defeated = False  # 기사단 처치 여부

# === HP 관련 ===
hp = 100
max_hp = 100

# === 점프 관련 ===
jumping = False
jump_start = 0
jump_duration = 500
jump_peak = screen_height - (screen_height // 4) - character_height

# === 앉기 관련 ===
original_height = character_height
crouch_height = int(character_height * 0.75)
current_height = original_height
crouching = False

# === 장면 관련 ===
scene = 1
scene_start = 0

# === 표시 상태 ===
show_character = True
show_hp = True

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

# === Resident 상호작용 상태 ===
interacting_with_resident = False

# === 텍스트 애니메이션 ===
display_resident_text = False
display_player_text = False
resident_text_index = 0
player_text_index = 0
text_interval = 3000
text_last_update = 0
character_can_move = True

# === 영주 대화 ===
display_player_lord_text = False
display_lord_dialogue = False
player_lord_text_index = 0
lord_dialogue_index = 0
lord_dialogue_started = False

running = True
clock = pygame.time.Clock()

# === 스토리 화면 함수 ===
def show_story_screen():
    #Game_Scene 0: 스토리 소개 화면
    global Game_Scene
    
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        
        # 타이틀
        title_text = title_font.render("전설의 농부", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, 120))
        screen.blit(title_text, title_rect)
        
        # 스토리 텍스트
        story_lines = [
            "한 마을에 아레인이라는 농부가 살고 있었습니다.",
            "",
            "영주는 마을 사람들로부터 많은 농사물을 거두어",
            "마을 사람들은 굶주림에 시달리고 있었습니다.",
            "",
            "아레인은 마을 사람들을 구하기 위해",
            "영주를 찾아가기로 결심합니다..."
        ]
        
        y_offset = 250
        for line in story_lines:
            if line:
                text = small_font.render(line, True, (200, 200, 200))
            else:
                text = small_font.render("", True, (0, 0, 0))
            text_rect = text.get_rect(center=(screen_width // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 40
        
        # 시작 안내
        start_text = font.render("ENTER를 눌러 시작하기", True, (255, 255, 100))
        start_rect = start_text.get_rect(center=(screen_width // 2, screen_height - 100))
        screen.blit(start_text, start_rect)
        
        # 조작 안내
        control_text = small_font.render("조작: 방향키/WASD - 이동, Space - 점프, F - 아이템 줍기, 마우스 클릭 - 공격", True, (150, 150, 150))
        control_rect = control_text.get_rect(center=(screen_width // 2, screen_height - 50))
        screen.blit(control_text, control_rect)
        
        pygame.display.flip()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    Game_Scene = 1
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    import sys
                    sys.exit()

# === 엔딩 스토리 화면 함수 ===
def show_ending_story():
    #Game_Scene 2: 영주 처치 후 엔딩 스토리
    global Game_Scene
    
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        
        # 타이틀
        title_text = large_font.render("영주를 쓰러트렸다!", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, 120))
        screen.blit(title_text, title_rect)
        
        # 엔딩 텍스트
        story_lines = [
            "레인은 영주를 쓰러트리고 마을을 구했습니다.",
            "",
            "하지만 성 밖에서 이상한 기운이 느껴집니다...",
            "",
            "사제가 나타났습니다!",
            "",
            "레인의 모험은 계속됩니다..."
        ]
        
        y_offset = 250
        for line in story_lines:
            if line:
                text = small_font.render(line, True, (200, 200, 200))
            else:
                text = small_font.render("", True, (0, 0, 0))
            text_rect = text.get_rect(center=(screen_width // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 40
        
        # 계속하기 안내
        continue_text = font.render("ENTER를 눌러 계속하기", True, (255, 255, 100))
        continue_rect = continue_text.get_rect(center=(screen_width // 2, screen_height - 80))
        screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    import sys
                    sys.exit()
    
    # 사냥꾼 대화 화면으로 전환
    show_hunter_scene()

# === 사냥꾼 대화 화면 함수 ===
def show_hunter_scene():
    """영주 처치 후 사냥꾼과 대화하는 장면"""
    # Trees 배경 로드
    trees_bg = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\Trees.png")
    trees_bg = pygame.transform.scale(trees_bg, (screen_width, screen_height))
    
    # 사냥꾼 이미지 로드
    hunter_img = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\hunter.png")
    hunter_width = 128
    hunter_height = 128
    hunter_img = pygame.transform.scale(hunter_img, (hunter_width, hunter_height))
    
    # 플레이어 위치
    player_x = 100
    player_y = screen_height - 160
    player_width = 160
    player_height = 160
    
    # 사냥꾼 위치
    hunter_x = screen_width // 2
    hunter_y = screen_height - hunter_height
    
    # 대화 상태
    display_hunter_text = False
    hunter_text_index = 0
    text_last_update = 0
    text_interval = 3000
    can_move = True
    interaction_started = False
    
    hunter_phrases = [
        "결국 영주를 쓰러트리고 사제와 드래곤이 배후에 있다는 것을 알았구나..",
        "이쪽으로 계속 가다보면 사제가 있는 곳으로 갈 수 있을거야.",
        "사제는 영주와 다르게 매우 강하니 조심하렴.."
    ]
    
    running = True
    facing_dir = "right"
    frame_idx = 0
    frame_counter = 0
    
    # 무기 장착 스프라이트 시트 사용
    SWORD_SPRITE_COLS = 7
    SWORD_SPRITE_ROWS = 6
    SWORD_FRAME_WIDTH = player_attack_img.get_width() // SWORD_SPRITE_COLS
    SWORD_FRAME_HEIGHT = player_attack_img.get_height() // SWORD_SPRITE_ROWS
    
    while running:
        clock.tick(60)
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    # 사냥꾼 근처에 있는지 확인
                    dist = abs(player_x - hunter_x)
                    if dist < 150 and not interaction_started:
                        interaction_started = True
                        display_hunter_text = True
                        hunter_text_index = 0
                        text_last_update = current_time
                        can_move = False
        
        # 대화 진행
        if display_hunter_text:
            if hunter_text_index < len(hunter_phrases):
                if current_time - text_last_update > text_interval:
                    hunter_text_index += 1
                    text_last_update = current_time
            if hunter_text_index >= len(hunter_phrases) and current_time - text_last_update > 3000:
                display_hunter_text = False
                can_move = True
        
        # 이동 처리
        if can_move:
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if player_x > 0:
                    player_x -= 5
                    facing_dir = "left"
                    frame_counter += 1
                    if frame_counter >= 5:
                        frame_counter = 0
                        frame_idx = (frame_idx + 1) % 7
            
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_x += 5
                facing_dir = "right"
                frame_counter += 1
                if frame_counter >= 5:
                    frame_counter = 0
                    frame_idx = (frame_idx + 1) % 7
                
                # 오른쪽 끝에 도달하면 2_screen.py로 전환
                if player_x >= screen_width:
                    running = False
        
        # 그리기
        screen.blit(trees_bg, (0, 0))
        
        # 사냥꾼 그리기
        screen.blit(hunter_img, (hunter_x, hunter_y))
        hunter_name = small_font.render("사냥꾼", True, (255, 255, 255))
        screen.blit(hunter_name, (hunter_x, hunter_y - 30))
        
        # 플레이어 그리기 (무기 장착 상태)
        row = 0 if facing_dir == "right" else 1
        col = frame_idx % 7
        rect = pygame.Rect(col * SWORD_FRAME_WIDTH, row * SWORD_FRAME_HEIGHT, SWORD_FRAME_WIDTH, SWORD_FRAME_HEIGHT)
        player_img = player_attack_img.subsurface(rect)
        player_scaled = pygame.transform.scale(player_img, (player_width, player_height))
        screen.blit(player_scaled, (player_x, player_y))
        
        player_name = small_font.render("아레인", True, (255, 255, 255))
        screen.blit(player_name, (player_x, player_y - 30))
        
        # E키 프롬프트 표시
        if not display_hunter_text and not interaction_started:
            dist = abs(player_x - hunter_x)
            if dist < 150:
                prompt = small_font.render("E를 눌러 대화하기", True, (255, 255, 255))
                prompt_rect = prompt.get_rect(center=(hunter_x + hunter_width // 2, hunter_y - 60))
                pygame.draw.rect(screen, (0, 0, 0), prompt_rect.inflate(20, 10))
                pygame.draw.rect(screen, (255, 255, 255), prompt_rect.inflate(20, 10), 2)
                screen.blit(prompt, prompt_rect)
        
        # 사냥꾼 대화 텍스트 (말풍선 형태)
        if display_hunter_text:
            idx = min(hunter_text_index, len(hunter_phrases) - 1)
            text_surface = small_font.render(hunter_phrases[idx], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(hunter_x + hunter_width // 2, hunter_y - 20))
            box_rect = text_rect.inflate(10, 10)
            pygame.draw.rect(screen, (0, 0, 0), box_rect)
            pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
            screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
    
    # while 루프 종료 후 2_screen.py로 전환
    import subprocess
    import sys
    pygame.quit()
    subprocess.run(["python", "C:\\Users\\minih\\Desktop\\C'MON_6\\2_screen.py"])
    sys.exit()

# === 게임 재시작 함수 (씬 2로 리셋) ===
def reset_to_scene_2():
    global scene, scene_start, character_x_pos, character_y_pos, hp, weapon_owned
    global jumping, jump_start, crouching, current_height
    global character_motion, attack_start_time, attack_hit, attack_frame, attack_frame_counter, attack_cooldown
    global walk_frame, walk_frame_counter, facing
    global show_hp, show_character, show_resident, enemies, knight_squad, lord
    global display_player_lord_text, display_lord_dialogue, player_lord_text_index, lord_dialogue_index, lord_dialogue_started
    global character_can_move, text_last_update, knight_defeated
    
    # 씬 2로 설정
    scene = 2
    scene_start = pygame.time.get_ticks()
    
    # 플레이어 위치 및 상태 초기화
    character_x_pos = 25
    character_y_pos = ground_y - character_height + 1
    hp = max_hp
    weapon_owned = True  # 무기는 이미 소유한 상태
    
    # 점프 및 앉기 초기화
    jumping = False
    jump_start = 0
    crouching = False
    current_height = original_height
    
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
    
    # 씬 표시 상태
    show_hp = True
    show_character = True
    show_resident = False
    
    # 적 초기화 (기사단 부활)
    enemies = []
    knight_squad = KnightSquad(screen_width * 0.7, ground_y - knight_height - 20)
    lord = None
    knight_defeated = False  # 기사단 부활
    
    # 대화 상태 초기화
    display_player_lord_text = False
    display_lord_dialogue = False
    player_lord_text_index = 0
    lord_dialogue_index = 0
    lord_dialogue_started = False
    character_can_move = True
    text_last_update = 0

# === 씬 업데이트 함수 ===
def update_scene_display():
    global show_hp, show_character, show_resident, enemies, knight_squad, lord
    if scene == 1:
        show_hp = True
        show_character = True
        if not resident_interacted:
            show_resident = True
        enemies = []
        knight_squad = None
        lord = None
    elif scene == 2:
        show_hp = True
        show_character = True
        show_resident = False
        enemies = []
        # 기사단이 아직 처치되지 않았다면 생성
        if not knight_defeated:
            knight_squad = KnightSquad(screen_width * 0.7, ground_y - knight_height - 20)
        else:
            knight_squad = None
        lord = None
    elif scene == 3:
        show_hp = True
        show_character = True
        show_resident = False
        enemies = []
        knight_squad = None
        lord = Lord(screen_width * 0.5, ground_y - lord_height + 1)
        # 영주 대화 초기화
        global display_player_lord_text, display_lord_dialogue, player_lord_text_index, lord_dialogue_index, lord_dialogue_started, character_can_move, text_last_update
        lord_dialogue_started = False
        display_player_lord_text = False
        display_lord_dialogue = False
        lord_dialogue_index = 0

# === 메인 루프 ===
# Game_Scene 0일 때 스토리 화면 표시
if Game_Scene == 0:
    show_story_screen()

while running:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()
    
    # Game_Scene 2일 때 엔딩 스토리 표시
    if Game_Scene == 2:
        show_ending_story()
    
    # Game_Scene 1이 아니면 게임 루프 실행 안 함
    if Game_Scene != 1:
        continue
    
    # HP가 0 이하면 게임 오버
    if hp <= 0:
        screen.fill((0, 0, 0))
        game_over_text = large_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(game_over_text, game_over_rect)
        
        restart_text = font.render("Press R to Restart or ESC to Exit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
        waiting_for_exit = True
        while waiting_for_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_to_scene_2()
                        waiting_for_exit = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        import sys
                        sys.exit()
            clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 점프
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE) and not jumping:
                jumping = True
                jump_start = current_time

        # 앉기
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                crouching = True
                current_height = crouch_height
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                crouching = False
                current_height = original_height

        # 공격
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if weapon_owned and attack_cooldown == 0:
                character_motion = character_attack
                attack_start_time = current_time
                attack_cooldown = attack_cooldown_time

        # 무기 주우기 (F 키)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            if scene == 1 and not weapon_owned:
                # 플레이어와 무기 사이 거리 계산
                dist_to_weapon = ((character_x_pos - weapon_x_pos) ** 2 + (character_y_pos - weapon_y_pos) ** 2) ** 0.5
                if dist_to_weapon < weapon_pickup_distance:
                    weapon_owned = True

    # 이동
    keys = pygame.key.get_pressed()
    moving = False

    if character_can_move and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
        if scene == 1:
            # Scene 1에서는 왼쪽으로 화면 밖으로 나가지 않도록 제한
            if character_x_pos > 0:
                character_x_pos -= character_speed
        else:
            character_x_pos -= character_speed
        moving = True
        facing = "left"

    if character_can_move and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        moving = True
        new_x = character_x_pos + character_speed
        
        # Scene 2에서 기사단이 살아있으면 화면 오른쪽 끝에서 막기
        if scene == 2 and knight_squad is not None and knight_squad.alive and knight_squad.hp > 0:
            if new_x + character_width > screen_width:
                new_x = screen_width - character_width
        
        character_x_pos = new_x
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
            # 무기 소유 시 또는 공격 중일 때는 character_height 사용
            h = character_height if (weapon_owned or character_motion == character_attack) else current_height
            # 점프 최고점은 바닥에서부터의 거리로 계산
            jump_top = ground_y - h + 1 - ((ground_y - h + 1) - jump_peak) * (progress * 2) if progress <= 0.5 else jump_peak + ((ground_y - h + 1) - jump_peak) * ((progress - 0.5) * 2)
            character_y_pos = jump_top
        else:
            jumping = False
            h = character_height if (weapon_owned or character_motion == character_attack) else current_height
            character_y_pos = ground_y - h + 1
    else:
        h = character_height if (weapon_owned or character_motion == character_attack) else current_height
        character_y_pos = ground_y - h + 1

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

    # 공격 애니메이션 프레임 업데이트 (경과 시간 기반)
    if character_motion == character_attack:
        elapsed_attack = current_time - attack_start_time
        # 공격 지속 시간 동안 0-6 프레임을 순환
        attack_frame = int((elapsed_attack / attack_duration) * 7) % 7

    # === 주민과의 충돌 및 대화 ===
    if scene == 1 and show_resident and character_can_move and not resident_interacted:
        if abs(character_x_pos - resident_x_pos) < 120:
            character_can_move = False
            display_resident_text = True
            resident_text_index = 0
            text_last_update = current_time
            resident_interacted = True

    # === 영주와의 대화 (scene 3 진입 시 자동 시작) ===
    if scene == 3 and not lord_dialogue_started:
        character_can_move = False
        display_player_lord_text = True
        player_lord_text_index = 0
        text_last_update = current_time
        lord_dialogue_started = True

    # === 텍스트 애니메이션 업데이트 ===
    if display_resident_text:
        resident_phrases = ["요즘 영주님이 농사물을 많이 거두셔서 힘들어..", "이러다가는 조만간 아사할 지경이라고!", "레인아.. 영주님을 막아서 우리 마을을 도와줘..!"]
        if resident_text_index < len(resident_phrases):
            if current_time - text_last_update > text_interval:
                resident_text_index += 1
                text_last_update = current_time
        if resident_text_index >= len(resident_phrases) and current_time - text_last_update > 3000:
            display_resident_text = False
            display_player_text = True
            player_text_index = 0
            text_last_update = current_time

    if display_player_text:
        player_phrase = "네!! 영주님께 가볼께요"
        # 한 번에 표시
        if current_time - text_last_update > 3000:
            display_player_text = False
            show_resident = False
            character_can_move = True

    # === 영주 대화 애니메이션 업데이트 ===
    if display_player_lord_text:
        player_lord_phrases = ["영주님.. 마을 사람들이 농사물을 너무 많이 거두어 먹지 못 하고 있습니다..", "농사물을 걷는 것을 조금 줄여주실 수 있을까요??"]
        if player_lord_text_index < len(player_lord_phrases):
            if current_time - text_last_update > text_interval:
                player_lord_text_index += 1
                text_last_update = current_time
        if player_lord_text_index >= len(player_lord_phrases) and current_time - text_last_update > 3000:
            display_player_lord_text = False
            display_lord_dialogue = True
            lord_dialogue_index = 0
            text_last_update = current_time

    if display_lord_dialogue:
        lord_phrase = "걷는 농사물을 줄여달라고?? 공물의 수를 줄일 수는 없지!!"
        # 한 번에 표시
        if current_time - text_last_update > 3000:
            display_lord_dialogue = False
            character_can_move = True

    # === 플레이어 공격 판정 ===
    if character_motion == character_attack and not attack_hit:
        elapsed_attack = current_time - attack_start_time
        if elapsed_attack < attack_duration:
            attack_range = character_width * 1.5
            if facing == "right":
                attack_x = character_x_pos + character_width
            else:
                attack_x = character_x_pos - attack_range
            attack_y = character_y_pos + character_height * 0.3
            attack_rect = pygame.Rect(attack_x, attack_y, attack_range, character_height * 0.4)
            
            # knight_squad 충돌 감지
            if knight_squad is not None and knight_squad.alive:
                knight_rect = pygame.Rect(knight_squad.x, knight_squad.y, knight_squad.width, knight_squad.height)
                if attack_rect.colliderect(knight_rect):
                    knight_squad.hp -= 3
                    attack_hit = True
                    if knight_squad.hp <= 0:
                        knight_squad.alive = False
                        knight_defeated = True  # 기사단 처치 표시
            
            # lord 충돌 감지
            if lord is not None and lord.alive:
                lord_rect = pygame.Rect(lord.x, lord.y, lord.width, lord.height)
                if attack_rect.colliderect(lord_rect):
                    lord.hp -= 3
                    attack_hit = True
                    if lord.hp <= 0:
                        lord.alive = False

    # === 적 업데이트 ===
    for enemy in enemies:
        enemy.update(character_x_pos, character_y_pos)
    if knight_squad is not None:
        knight_squad.update(character_x_pos, character_y_pos)
    if lord is not None:
        lord.update(character_x_pos, character_y_pos)
        if lord.hp <= 0:
            lord.alive = False
            # 영주 처치 시 엔딩 스토리로 전환
            Game_Scene = 2
    
    # === 씬 전환 로직 ===
    if character_x_pos > screen_width and scene == 1:
        scene = 2
        scene_start = current_time
        character_x_pos = 25 
        update_scene_display()
    
    # Scene 2에서 Scene 3으로 전환 (기사단을 쓰러트려야만 가능)
    if scene == 2 and character_x_pos > screen_width and current_time - scene_start > 1000:
        # 기사단이 죽었는지 확인
        if knight_squad is None or not knight_squad.alive or knight_squad.hp <= 0:
            scene = 3
            scene_start = current_time
            character_x_pos = 25
            update_scene_display()
    
    if character_x_pos < -character_width and scene == 3:
        scene = 2
        scene_start = current_time
        character_x_pos = screen_width - character_width - 25
        update_scene_display()
    if scene == 2 and character_x_pos < -character_width and current_time - scene_start > 1000:
        scene = 1
        scene_start = current_time
        character_x_pos = screen_width - character_width - 25
        update_scene_display()
    # Scene 1에서 왼쪽으로 나가는 조건 추가
    if character_x_pos < -character_width and scene == 1:
        scene = 2
        scene_start = current_time
        character_x_pos = screen_width - character_width - 25
        update_scene_display()
            
    # === 화면 그리기 ===
    if scene == 1:
        screen.blit(houses, (0, 0))
    elif scene == 2:
        screen.blit(Trees, (0, 0))
    elif scene == 3:
        screen.blit(forest_castle, (0, 0))

    # Scene 1에서 무기 표시
    if scene == 1 and not weapon_owned:
        screen.blit(weapon_img, (weapon_x_pos, weapon_y_pos))
        
        # 무기와의 거리 계산
        dist_to_weapon = ((character_x_pos - weapon_x_pos) ** 2 + (character_y_pos - weapon_y_pos) ** 2) ** 0.5
        
        # 가까우면 "F를 눌러 주우세요" 메시지 표시
        if dist_to_weapon < weapon_pickup_distance:
            pickup_text = small_font.render("F를 눌러 주우세요", True, (255, 255, 0))
            screen.blit(pickup_text, (int(weapon_x_pos - 50), int(weapon_y_pos - 60)))

    # 캐릭터 그리기
    if show_character:
        # 무기 소유 시
        if weapon_owned:
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
            
            # 무기 소유 시 항상 character_height 사용
            img = get_weapon_frame(frame, facing_dir=facing, state=state)
            char_scaled = pygame.transform.scale(img, (character_width, character_height))
        else:
            # 무기 없을 때 기존 방식
            if character_motion == character_normal:
                img = get_player_frame(walk_frame, facing_dir=facing, is_attacking=False)
                char_scaled = pygame.transform.scale(img, (character_width, current_height))
            else:
                img = get_attack_frame(attack_frame, facing_dir=facing)
                char_scaled = pygame.transform.scale(img, (character_width, character_height))

        screen.blit(char_scaled, (character_x_pos, character_y_pos))
        name_text = small_font.render("아레인", True, (255, 255, 255))
        screen.blit(name_text, (character_x_pos, character_y_pos - 30))

    # 주민 그리기
    if scene == 1 and show_resident:
        screen.blit(resident_img, (resident_x_pos, resident_y_pos))

    # 주민 텍스트
    if display_resident_text:
        resident_phrases = ["요즘 영주님이 농사물을 많이 거두셔서 힘들어..", "이러다가는 조만간 아사할 지경이라고!", "레인아.. 영주님을 막아서 우리 마을을 도와줘..!"]
        idx = min(resident_text_index, len(resident_phrases) - 1)
        text_surface = small_font.render(resident_phrases[idx], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(resident_x_pos + resident_width // 2, resident_y_pos - 20))
        box_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
        screen.blit(text_surface, text_rect)

    # 플레이어 텍스트
    if display_player_text:
        player_phrase = "네!! 영주님께 가볼께요"
        text_surface = small_font.render(player_phrase, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(character_x_pos + character_width // 2, character_y_pos - 20))
        box_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
        screen.blit(text_surface, text_rect)

    # 영주에게 말하는 플레이어 텍스트
    if display_player_lord_text:
        player_lord_phrases = [
            ["영주님.. 마을 사람들이 농사물을 너무 많이 거두어", "먹지 못 하고 있습니다.."],
            ["농사물을 걷는 것을 조금 줄여주실 수 있을까요??"]
        ]
        idx = min(player_lord_text_index, len(player_lord_phrases) - 1)
        
        # 텍스트 박스를 화면 하단 중앙에 고정 (300픽셀 위로)
        box_y = screen_height - 420
        current_phrases = player_lord_phrases[idx]
        
        # 여러 줄 텍스트를 위한 높이 계산
        line_height = 30
        total_height = len(current_phrases) * line_height + 20
        
        # 가장 긴 줄의 너비 계산
        max_width = 0
        for phrase in current_phrases:
            text_surface = small_font.render(phrase, True, (255, 255, 255))
            max_width = max(max_width, text_surface.get_width())
        
        # 박스 그리기
        box_rect = pygame.Rect(
            (screen_width - max_width - 20) // 2,
            box_y,
            max_width + 20,
            total_height
        )
        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
        
        # 각 줄 그리기
        for i, phrase in enumerate(current_phrases):
            text_surface = small_font.render(phrase, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_width // 2, box_y + 10 + i * line_height + line_height // 2))
            screen.blit(text_surface, text_rect)

    # 영주 대화 텍스트
    if display_lord_dialogue and lord is not None:
        lord_phrase = "걷는 농사물을 줄여달라고?? 공물을 줄일 수는 없지!!"
        box_y = screen_height - 420
        
        text_surface = small_font.render(lord_phrase, True, (255, 255, 255))
        text_width = text_surface.get_width()
        
        # 박스 그리기
        box_rect = pygame.Rect(
            (screen_width - text_width - 20) // 2,
            box_y,
            text_width + 20,
            40
        )
        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
        
        # 텍스트 그리기
        text_rect = text_surface.get_rect(center=(screen_width // 2, box_y + 20))
        screen.blit(text_surface, text_rect)

    # 적 그리기
    for enemy in enemies:
        if enemy.alive and enemy.hp > 0:
            enemy.draw(screen)
    if knight_squad is not None and knight_squad.alive and knight_squad.hp > 0:
        knight_squad.draw(screen)
    if lord is not None and lord.alive and lord.hp > 0:
        lord.draw(screen)

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