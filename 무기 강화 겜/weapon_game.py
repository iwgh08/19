import pygame
import os
import random

pygame.init()

# ====== 화면 설정 ======
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("검강겜")
fullscreen = True
screen_number = 0

# ====== 폰트 설정 ======
font_path = os.path.join("NanumGothic.ttf")
font = pygame.font.Font(font_path, 20)
large_font = pygame.font.Font(font_path, 30)
title_font = pygame.font.Font(font_path, 70)
small_font = pygame.font.Font(font_path, 10)

# 버튼 설정
button_color = (255, 255, 255)

# 검 이미지 가져오기
weapon1 = pygame.image.load("image/1강 검.png")
weapon2 = pygame.image.load("image/2강 검.png")
weapon3 = pygame.image.load("image/3강 검.png")
weapon4 = pygame.image.load("image/4강 검.png")
weapon5 = pygame.image.load("image/5강 검.png")
weapon6 = pygame.image.load("image/6강 검.png")
weapon7 = pygame.image.load("image/7강 검.png")
weapon8 = pygame.image.load("image/8강 검.png")
weapon9 = pygame.image.load("image/9강 검.png")
weapon10 = pygame.image.load("image/10강 검.png")
weapon11 = pygame.image.load("image/11강 검.png")
weapon_rect = weapon1.get_rect()
weapon_rect.center = (screen_width // 2, screen_height // 2)

# 텍스트 모음
text = []
# 제목
text.append(title_font.render("검강겜", True, (0, 0, 0)))
text_0_rect = text[0].get_rect()
# 조작 방법 타이틀
text.append(title_font.render("조작 방법", True, (0, 0, 0)))
text_1_rect = text[1].get_rect()
# 조작 설명
text.append(large_font.render("SPACE키 --> 강화 하기", True, (0, 0, 0)))
text_2_rect = text[2].get_rect()
text.append(large_font.render("뭘 설명할게 있다고 들어와. 퉤.", True, (0, 0, 0)))
text_3_rect = text[3].get_rect()
# 강화 성공 여부
text.append(large_font.render("강화 성공!", True, (0, 0, 0)))
text_4_rect = text[4].get_rect()
text.append(large_font.render("강화 실패!", True, (0, 0, 0)))
text_5_rect = text[5].get_rect()
text.append(large_font.render("ㅋ", True, (0, 0, 0)))
text_6_rect = text[6].get_rect()

enhanced1 = False
enhanced2 = False
current_sward_level = 1

weapons = [weapon1, weapon2, weapon3, weapon4, weapon5, weapon6, weapon7, weapon8, weapon9, weapon10, weapon11]
rates = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05]

