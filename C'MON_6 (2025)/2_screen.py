import pygame
import sys
import random

# ====== 전설의 농부 - 사제 전투 ======
import pygame
import random
import sys
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
title_font = pygame.font.Font(font_path, 120)
small_font = pygame.font.Font(font_path, 25)

# ====== 경로 설정 ======
base_path = "C:\\Users\\minih\\Desktop\\C'MON_6\\C'MON_6\\"
image_path = base_path + "Game_image_files\\"
character_path = base_path + "characters\\"

# ====== 배경 이미지 ======
background = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\altar.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# ====== 화살 이미지 ======

arrow_img = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\Arrow.png")

# ====== 스프라이트 시트 (플레이어) =====
base_sprite_sheet = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\player.png").convert_alpha()
sword_sprite_sheet = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\player_attack.png").convert_alpha()
SPRITE_COLS = 7

BASE_SPRITE_ROWS = 4
BASE_FRAME_WIDTH = base_sprite_sheet.get_width() // SPRITE_COLS
BASE_FRAME_HEIGHT = base_sprite_sheet.get_height() // BASE_SPRITE_ROWS
SWORD_SPRITE_ROWS = 6
SWORD_FRAME_WIDTH = sword_sprite_sheet.get_width() // SPRITE_COLS
SWORD_FRAME_HEIGHT = sword_sprite_sheet.get_height() // SWORD_SPRITE_ROWS
# ====== 보스 이미지 ======
boss_sprite_sheet = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\Boss.png").convert_alpha()
BOSS_COLS = 3
BOSS_ROWS = 4
BOSS_FRAME_WIDTH = boss_sprite_sheet.get_width() // BOSS_COLS
BOSS_FRAME_HEIGHT = boss_sprite_sheet.get_height() // BOSS_ROWS

def get_boss_image(direction, jumping, frame):
    if jumping:
        row = 2 if direction == -1 else 3
    else:
        row = 0 if direction == -1 else 1
    
    col = frame % BOSS_COLS
    rect = pygame.Rect(col * BOSS_FRAME_WIDTH, row * BOSS_FRAME_HEIGHT, BOSS_FRAME_WIDTH, BOSS_FRAME_HEIGHT)
    return boss_sprite_sheet.subsurface(rect)
    
def get_player_image(facing, jumping, frame, sword_equipped, sword_swing, jump_frame_count=6):
    row = 0
    col = 0
    
    if sword_equipped:
        sprite_sheet = sword_sprite_sheet
        frame_width = SWORD_FRAME_WIDTH
        frame_height = SWORD_FRAME_HEIGHT
        
        if sword_swing:
            row = 4 if facing == "right" else 5
            col = frame % 7
        elif jumping:
            row = 2 if facing == "right" else 3
            col = frame % jump_frame_count
        else:
            row = 0 if facing == "right" else 1
            col = frame % 7
    else:
        sprite_sheet = base_sprite_sheet
        frame_width = BASE_FRAME_WIDTH
        frame_height = BASE_FRAME_HEIGHT
        
        if jumping:
            row = 3 if facing == "right" else 2
            col = frame % jump_frame_count
        else:
            row = 0 if facing == "right" else 1
            col = frame % 7
    rect = pygame.Rect(col*frame_width, row*frame_height, frame_width, frame_height)
    return sprite_sheet.subsurface(rect)

# ====== 플레이어 변수 ======
player_size = 80  
PLAYER_SCALE = 1.0  
SWORD_PLAYER_SIZE = 160
player_x = 100
player_y = screen_height - player_size
facing = "right"
jumping = False
vertical_velocity = 0
player_hp = 15
max_hp = 15

player_speed = 5
jump_power = 20
gravity = 1

player_frame = 0
frame_counter = 0
FRAME_SPEED = 5

ground_y = screen_height - player_size

# ====== 검 관련 변수 ======
sword_equipped = True  
sword_swing = False
sword_hit = False
sword_cooldown_time = 60
sword_cooldown_timer = 0

# ====== 게임 상태 ======
arrows = []
game_over = False

