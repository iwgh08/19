import pygame
# ====== 전설의 농부 - 엔딩 ======
import pygame
import sys
pygame.init()

# ====== 화면 설정 ======
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("전설의 농부 - 엔딩")

# ====== 폰트 설정 ======
font_path = "C:\\Users\\minih\\Desktop\\C'MON_6\\NanumGothic.ttf"
font = pygame.font.Font(font_path, 40)
large_font = pygame.font.Font(font_path, 80)
small_font = pygame.font.Font(font_path, 20)

# ====== 배경 이미지 ======
houses = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\houses.png")
lord_room = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\lord_room.png")
forest_castle = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\forest_castle.png")
desk = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\desk.png")

houses = pygame.transform.scale(houses, (screen_width, screen_height))
lord_room = pygame.transform.scale(lord_room, (screen_width, screen_height))
forest_castle = pygame.transform.scale(forest_castle, (screen_width, screen_height))
desk = pygame.transform.scale(desk, (screen_width, screen_height))
# ====== 캐릭터 이미지 ======
# 스프라이트 시트 로드
sprite_sheet = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\hunter_sprite.png").convert_alpha()
sheet_width = sprite_sheet.get_width()
sheet_height = sprite_sheet.get_height()

# 스프라이트 시트는 6행 3열
SPRITE_ROWS = 6
SPRITE_COLS = 3
frame_width = sheet_width // SPRITE_COLS
frame_height = sheet_height // SPRITE_ROWS

# 각 애니메이션 프레임 추출
def load_sprite_frames(row):
    frames = []
    for col in range(SPRITE_COLS):
        frame = sprite_sheet.subsurface(pygame.Rect(
            col * frame_width,
            row * frame_height,
            frame_width,
            frame_height
        ))
        frames.append(frame)
    return frames

# 애니메이션 프레임 로드
walk_left_frames = load_sprite_frames(0)   # 1행 - 왼쪽 이동
walk_right_frames = load_sprite_frames(1)  # 2행 - 오른쪽 이동
jump_left_frames = load_sprite_frames(2)   # 3행 - 왼쪽 점프
jump_right_frames = load_sprite_frames(3)  # 4행 - 오른쪽 점프
crouch_left_frames = load_sprite_frames(4) # 5행 - 왼쪽 앉기
crouch_right_frames = load_sprite_frames(5) # 6행 - 오른쪽 앉기

character_width, character_height = 128, 128  # 크기 조절 가능
character_x_pos = 50
character_y_pos = screen_height - character_height

# 애니메이션 상태
current_frame = 0
animation_speed = 100  # 밀리초
last_animation_update = 0
facing_right = True  # 캐릭터가 바라보는 방향

# ====== 주민 이미지 ======
resident_img = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\characters\\resident2.png")
resident_width, resident_height = 128, 128  # 크기 조절 가능
resident_img = pygame.transform.scale(resident_img, (resident_width, resident_height))
resident_x_pos = 768
resident_y_pos = screen_height - resident_height
show_resident = True
resident_interacted = False

# ====== 집 이미지 ======
house = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\house.png")
house_width, house_height = 600, 600
house = pygame.transform.scale(house, (house_width, house_height))
house_x_pos = screen_width - house_width + 100
house_y_pos = screen_height - house_height
show_house = False