def sward_enhanced():
    global current_sward_level, enhanced1, enhanced2
    
    # 만렙이면 더 이상 강화 안 함
    if current_sward_level >= 11:
        return

    # 현재 레벨에 맞는 확률 가져오기 (인덱스는 레벨-1)
    chance = rates[current_sward_level - 1]
    
    if random.random() < chance:
        current_sward_level += 1
        enhanced1 = True # 성공 플래그
        enhanced2 = False
    else:
        current_sward_level = 1 # 실패 시 초기화 (원하는 레벨로 수정 가능)
        enhanced1 = False
        enhanced2 = True # 실패 플래그

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            # 검 강화 버튼 ( 스페이스 키 )
            if event.key == pygame.K_SPACE:
                sward_enhanced()       
            
            # 풀 스크린 변환
            if event.key == pygame.K_F11:
                if fullscreen == False:
                    screen_width = info.current_w
                    screen_height = info.current_h
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    fullscreen = True
                else:
                    screen_width = 1280
                    screen_height = 720
                    screen = pygame.display.set_mode((screen_width, screen_height))
                    fullscreen = False
            
            # 설정 화면 변환
            if event.key == pygame.K_ESCAPE:
                if screen_number != 1:
                    screen_number = 1
                else:
                    screen_number = 0
        
        if event.type == pygame.MOUSEBUTTONUP:
            if screen_number == 1:
                if main_button_rect.collidepoint(event.pos):
                    screen_number = 0
                
                if setting_button_rect.collidepoint(event.pos):
                    screen_number = 2
                
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
    
                
    
    # 화면 그리기
    if screen_number == 0:
        # 메인 화면
        screen.fill((255,255,255))

        # 글자 그리기
        text_0_rect.center = ((screen_width // 2, screen_height//10))
        screen.blit(text[0], text_0_rect)

        # level 글자
        current_chance = int(rates[current_sward_level - 1] * 100)
        level_text = large_font.render(f"+ {current_sward_level} 단계  " f" 성공 확률: {current_chance}%", True, (0, 0, 0))
        level_rect = level_text.get_rect()
        weapon_rect.center = (screen_width // 2, screen_height // 2)
        level_rect.center = (screen_width // 2, weapon_rect.top - 50)
        screen.blit(level_text, level_rect)
        screen.blit(weapons[current_sward_level - 1], weapon_rect)

        
        # 무기 그리기
        screen.blit(weapons[current_sward_level - 1], weapon_rect)
    
        # 강화 결과 텍스트 띄우기
        if enhanced1:
            text_4_rect.center = (screen_width // 2, screen_height // 2 + 200)
            screen.blit(text[4], text_4_rect)
        elif enhanced2:
            text_5_rect.center = (screen_width // 2, screen_height // 2 + 200)
            screen.blit(text[5], text_5_rect)
        pygame.display.update()

        if enhanced1 or enhanced2:
            pygame.time.wait(500) # 0.5초 대기
            enhanced1 = False
            enhanced2 = False

        # 강화 성공 화면
    elif screen_number == 1:
        # 설정 화면
        screen.fill((160, 160, 160))
        
        # 버튼 그리기
        # bnt1 메인화면버튼
        bnt1_w = screen_width // 5
        bnt1_h = screen_height // 10
        main_button_rect = pygame.Rect(screen_width//8, screen_height//6, screen_width//8, screen_height//10)
        pygame.draw.rect(screen, button_color, main_button_rect, border_radius=15)

        dynamic_size = int(bnt1_h * 0.4)
        dynamic_font = pygame.font.Font(font_path, dynamic_size)
        btn1_text = dynamic_font.render("메인화면으로", True, (0, 0, 0))
        btn1_text_rect = btn1_text.get_rect(center=main_button_rect.center)
        screen.blit(btn1_text, btn1_text_rect)

        # bnt2 조작 방법 버튼
        bnt2_w = screen_width // 5
        bnt2_h = screen_height // 10
        setting_button_rect = pygame.Rect(screen_width//8, screen_height//6 + screen_height//5, screen_width//8, screen_height//10)
        pygame.draw.rect(screen, button_color, setting_button_rect, border_radius=15)

        dynamic_size = int(bnt2_h * 0.4)
        dynamic_font = pygame.font.Font(font_path, dynamic_size)
        btn2_text = dynamic_font.render("조작 방법", True, (0, 0, 0))
        btn2_text_rect = btn2_text.get_rect(center=setting_button_rect.center)
        screen.blit(btn2_text, btn2_text_rect)

        # bnt3 게임 종료
        bnt3_w = screen_width // 5
        bnt3_h = screen_height // 10
        quit_button_rect = pygame.Rect(screen_width//8, screen_height//6 + screen_height//5*2, screen_width//8, screen_height//10)
        pygame.draw.rect(screen, button_color, quit_button_rect, border_radius=15)

        dynamic_size = int(bnt3_h * 0.4)
        dynamic_font = pygame.font.Font(font_path, dynamic_size)
        btn3_text = dynamic_font.render("게임 종료", True, (0, 0, 0))
        btn3_text_rect = btn3_text.get_rect(center=quit_button_rect.center)
        screen.blit(btn3_text, btn3_text_rect)
    
    elif screen_number == 2:
        screen.fill((255, 255, 255))

        text_1_rect.center = ((screen_width // 2, 100))
        screen.blit(text[1], text_1_rect)

        text_2_rect.center = ((screen_width // 2, screen_height//2))
        screen.blit(text[2], text_2_rect)

        text_3_rect.center = ((screen_width // 2, screen_height//2 + screen_height//20))
        screen.blit(text[3], text_3_rect)

    pygame.display.update()
    
    