# ====== Arrow 클래스 ======
class Arrow:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.size = 16
        self.speed = 8
        self.direction = direction
        self.active = True

    def update(self):
        if not self.active:
            return
        self.x += self.speed * self.direction
        if self.x < -100 or self.x > screen_width + 100:
            self.active = False

    def draw(self, screen):
        if not self.active:
            return
        
        arrow_width = self.size * 4
        arrow_height = self.size // 2
        arrow_x = self.x
        arrow_y = self.y + self.size * 2
        
        if self.direction == -1:
            arrow_x -= arrow_width

        if arrow_img:
            ARROW_SCALE = 8
            display_w = int(arrow_width * ARROW_SCALE)
            display_h = int(arrow_height * ARROW_SCALE)
            
            draw_x = arrow_x - (display_w - arrow_width) // 2
            draw_y = arrow_y - (display_h - arrow_height) // 2
            
            display_arrow = pygame.transform.scale(arrow_img, (display_w, display_h))
            
            if self.direction == 1:
                display_arrow = pygame.transform.flip(display_arrow, True, False)
            
            screen.blit(display_arrow, (draw_x, draw_y))
        else:
            pygame.draw.rect(screen, (255, 255, 0), (arrow_x, arrow_y, arrow_width, arrow_height))
        
        return pygame.Rect(arrow_x, arrow_y, arrow_width, arrow_height)

# ====== Boss 클래스 ======
class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 80
        self.hp = 40
        self.alive = True
        self.direction = random.choice([-1, 1])
        self.jumping = False
        self.vertical_velocity = 0
        self.jump_power = 18
        self.speed = 4
        self.gravity = 1
        self.jump_timer = 0
        self.move_timer = 0
        self.shoot_timer = 0
        
        self.frame = 0
        self.frame_counter = 0
        self.frame_speed = 10
        
        self.set_random_timers()
        self.set_random_shoot_timer()

    def set_random_timers(self):
        self.jump_timer = random.randint(30, 90)
        self.move_timer = random.randint(60, 90)
    
    def set_random_shoot_timer(self):
        self.shoot_timer = random.randint(18, 60)

    def start_jump(self):
        if not self.jumping:
            self.jumping = True
            self.vertical_velocity = -self.jump_power

    def shoot_arrow(self):
        start_x = self.x + self.size // 2
        start_y = self.y
        arrows.append(Arrow(start_x, start_y, -1))
        arrows.append(Arrow(start_x, start_y, 1))

    def update(self):
        if not self.alive:
            return
        
        # 중력 및 점프
        if self.jumping:
            self.vertical_velocity += self.gravity
            self.y += self.vertical_velocity
            
            if self.y >= screen_height - self.size:
                self.y = screen_height - self.size
                self.jumping = False
                self.vertical_velocity = 0
        else:
            if self.y < screen_height - self.size:
                self.jumping = True
                self.vertical_velocity = 0
            
            self.jump_timer -= 1
            if self.jump_timer <= 0:
                self.start_jump()
                self.set_random_timers()
                
            self.move_timer -= 1
            if self.move_timer <= 0:
                self.direction *= -1
                self.set_random_timers()
        
        # 이동
        new_x = self.x + self.speed * self.direction
        
        if new_x < 0 or new_x + self.size > screen_width:
            self.direction *= -1
            self.set_random_timers()
        else:
            self.x = new_x
        
        # 화살 발사
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_arrow()
            self.set_random_shoot_timer()

    def draw(self, screen):
        if not self.alive:
            return
        
        # 애니메이션
        self.frame_counter += 1
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.frame = (self.frame + 1) % 3

        if 'boss_sprite_sheet' in globals():
            boss_image = get_boss_image(self.direction, self.jumping, self.frame)
            
            BOSS_IMAGE_SCALE = 2.5
            display_width = int(self.size * BOSS_IMAGE_SCALE)
            display_height = int(self.size * BOSS_IMAGE_SCALE)
            
            draw_x = self.x - (display_width - self.size) // 2
            draw_y = self.y - (display_height - self.size) // 2.1
            
            boss_image = pygame.transform.scale(boss_image, (display_width, display_height))
            screen.blit(boss_image, (draw_x, draw_y))
        else:
            pygame.draw.rect(screen, (128, 0, 128), (int(self.x), int(self.y), self.size, self.size))
        
        # 사제 이름 표시
        name_text = small_font.render("사제", True, (255, 255, 255))
        screen.blit(name_text, (int(self.x), int(self.y) - 55))
        
        hp_text = small_font.render(f"HP: {self.hp}", True, (255, 255, 255))
        screen.blit(hp_text, (int(self.x), int(self.y) - 30))
        
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