#====== 책 이미지 ======
book = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\book_outside.png")
book_width, book_height = 700,450
book = pygame.transform.scale(book, (book_width, book_height))
book_x_pos = (screen_width + book_width-200)//2 - 300
book_y_pos = (screen_height - book_height)//2
show_book = False
bookinside = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\book_inside_2.png")
bookinside = pygame.transform.scale(bookinside, (2050, 950))
bookinside_rect = bookinside.get_rect(center=(screen_width // 2, screen_height // 2))
bookcover = pygame.image.load("C:\\Users\\minih\\Desktop\\C'MON_6\\Game_image_files\\book_inside_1.png")
bookcover = pygame.transform.scale(bookcover, (1150, 700))
bookcover_rect = bookcover.get_rect(center=(screen_width // 2, screen_height // 2))

# === HP ===
hp = 100
max_hp = 100
font = pygame.font.Font("C:\\Users\\minih\\Desktop\\C'MON_6\\NanumGothic.ttf", 40)
show_hp = True

# === 점프/앉기 ===
jumping = False
jump_start = 0
jump_duration = 500
jump_peak = screen_height - (screen_height // 4) - character_height
original_height = character_height
crouch_height = int(character_height * 0.75)
current_height = original_height
crouching = False

# === 장면/모션 ===
scene = 1
scene_start = 0
show_character = True
character_normal = "normal"
character_attack = "attack"
character_motion = character_normal
attack_duration = 300
attack_start_time = 0

# === 텍스트 애니메이션 ===
display_resident_text = False
display_hunter_text = False
resident_index = 0
hunter_index = 0
text_interval = 300
text_last_update = 0
character_can_move = True
# === book inside 스토리 (scene 5) ===
story_lines = [
    "이것은 한 농부가 전설이 되기까지의 이야기이다.",
    "그의 이야기는 끝났지만,",
    "세상은 그가 남긴 불씨 위에서 다시 움직이기 시작했다.",
    "",
    "붉게 물들었던 하늘은 다시 푸르게 열리고,",
    "사람들은 그가 지켜낸 땅 위에서 새로운 하루를 살아간다.",
    "",
    "그의 이름은 언젠가 사라지겠지만,",
    "그가 남긴 선택은 영원히 남을 것이다.",
    "",
    "이곳에서 그의 이야기는 막을 내렸다.",
    "그리고 지금,",
    "그들이 써 내려갈 새로운 이야기가 쓰여질 것이다"
]

story_font = pygame.font.Font("C:\\Users\\minih\\Desktop\\C'MON_6\\NanumGothic.ttf",20)
story_font.set_bold(True)
story_line_index = 0
story_char_index = 0
story_typing = False
story_last_time = 0
story_speed = 40


# === 씬 업데이트 함수 ===
def update_scene_display():
    global show_hp, show_house, show_character, show_resident
    if scene == 1:
        show_hp = True
        show_house = False
        show_character = True
        show_resident = True
        

    elif scene == 2:
        show_hp = False
        show_house = False
        show_character = False
        show_resident = False
    elif scene == 3:
        show_hp = True
        show_house = True
        show_character = True
        show_resident = False
    elif scene == 4:
        show_hp = False
        show_house = False
        show_character = False
        show_resident = False
        show_book = True
    elif scene == 5:
        show_hp = False
        show_house = False
        show_character = False
        show_resident = False
        show_book = False

fade_surface = pygame.Surface((screen_width, screen_height))
fade_surface.fill((0, 0, 0))
fade_alpha = 0
fading = False
fade_direction = 1
fade_speed = 6
next_scene = None
book_alpha = 0
book_fade_speed = 10


def start_fade(target_scene):
    global fading, fade_alpha, fade_direction, next_scene
    fading = True
    fade_alpha = 0
    fade_direction = 1
    next_scene = target_scene

# === 메인 루프 ===
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE) and not jumping and scene != 5:
                jumping = True
                jump_start = current_time
            if event.key in (pygame.K_DOWN, pygame.K_s):
                crouching = True
                current_height = crouch_height
                # Enter → scene 4 → fade → scene 5
            if event.key == pygame.K_RETURN:
                if scene == 4 and not fading:
                    start_fade(5)
            if event.key == pygame.K_SPACE and scene == 5:
                if story_typing:
                    pass
                if story_line_index < len(story_lines):
                    story_typing = True
                    story_char_index = 0
                    story_last_time = current_time

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                crouching = False
                current_height = original_height


    # --- 캐릭터 이동 ---
    keys = pygame.key.get_pressed()
    moving = False
    if character_can_move:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            character_x_pos -= character_speed
            moving = True
            facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            moving = True
            facing_right = True
            if show_resident:
                max_x = resident_x_pos - 100
                if character_x_pos < max_x:
                    character_x_pos += character_speed
            elif scene == 3:
                max_x = house_x_pos + 85
                if character_x_pos < max_x:
                    character_x_pos += character_speed
            else:
                character_x_pos += character_speed

    # 점프 처리
    if jumping:
        elapsed = current_time - jump_start
        if elapsed < jump_duration:
            progress = elapsed / jump_duration
            if progress <= 0.5:
                character_y_pos = (screen_height - original_height) - ((screen_height - original_height) - jump_peak) * (progress * 2)
            else:
                character_y_pos = jump_peak + ((screen_height - original_height) - jump_peak) * ((progress - 0.5) * 2)
        else:
            jumping = False
            character_y_pos = screen_height - original_height
    else:
        character_y_pos = screen_height - current_height

    # 공격 모션 종료


    # --- 장면 전환 ---
    if character_x_pos > screen_width and scene == 1:
        scene = 3
        scene_start = current_time
        update_scene_display()
        character_x_pos = 25
    if scene == 2 and character_x_pos > screen_width and current_time - scene_start > 1000:
        scene = 3
        scene_start = current_time
        character_x_pos = 25
        update_scene_display()
    if character_x_pos < -character_width and scene == 3:
        scene = 1
        scene_start = current_time
        update_scene_display()
    if scene == 3 and character_x_pos < -character_width and current_time - scene_start > 1000:
        scene = 1
        scene_start = current_time
        character_x_pos = 25
        update_scene_display()

    # --- 주민과 충돌 ---
    # --- 주민과 충돌 (1회성) ---
    if scene == 1 and show_resident and character_can_move and not resident_interacted:
        if (resident_x_pos - 160) < character_x_pos < (resident_x_pos - 150):
            character_x_pos = resident_x_pos - 150
            display_resident_text = True
            resident_index = 0
            text_last_update = current_time
            character_can_move = False
            resident_interacted = True   # ✅ 여기!

    # --- 캐릭터 속도 조절 ---
    character_speed = 3  # 기본값 먼저 고정


    # --- 애니메이션 프레임 업데이트 ---
    if current_time - last_animation_update > animation_speed:
        current_frame = (current_frame + 1) % SPRITE_COLS
        last_animation_update = current_time
    if crouching:
        character_speed *= 0.5


    
    # === scene 5 스토리 타이핑 처리 ===
    if scene == 5 and story_typing:
        if story_line_index < len(story_lines):
            if current_time - story_last_time > story_speed:
                story_char_index += 1
                story_last_time = current_time

                if story_char_index >= len(story_lines[story_line_index]):
                    story_typing = False
                    story_line_index += 1


    
    
    #=== 추가화면전환 ===
    if scene == 3 and character_x_pos >= house_x_pos - 50 and not fading:
        start_fade(2)

    if scene == 2 and current_time - scene_start > 1000 and not fading:
        start_fade(4)
        show_book = True
    if scene == 4 and show_book:
        if book_alpha < 255:
            book_alpha += book_fade_speed
            if book_alpha > 255:
                book_alpha = 255


    # --- 화면 그리기 ---
    if scene == 1:
        screen.blit(houses, (0, 0))
    elif scene == 2:
        screen.blit(lord_room, (0, 0))
    elif scene == 3:
        screen.blit(forest_castle, (0, 0))
    elif scene == 4:
        screen.blit(desk, (0, 0))
        screen.blit(book, (book_x_pos, book_y_pos))
    elif scene == 5:
        screen.blit(desk, (0, 0))
        show_book = False
        screen.blit(bookcover, bookcover_rect)
        screen.blit(bookinside, bookinside_rect)
    if scene == 5:
        text_x = screen_width/2 + 25
        text_y = bookinside_rect.top + 195
        line_gap = 40

        for i in range(story_line_index):
            line_surface = story_font.render(story_lines[i], True, (0,0,0))
            screen.blit(line_surface, (text_x, text_y + i * line_gap))
            

        if story_typing and story_line_index < len(story_lines):
            partial = story_lines[story_line_index][:story_char_index]
            line_surface = story_font.render(partial, True, (0, 0, 0))
            screen.blit(line_surface, (text_x, text_y + story_line_index * line_gap))


    if show_house:
        screen.blit(house, (house_x_pos, house_y_pos))


    if scene == 4 and show_book:
        info_text = small_font.render("> 진행을 위해 Enter 키를 눌러주세요", True, (255, 255, 255))

        # HP 위치 기준 (좌상단)
        info_rect = info_text.get_rect(topleft=(20, 20))
        box_rect = info_rect.inflate(10, 10)

        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
        screen.blit(info_text, info_rect)

    # 캐릭터
    if show_character:
        # 애니메이션 프레임 선택
        if jumping:
            if facing_right:
                current_animation = jump_right_frames
            else:
                current_animation = jump_left_frames
        elif crouching:
            if facing_right:
                current_animation = crouch_right_frames
            else:
                current_animation = crouch_left_frames
        else:
            if moving:
                if facing_right:
                    current_animation = walk_right_frames
                else:
                    current_animation = walk_left_frames
            else:
                # 정지 상태일 때는 첫 번째 프레임 사용
                if facing_right:
                    current_animation = walk_right_frames
                else:
                    current_animation = walk_left_frames
                current_frame = 0
        
        # 현재 프레임 가져오기
        character_img = current_animation[current_frame]
        
        if current_height != character_height:
            scaled_char = pygame.transform.scale(character_img, (character_width, current_height))
            screen.blit(scaled_char, (character_x_pos, character_y_pos))
        else:
            scaled_char = pygame.transform.scale(character_img, (character_width, character_height))
            screen.blit(scaled_char, (character_x_pos, character_y_pos))
        
        # 사냥꾼 이름 표시
        hunter_name = small_font.render("사냥꾼", True, (255, 255, 255))
        screen.blit(hunter_name, (character_x_pos, character_y_pos - 30))


    # 주민
    if show_resident:
        screen.blit(resident_img, (resident_x_pos, resident_y_pos))
        # 거주민 이름 표시
        resident_name = small_font.render("거주민", True, (255, 255, 255))
        screen.blit(resident_name, (resident_x_pos, resident_y_pos - 30))

    # --- 주민 텍스트 ---
    if display_resident_text:
        resident_font = pygame.font.Font("C:\\Users\\minih\\Desktop\\C'MON_6\\NanumGothic.ttf", 25)
        resident_phrases = ["평", "평화", "평화롭", "평화롭군", "평화롭군.", "평화롭군..", "평화롭군..."]
        if resident_index < len(resident_phrases):
            if current_time - text_last_update > text_interval:
                resident_index += 1
                text_last_update = current_time
        idx = max(resident_index - 1, 0)
        text_surface = resident_font.render(resident_phrases[idx], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(resident_x_pos + resident_width // 2, resident_y_pos - 20))
        box_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
        screen.blit(text_surface, text_rect)

        if resident_index == len(resident_phrases) and current_time - text_last_update > 2000:
            display_resident_text = False
            display_hunter_text = True
            hunter_index = 0
            text_last_update = current_time
            character_can_move = True
            
    if show_book:
        book.set_alpha(book_alpha)
        screen.blit(book, (book_x_pos, book_y_pos))

    # --- gentile hunter 텍스트 ---
    if display_hunter_text:
        hunter_font = pygame.font.Font("C:\\Users\\minih\\Desktop\\C'MON_6\\NanumGothic.ttf", 25)
        hunter_phrase = "정말 그렇군요..."
        if hunter_index < len(hunter_phrase):
            if current_time - text_last_update > text_interval:
                hunter_index += 1
                text_last_update = current_time
        idx = max(hunter_index - 1, 0)
        text_surface = hunter_font.render(hunter_phrase[:idx], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(character_x_pos + character_width // 2, character_y_pos - 20))
        box_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
        screen.blit(text_surface, text_rect)

        if hunter_index == len(hunter_phrase) and current_time - text_last_update > 2000:
            display_hunter_text = False
            show_resident = False
    # HP
    if show_hp:
        hp_text = font.render(f"HP: {hp}/{max_hp}", True, (255, 0, 0))
        screen.blit(hp_text, (20, 20))
        bar_width = 200
        bar_height = 20
        fill = (hp / max_hp) * bar_width
        pygame.draw.rect(screen, (255, 0, 0), (20, 60, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (20, 60, fill, bar_height))
    
    
    if scene == 5 and not story_typing and story_line_index < len(story_lines):
        guide_text = small_font.render("SPACE 키를 눌러 진행해주세요", True, (255,255,255))
        guide_rect = guide_text.get_rect(topleft=(20, 20))
        bg_rect = guide_rect.inflate(10, 6)

        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(screen, (255,255,255), bg_rect, 2)
        screen.blit(guide_text, guide_rect)

    if fading:
        fade_alpha += fade_speed * fade_direction
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        if fade_alpha >= 255:
            scene = next_scene
            scene_start = current_time
            update_scene_display()
            fade_direction = -1
            if scene == 4:
                book_alpha = 0


        if fade_alpha <= 0 and fade_direction == -1:
            fading = False

    pygame.display.update()

pygame.quit()
