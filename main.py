import pygame, sys, random, os, time

from button import Button

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dolphin Rescue")


pygame.mixer.init()
ambiente_sound = pygame.mixer.Sound("assets/aquatic.mp3")
collision_sound = pygame.mixer.Sound("assets/collision.wav")
blip = pygame.mixer.Sound("assets/blip.mp3")
ambiente_sound.set_volume(0.1)


BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/", "back.jpeg")), (SCREEN_WIDTH, SCREEN_HEIGHT))
BG1 = pygame.transform.scale(pygame.image.load(os.path.join("assets/", "back1.jpeg")), (SCREEN_WIDTH, SCREEN_HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load(os.path.join("assets/", "back1_2.jpeg")), (SCREEN_WIDTH, SCREEN_HEIGHT))
BG3 = pygame.transform.scale(pygame.image.load(os.path.join("assets/", "back2_3.jpeg")), (SCREEN_WIDTH, SCREEN_HEIGHT))
BG4 = pygame.transform.scale(pygame.image.load(os.path.join("assets/", "back3_4.jpeg")), (SCREEN_WIDTH, SCREEN_HEIGHT))

shadow_sprite = pygame.image.load("assets/Shadow.png")
shadow_sprite = pygame.transform.scale(shadow_sprite, (100,100))

navy_sprite = pygame.image.load("assets/navy.png")
navy_sprite = pygame.transform.scale(navy_sprite, (100,100))

drowning = pygame.image.load("assets\drowning.png")
drowning = pygame.transform.scale(drowning, (100,100))

tubarao = pygame.image.load("assets\Tubarao1.png")
tubarao = pygame.transform.scale(tubarao, (242,116))

Piranha = pygame.image.load("assets\Piranha.png")
Piranha = pygame.transform.scale(Piranha, (200,200))

TubaraoMaligno = pygame.image.load("assets\TubaraoMaligno.png")
TubaraoMaligno = pygame.transform.scale(TubaraoMaligno, (300,300))

class Character(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

def transicao(f, n):
    SCREEN.fill("Black")
    pygame.display.flip()
    time.sleep(1)
    fase = get_font(25).render(f, True, "White")
    time.sleep(0.5)
    nome = get_font(30).render(n, True, "White")
    fase_rect = fase.get_rect(center=(640, 260))
    nome_rect = nome.get_rect(center=(640, 460))
    SCREEN.fill("Black")
    SCREEN.blit(fase, fase_rect)
    SCREEN.blit(nome, nome_rect)
    pygame.display.flip()
    time.sleep(2)

with open(r"ranking.txt", "r") as f:
    Ranking = f.read()

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def gameover(pontos):
    pygame.display.set_caption("Game Over")
    Ranking = 0
    if pontos>int(Ranking):
        Ranking = pontos
        with open(r"ranking.txt", "w") as f:
            f.write(str(Ranking))

    
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        GAMEOVER_TEXT = get_font(45).render("Obrigado por jogar", True, "Black")
        GAMEOVER_RECT = GAMEOVER_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(GAMEOVER_TEXT, GAMEOVER_RECT)

        GAMEOVER_GAMEOVER = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Red")

        GAMEOVER_GAMEOVER.changeColor(OPTIONS_MOUSE_POS)
        GAMEOVER_GAMEOVER.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GAMEOVER_GAMEOVER.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    

def game_navy(multiplicador):
    pygame.display.set_caption("Navy")
    navy = Character(navy_sprite, (512,512))

    tuba = Character(tubarao, (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
    afogado = Character(drowning, (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
    pira = Character(Piranha, (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
    tubaMaligno = Character(TubaraoMaligno, (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
    tubaspeed = 3
    piraspeed = 5
    tubaMalignoSpeed = 9
    life = 5
    score = 0
    direction = 0
    change_direction_interval = 1000
    last_direction_change_time = pygame.time.get_ticks()
    timer_font = pygame.font.Font(None, 36)
    start_time = pygame.time.get_ticks() 
    time_limit = 180/multiplicador  

    transicao("Fase 1", "Tranquilidade nas profundezas")           
    while True:

        keys = pygame.key.get_pressed()
        navy.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
        navy.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5
        
        current_time = pygame.time.get_ticks()
        if current_time - last_direction_change_time > change_direction_interval:
            direction = random.randint(0, 3)  

            last_direction_change_time = current_time

        if direction == 0:
            tuba.rect.x += tubaspeed
        elif direction == 1:
            tuba.rect.x -= tubaspeed
        elif direction == 2:
            tuba.rect.y -= tubaspeed
        elif direction == 3:
            tuba.rect.y += tubaspeed

        tuba.rect.x = max(0, min(tuba.rect.x, 1000))  
        tuba.rect.y = max(0, min(tuba.rect.y, 700))  




        if navy.rect.colliderect(afogado.rect):
            collision_sound.play()
            score += 5
            afogado.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

        elif navy.rect.colliderect( tuba.rect):
            collision_sound.play()
            if life != 0:
                life -= 1
                navy.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            else: gameover(score)

        elif tuba.rect.colliderect(afogado.rect):
            afogado.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000 

        SCREEN.blit(BG2, (0, 0))
        SCREEN.blit(afogado.image, afogado.rect)
        SCREEN.blit(tuba.image,  tuba.rect)
        SCREEN.blit(navy.image, navy.rect)
        

        SCORE_TEXT = get_font(15).render(f"Score: {score}", True, "Black")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(90, 30))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        FASE_TEXT = get_font(5).render("Tranquilidade nas Profundezas", True, "Black")
        SCORE_RECT = FASE_TEXT.get_rect(center=(340, 30))
        SCREEN.blit(FASE_TEXT, SCORE_RECT)

        timer_text = timer_font.render(f"Tempo: {time_limit - elapsed_time}", True, "Black")
        timer_rect = timer_text.get_rect(center=(1150, 30))
        SCREEN.blit(timer_text, timer_rect)

        VIDA_TEXT = get_font(15).render(f"Vidas: {life}", True, "Black")
        VIDA_RECT = VIDA_TEXT.get_rect(center=(90,50))
        SCREEN.blit(VIDA_TEXT,VIDA_RECT)

        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif elapsed_time >= time_limit:
                gameover(score)
            elif score >= 40:

                transicao("Fase 2", "Sombras Emergentes")  
                while True:

                    keys = pygame.key.get_pressed()
                    navy.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
                    navy.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5

                    current_time = pygame.time.get_ticks()
                    if current_time - last_direction_change_time > change_direction_interval:
                        direction = random.randint(0, 3)  # 0: direita, 1: esquerda, 2: cima, 3: baixo

                        last_direction_change_time = current_time

                    if direction == 0:
                        pira.rect.x += piraspeed
                    elif direction == 1:
                        pira.rect.x -= piraspeed
                    elif direction == 2:
                        pira.rect.y -= piraspeed
                    elif direction == 3:
                        pira.rect.y += piraspeed

                    pira.rect.x = max(0, min(pira.rect.x, 1000))  # Largura da tela - largura do sprite
                    pira.rect.y = max(0, min(pira.rect.y, 700))  # Altura da tela - altura do sprite

                    if navy.rect.colliderect(afogado.rect):
                        collision_sound.play()
                        score += 5
                        afogado.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

                    elif navy.rect.colliderect(pira.rect):
                        collision_sound.play()
                        if life != 0:
                            life -= 1
                            navy.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
                        else: gameover(score)

                    elif pira.rect.colliderect(afogado.rect):
                        afogado.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

                    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000 

                    

                    SCREEN.blit(BG3, (0, 0))
                    SCREEN.blit(afogado.image, afogado.rect)
                    SCREEN.blit(pira.image, pira.rect)
                    SCREEN.blit(navy.image, navy.rect)

                    SCORE_TEXT = get_font(15).render(f"Score: {score}", True, "White")
                    SCORE_RECT = SCORE_TEXT.get_rect(center=(90, 30))
                    SCREEN.blit(SCORE_TEXT, SCORE_RECT)

                    FASE_TEXT = get_font(15).render("Sombras Emergentes", True, "White")
                    SCORE_RECT = FASE_TEXT.get_rect(center=(640, 30))
                    SCREEN.blit(FASE_TEXT, SCORE_RECT)

                    timer_text = timer_font.render(f"Tempo: {time_limit - elapsed_time}", True, "White")
                    timer_rect = timer_text.get_rect(center=(1150, 30))
                    SCREEN.blit(timer_text, timer_rect)

                    VIDA_TEXT = get_font(15).render(f"Vidas: {life}", True, "White")
                    VIDA_RECT = VIDA_TEXT.get_rect(center=(90,50))
                    SCREEN.blit(VIDA_TEXT,VIDA_RECT)

                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif elapsed_time >= time_limit:
                            gameover(score)
                        elif score >= 80:
                            transicao("Fase 3", "Abismo do Desespero")  
                            while True:

                                keys = pygame.key.get_pressed()
                                navy.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 1.5
                                navy.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 1.5

                                current_time = pygame.time.get_ticks()
                                if current_time - last_direction_change_time > change_direction_interval:
                                    direction = random.randint(0, 3)  # 0: direita, 1: esquerda, 2: cima, 3: baixo

                                    last_direction_change_time = current_time

                                if direction == 0:
                                    tubaMaligno.rect.x += tubaMalignoSpeed
                                elif direction == 1:
                                    tubaMaligno.rect.x -= tubaMalignoSpeed
                                elif direction == 2:
                                    tubaMaligno.rect.y -= tubaMalignoSpeed
                                elif direction == 3:
                                    tubaMaligno.rect.y += tubaMalignoSpeed

                                tubaMaligno.rect.x = max(100, min(tubaMaligno.rect.x, 1000))  # Largura da tela - largura do sprite
                                tubaMaligno.rect.y = max(100, min(tubaMaligno.rect.y, 650))  # Altura da tela - altura do sprite

                                if navy.rect.colliderect(afogado.rect):
                                    collision_sound.play()
                                    score += 5
                                    afogado.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
                                

                                elif  navy.rect.colliderect( tubaMaligno.rect):
                                    collision_sound.play()
                                    if life != 0:
                                        life -= 1
                                        navy.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
                                    else: gameover(score) 

                                elif tubaMaligno.rect.colliderect(afogado.rect):
                                    afogado.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))


                                elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

                                SCREEN.blit(BG4, (0, 0))
                                SCREEN.blit(navy.image, navy.rect)
                                SCREEN.blit(tubaMaligno.image,   tubaMaligno.rect)
                                SCREEN.blit(afogado.image, afogado.rect)

                                SCORE_TEXT = get_font(15).render(f"Score: {score}", True, "White")
                                SCORE_RECT = SCORE_TEXT.get_rect(center=(90, 30))
                                SCREEN.blit(SCORE_TEXT, SCORE_RECT)

                                FASE_TEXT = get_font(15).render("Abismo do Desespero", True, "White")
                                SCORE_RECT = FASE_TEXT.get_rect(center=(640, 30))
                                SCREEN.blit(FASE_TEXT, SCORE_RECT)

                                timer_text = timer_font.render(f"Tempo: {time_limit - elapsed_time}", True, "White")
                                timer_rect = timer_text.get_rect(center=(1150, 30))
                                SCREEN.blit(timer_text, timer_rect)

                                VIDA_TEXT = get_font(15).render(f"Vidas: {life}", True, "White")
                                VIDA_RECT = VIDA_TEXT.get_rect(center=(90,50))
                                SCREEN.blit(VIDA_TEXT,VIDA_RECT)

                                pygame.display.flip()
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    elif elapsed_time >= time_limit:
                                        gameover(score)

def game_shadow(multiplicador):
    shadow = Character(shadow_sprite, (512,512))

    tuba = Character(tubarao, (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
    afogado = Character(drowning, (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
    pira = Character(Piranha, (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
    tubaMaligno = Character(TubaraoMaligno, (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))

    tubaspeed = 3
    piraspeed = 2
    tubaMalignoSpeed = 1
    score = 0
    life = 3
    direction = 0
    change_direction_interval = 1000
    last_direction_change_time = pygame.time.get_ticks()
    timer_font = pygame.font.Font(None, 36)
    start_time = pygame.time.get_ticks() 
    time_limit = 180/multiplicador  


    transicao("Fase 1", "Tranquilidade nas profundezas")  

    while True:
        keys = pygame.key.get_pressed()
        shadow.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
        shadow.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5

        current_time = pygame.time.get_ticks()
        if current_time - last_direction_change_time > change_direction_interval:
            direction = random.randint(0, 3)  # 0: direita, 1: esquerda, 2: cima, 3: baixo

            last_direction_change_time = current_time

        if direction == 0:
            tuba.rect.x += tubaspeed
        elif direction == 1:
            tuba.rect.x -= tubaspeed
        elif direction == 2:
            tuba.rect.y -= tubaspeed
        elif direction == 3:
            tuba.rect.y += tubaspeed

        tuba.rect.x = max(0, min(tuba.rect.x, 1000))  # Largura da tela - largura do sprite
        tuba.rect.y = max(0, min(tuba.rect.y, 700))  # Altura da tela - altura do sprite

        if shadow.rect.colliderect(afogado.rect):
            collision_sound.play()
            score += 5
            new_x = random.randint(0, SCREEN_WIDTH - afogado.rect.width)
            new_y = random.randint(0, SCREEN_HEIGHT - afogado.rect.height)
            afogado.rect.topleft = (new_x, new_y)

        elif shadow.rect.colliderect(tuba.rect):
            collision_sound.play()
            if life != 0:
                life -= 1
                shadow.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            else: gameover(score)

        elif tuba.rect.colliderect(afogado.rect):
            afogado.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000 

        SCREEN.blit(BG2, (0, 0))
        SCREEN.blit(shadow.image, shadow.rect)
        SCREEN.blit(tuba.image,   tuba.rect)
        SCREEN.blit(afogado.image, afogado.rect)

        SCORE_TEXT = get_font(15).render(f"Score: {score}", True, "Black")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(90, 30))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        FASE_TEXT = get_font(15).render("Tranquilidade nas Profundezas", True, "Black")
        SCORE_RECT = FASE_TEXT.get_rect(center=(640, 30))
        SCREEN.blit(FASE_TEXT, SCORE_RECT)

        timer_text = timer_font.render(f"Tempo: {time_limit - elapsed_time}", True, "Black")
        timer_rect = timer_text.get_rect(center=(1150, 30))
        SCREEN.blit(timer_text, timer_rect)

        VIDA_TEXT = get_font(15).render(f"Vidas: {life}", True, "Black")
        VIDA_RECT = VIDA_TEXT.get_rect(center=(90,50))
        SCREEN.blit(VIDA_TEXT,VIDA_RECT)

        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif elapsed_time >= time_limit:
                gameover(score)
            elif score >= 40:

                transicao("Fase 2", "Sombras Emergentes")  

                while True:

                    keys = pygame.key.get_pressed()
                    shadow.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
                    shadow.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5
                    
                    current_time = pygame.time.get_ticks()
                    if current_time - last_direction_change_time > change_direction_interval:
                        direction = random.randint(0, 3)  # 0: direita, 1: esquerda, 2: cima, 3: baixo

                        last_direction_change_time = current_time

                    if direction == 0:
                        pira.rect.x += piraspeed
                    elif direction == 1:
                        pira.rect.x -= piraspeed
                    elif direction == 2:
                        pira.rect.y -= piraspeed
                    elif direction == 3:
                        pira.rect.y += piraspeed

                    pira.rect.x = max(0, min(pira.rect.x, 1000))  # Largura da tela - largura do sprite
                    pira.rect.y = max(0, min(pira.rect.y, 700))  # Altura da tela - altura do sprite

                    if shadow.rect.colliderect(afogado.rect):
                        collision_sound.play()
                        score += 5
                        new_x = random.randint(0, SCREEN_WIDTH - afogado.rect.width)
                        new_y = random.randint(0, SCREEN_HEIGHT - afogado.rect.height)
                        afogado.rect.topleft = (new_x, new_y)

                    elif shadow.rect.colliderect(pira.rect):
                        collision_sound.play()
                        if life != 0:
                            life -= 1
                            shadow.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
                        else: gameover(score)

                    elif pira.rect.colliderect(afogado.rect):
                        afogado.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

                    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000 

                    SCREEN.blit(BG3, (0, 0))
                    SCREEN.blit(shadow.image, shadow.rect)
                    SCREEN.blit(pira.image,   pira.rect)
                    SCREEN.blit(afogado.image, afogado.rect)

                    SCORE_TEXT = get_font(15).render(f"Score: {score}", True, "White")
                    SCORE_RECT = SCORE_TEXT.get_rect(center=(90, 30))
                    SCREEN.blit(SCORE_TEXT, SCORE_RECT)

                    FASE_TEXT = get_font(15).render("Sombras Emergentes", True, "White")
                    SCORE_RECT = FASE_TEXT.get_rect(center=(640, 30))
                    SCREEN.blit(FASE_TEXT, SCORE_RECT)

                    timer_text = timer_font.render(f"Tempo: {time_limit - elapsed_time}", True, "White")
                    timer_rect = timer_text.get_rect(center=(1150, 30))
                    SCREEN.blit(timer_text, timer_rect)

                    VIDA_TEXT = get_font(15).render(f"Vidas: {life}", True, "White")
                    VIDA_RECT = VIDA_TEXT.get_rect(center=(90,50))
                    SCREEN.blit(VIDA_TEXT,VIDA_RECT)

                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif elapsed_time >= time_limit:
                            gameover(score)
                        elif score >= 80:

                            transicao("Fase 3", "Abismo do Desespero")  

                            while True:

                                keys = pygame.key.get_pressed()
                                shadow.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 1.5
                                shadow.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 1.5

                                current_time = pygame.time.get_ticks()
                                if current_time - last_direction_change_time > change_direction_interval:
                                    direction = random.randint(0, 3)  # 0: direita, 1: esquerda, 2: cima, 3: baixo

                                    last_direction_change_time = current_time

                                if direction == 0:
                                    tubaMaligno.rect.x += tubaMalignoSpeed
                                elif direction == 1:
                                    tubaMaligno.rect.x -= tubaMalignoSpeed
                                elif direction == 2:
                                    tubaMaligno.rect.y -= tubaMalignoSpeed
                                elif direction == 3:
                                    tubaMaligno.rect.y += tubaMalignoSpeed

                                tubaMaligno.rect.x = max(100, min(tubaMaligno.rect.x, 1000))  # Largura da tela - largura do sprite
                                tubaMaligno.rect.y = max(100, min(tubaMaligno.rect.y, 650))  # Altura da tela - altura do sprite

                                if shadow.rect.colliderect(afogado.rect):
                                    collision_sound.play()
                                    score += 5
                                    new_x = random.randint(0, SCREEN_WIDTH - afogado.rect.width)
                                    new_y = random.randint(0, SCREEN_HEIGHT - afogado.rect.height)
                                    afogado.rect.topleft = (new_x, new_y)

                                if shadow.rect.colliderect(tubaMaligno.rect):
                                    collision_sound.play()
                                    if life != 0:
                                        life -= 1
                                        shadow.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
                                    else: gameover(score)

                                elif tubaMaligno.rect.colliderect(afogado.rect):
                                    afogado.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
                                    
                                elapsed_time = (pygame.time.get_ticks() - start_time) // 1000 

                                SCREEN.blit(BG4, (0, 0))
                                SCREEN.blit(shadow.image, shadow.rect)
                                SCREEN.blit(tubaMaligno.image, tubaMaligno.rect)
                                SCREEN.blit(afogado.image, afogado.rect)

                                SCORE_TEXT = get_font(15).render(f"Score: {score}", True, "White")
                                SCORE_RECT = SCORE_TEXT.get_rect(center=(90, 30))
                                SCREEN.blit(SCORE_TEXT, SCORE_RECT)

                                FASE_TEXT = get_font(15).render("Abismo do Desespero", True, "White")
                                SCORE_RECT = FASE_TEXT.get_rect(center=(640, 30))
                                SCREEN.blit(FASE_TEXT, SCORE_RECT)

                                timer_text = timer_font.render(f"Tempo: {time_limit - elapsed_time}", True, "White")
                                timer_rect = timer_text.get_rect(center=(1150, 30))
                                SCREEN.blit(timer_text, timer_rect)

                                VIDA_TEXT = get_font(15).render(f"Vidas: {life}", True, "White")
                                VIDA_RECT = VIDA_TEXT.get_rect(center=(90,50))
                                SCREEN.blit(VIDA_TEXT,VIDA_RECT)

                                pygame.display.flip()
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    elif elapsed_time >= time_limit:
                                        gameover(score)

def character(dificuldade):
    pygame.display.set_caption("Personagem")
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        SCREEN.blit(BG1, (0, 0))

        GAME_TEXT = get_font(45).render("Escolha o personagem!", True, "Black")
        GAME_RECT = GAME_TEXT.get_rect(center=(640, 160))
        SCREEN.blit(GAME_TEXT, GAME_RECT)

        CHARACTER1 = Button(image=None, pos=(640, 260), 
                            text_input="Navy", font=get_font(40), base_color="Blue", hovering_color="White")
        CHARACTER2 = Button(image=None, pos=(640, 360), 
                            text_input="Shadow", font=get_font(40), base_color="Red", hovering_color="Black")
        PLAY_BACK = Button(image=None, pos=(640, 560), 
                            text_input="BACK", font=get_font(75), base_color="Dark Gray", hovering_color="Green")

        CHARACTER1.changeColor(PLAY_MOUSE_POS)
        CHARACTER1.update(SCREEN)

        CHARACTER2.changeColor(PLAY_MOUSE_POS)
        CHARACTER2.update(SCREEN)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CHARACTER1.checkForInput(PLAY_MOUSE_POS):
                    blip.play()
                    game_navy(dificuldade)
                elif CHARACTER2.checkForInput(PLAY_MOUSE_POS):
                    blip.play()
                    game_shadow(dificuldade)
                elif PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    blip.play()
                    main_menu()

        pygame.display.update()

def play():
    pygame.display.set_caption("Dificuldade")
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        SCREEN.blit(BG1, (0, 0))
        
        PLAY_TEXT = get_font(35).render("Escolha a dificuldade!", True, "Black")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 160))

        
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        EASY_BUTTON = Button(image=None, pos=(640, 260),
                            text_input="EASY", font=get_font(40), base_color="#FFCC57", hovering_color="#242834")
        MEDIUM_BUTTON = Button(image=None, pos=(640, 360),
                            text_input="MEDIUM", font=get_font(40), base_color="#C4B0A9", hovering_color="#242834")
        HARD_BUTTON = Button(image=None, pos=(640, 460),
                            text_input="HARD", font=get_font(40), base_color="#489AC2", hovering_color="#242834")
        
        

        PLAY_BACK = Button(image=None, pos=(640, 560), 
                            text_input="BACK", font=get_font(75), base_color="Gray", hovering_color="Green")
        
        EASY_BUTTON.changeColor(PLAY_MOUSE_POS)
        EASY_BUTTON.update(SCREEN)

        MEDIUM_BUTTON.changeColor(PLAY_MOUSE_POS)
        MEDIUM_BUTTON.update(SCREEN)

        HARD_BUTTON.changeColor(PLAY_MOUSE_POS)
        HARD_BUTTON.update(SCREEN)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    blip.play()
                    character(1)
                elif MEDIUM_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    blip.play()
                    character(2)
                elif HARD_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    blip.play()
                    character(3)
                elif PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    blip.play()
                    main_menu()

        pygame.display.update()

def ranking():
    pygame.display.set_caption("Options")
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        SCREEN.blit(BG2, (0, 0))

        OPTIONS_TEXT = get_font(35).render("Pontuacao Maxima", True, "#002535")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 160))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        with open(r"ranking.txt", "r") as f:
            Ranking = f.read()

        RANKING_BUTTON = Button(image=None, pos=(640, 260),
                            text_input=Ranking, font=get_font(40), base_color="#FFCC57", hovering_color="#242834")

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="#22646e")


        RANKING_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        RANKING_BUTTON.update(SCREEN)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    blip.play()
                    main_menu()

        pygame.display.update()

def options():
    pygame.display.set_caption("Options")
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        SCREEN.blit(BG2, (0, 0))

        OPTIONS_TEXT = get_font(35).render("SOM", True, "#002535")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 160))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        SOM_BUTTON_OFF = Button(image=None, pos=(426.67, 260),
                            text_input="OFF", font=get_font(40), base_color="#FFCC57", hovering_color="#242834")
        SOM_BUTTON_ON = Button(image=None, pos=(853.34, 260),
                            text_input="ON", font=get_font(40), base_color="#FFCC57", hovering_color="#242834")
        RANKING_BUTTON = Button(image=None, pos=(640, 360),
                            text_input="Ranking", font=get_font(40), base_color="#C4B0A9", hovering_color="#242834")

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="#22646e")

        SOM_BUTTON_OFF.changeColor(OPTIONS_MOUSE_POS)
        SOM_BUTTON_OFF.update(SCREEN)

        SOM_BUTTON_ON.changeColor(OPTIONS_MOUSE_POS)
        SOM_BUTTON_ON.update(SCREEN)

        RANKING_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        RANKING_BUTTON.update(SCREEN)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    blip.play()
                    main_menu()
                elif SOM_BUTTON_OFF.checkForInput(OPTIONS_MOUSE_POS):
                    blip.play()
                    collision_sound.set_volume(0)
                    ambiente_sound.set_volume(0)
                    blip.set_volume(0)
                elif SOM_BUTTON_ON.checkForInput(OPTIONS_MOUSE_POS):
                    collision_sound.set_volume(0.5)
                    ambiente_sound.set_volume(0.1)
                    blip.set_volume(1)
                    blip.play()
                elif RANKING_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    blip.play()
                    ranking()

        pygame.display.update()

def main_menu():
    pygame.display.set_caption("Menu")
    ambiente_sound.play()
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("DOLPHIN RESCUE", True, "BLACK")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="#13294B")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(50), base_color="#d7fcd4", hovering_color="#13294B")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="#13294B")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    blip.play()
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    blip.play()
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    blip.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