# ====== 보스 초기화 ======
boss = Boss(screen_width * 0.7, screen_height - 80)

# ====== 게임 초기화 함수 ======
def reset_game():
    global player_x, player_y, facing, jumping, vertical_velocity, player_hp
    global sword_equipped, sword_swing, sword_hit, sword_cooldown_timer, arrows, boss, game_over
    global player_frame, frame_counter
    
    player_x = 100
    player_y = screen_height - player_size
    facing = "right"
    jumping = False
    vertical_velocity = 0
    player_hp = max_hp
    player_frame = 0
    frame_counter = 0

    sword_equipped = True 
    sword_swing = False
    sword_hit = False
    sword_cooldown_timer = 0
    
    arrows.clear()
    boss = Boss(screen_width * 0.7, screen_height - 80)
    
    game_over = False

# ====== 사제 처치 후 스토리 화면 ======
def show_priest_ending_story():
    story_lines = [
        "사제를 쓰러트렸다.",
        "",
        "하지만 아직 끝이 아니다.",
        "",
        "더 큰 위협이 기다리고 있다..."
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
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
        
        pygame.display.flip()
        clock.tick(60)
    
    # 3_screen.py로 전환
    import subprocess
    pygame.quit()
    subprocess.run(["python", "C:\\Users\\minih\\Desktop\\C'MON_6\\3_screen.py"])
    sys.exit()

# ====== 게임 오버 화면 ======
def draw_game_over(screen):
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    go_text = large_font.render("GAME OVER", True, (255, 0, 0))
    go_rect = go_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(go_text, go_rect)

    restart_text = font.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(restart_text, restart_rect)
def draw_game_over(screen):
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    go_text = large_font.render("GAME OVER", True, (255, 0, 0))
    go_rect = go_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(go_text, go_rect)

    restart_text = font.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(restart_text, restart_rect)

# ====== 시작 화면 ======
def start_screen():
    waiting = True
    
    while waiting:
        screen.fill((0, 0, 0))
        
        title = title_font.render("legendary farmer", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        screen.blit(title, title_rect)
        
        instruction = font.render("Press ENTER to Start", True, (150, 150, 150))
        instruction_rect = instruction.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(instruction, instruction_rect)

        controls = font.render("A/D 또는 ←/→: 이동, Space: 점프, E: 상호작용, Mouse Click: 공격", True, (100, 100, 100))
        controls_rect = controls.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(controls, controls_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

# ====== 메인 게임 루프 ======
def run_game():
    global player_x, player_y, facing, jumping, vertical_velocity, player_hp
    global sword_equipped, sword_swing, sword_hit, sword_cooldown_timer, arrows, boss, game_over
    global player_frame, frame_counter
    
    reset_game()
    
    running = True
    
    while running:
        clock.tick(60)
        
        # 게임 오버 확인
        if player_hp <= 0 and not game_over:
            game_over = True
        
        # 보스 처치 시 스토리 화면 표시
        if boss and not boss.alive:
            show_priest_ending_story()
            return
        
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    reset_game()
                    continue
                
                if event.key == pygame.K_ESCAPE:
                    if game_over:
                        return
                
                if not game_over:
                    if event.key == pygame.K_SPACE:
                        if not jumping:
                            jumping = True
                            vertical_velocity = -jump_power

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and sword_equipped and sword_cooldown_timer <= 0:
                    sword_swing = True
                    sword_hit = False
                    sword_cooldown_timer = sword_cooldown_time
                    player_frame = 0
                    frame_counter = 0

        # 게임 오버 상태 처리
        if game_over:
            draw_game_over(screen)
            pygame.display.flip()
            continue
        
        # 쿨다운 감소
        if sword_cooldown_timer > 0:
            sword_cooldown_timer -= 1.5
        
        # 이동
        keys = pygame.key.get_pressed()
        move_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -player_speed
            facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = player_speed
            facing = "right"

        new_x = player_x + move_x
        if 0 <= new_x <= screen_width - player_size:
            player_x = new_x

        # 점프 및 중력
        if jumping:
            vertical_velocity += gravity
            player_y += vertical_velocity
            
            if player_y >= ground_y:
                player_y = ground_y
                jumping = False
                vertical_velocity = 0
        else:
            if player_y < ground_y:
                jumping = True
                vertical_velocity = 0

        # 보스 업데이트
        if boss and boss.alive:
            boss.update()

        # 화살 업데이트
        for arrow in list(arrows):
            arrow.update()
            
            if arrow.active:
                arrow_width = arrow.size * 4
                arrow_height = arrow.size // 2
                arrow_x = arrow.x
                
                if arrow.direction == -1:
                    arrow_x -= arrow_width
                    
                arrow_rect = pygame.Rect(arrow_x, arrow.y + arrow.size * 2, arrow_width, arrow_height)
                player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
                
                if player_rect.colliderect(arrow_rect):
                    if player_hp > 0:
                        player_hp -= 1
                        arrow.active = False
            
            if not arrow.active:
                arrows.remove(arrow)

        # 애니메이션 업데이트
        if 'get_player_image' in globals():
            current_frame_count = 7
            
            if sword_swing and sword_equipped:
                current_frame_count = 7
                if player_frame == current_frame_count - 1 and frame_counter == FRAME_SPEED - 1:
                    sword_swing = False
                    player_frame = 0
                    frame_counter = 0
            elif jumping:
                current_frame_count = 6
            elif move_x != 0:
                current_frame_count = 7
            else:
                if not sword_swing:
                    player_frame = 0
                    frame_counter = 0
                
            if (move_x != 0 or jumping or (sword_swing and sword_equipped)):
                frame_counter += 1
                if frame_counter >= FRAME_SPEED:
                    frame_counter = 0
                    max_frame = 7 if sword_swing and sword_equipped else current_frame_count
                    player_frame = (player_frame + 1) % max_frame
            
            if sword_swing == False and player_frame != 0 and not jumping and move_x == 0:
                player_frame = 0
                frame_counter = 0

        # 그리기
        screen.blit(background, (0, 0))

        # 보스 그리기
        boss_rect = None
        if boss and boss.alive:
            boss_rect = boss.draw(screen)

        # 플레이어 그리기
        if 'get_player_image' in globals() and 'player_image_fallback' not in globals():
            player_image = get_player_image(facing, jumping, player_frame, sword_equipped, sword_swing)
            
            if sword_equipped:
                display_size = int(SWORD_PLAYER_SIZE * PLAYER_SCALE)
                x_adjust = (display_size - player_size) / 2
                y_adjust = (display_size - player_size) - 40
                screen_x = player_x - x_adjust
                screen_y = player_y - y_adjust
            else:
                display_size = int(player_size * PLAYER_SCALE)
                screen_x = player_x
                screen_y = player_y

            player_image = pygame.transform.scale(player_image, (display_size, display_size))
            screen.blit(player_image, (screen_x, screen_y))
            
            # 아레인 이름 표시
            player_name = small_font.render("아레인", True, (255, 255, 255))
            screen.blit(player_name, (player_x, player_y - 30))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_size, player_size))

        # 검 공격 충돌
        if sword_equipped and sword_swing:
            if facing == "right":
                sword_rect = pygame.Rect(player_x + player_size/2, player_y + player_size - player_size//3, player_size, player_size//5)
            else:
                sword_rect = pygame.Rect(player_x - player_size//2, player_y + player_size - player_size//3, player_size, player_size//5)

            if boss and boss.alive and not sword_hit and boss_rect:
                if sword_rect.colliderect(boss_rect):
                    boss.hp -= 3
                    sword_hit = True
                    if boss.hp <= 0:
                        boss.alive = False

        # 화살 그리기
        for arrow in arrows:
            arrow.draw(screen)

        # UI 그리기
        hp_text = font.render(f"HP: {player_hp}", True, (255, 0, 0))
        screen.blit(hp_text, (10, 10))
        
        # 쿨다운 바
        if sword_cooldown_timer > 0:
            cooldown_ratio = sword_cooldown_timer / sword_cooldown_time
            bar_width = 100
            bar_height = 10
            pygame.draw.rect(screen, (255, 0, 0), (screen_width - bar_width - 10, 10, bar_width, bar_height), 1)
            fill_width = bar_width * (1 - cooldown_ratio)
            pygame.draw.rect(screen, (0, 255, 0), (screen_width - bar_width - 10, 10, fill_width, bar_height))

        pygame.display.flip()

# ====== 메인 실행 ======
clock = pygame.time.Clock()
run_game()

pygame.quit()
sys.exit()
