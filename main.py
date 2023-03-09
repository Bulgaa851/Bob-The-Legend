import pygame
from sys import exit
from random import randint,choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk1 = pygame.image.load('Graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('Graphics/Player/player_walk_2.png').convert_alpha()

        self.player_walk = [player_walk1,player_walk2]

        self.player_jump = pygame.image.load('Graphics/Player/jump.png').convert_alpha()
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity +=0.9
        self.rect.y+=self.gravity
        if self.rect.bottom>=300:
            self.rect.bottom=300
    def animation(self):
        if self.rect.bottom <300:
            self.image = self.player_jump
        else:
            self.player_index +=0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':

            fly_frame1 = pygame.image.load('Graphics/Fly/Fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('Graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1,fly_frame2]
            y_pos = 200
        else:
            snail_frame1 = pygame.image.load('Graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('Graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1,snail_frame2]
            y_pos=300

        self.animation_index=0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    def animation(self):
        self.animation_index+=0.1
        if self.animation_index >= len(self.frames):self.animation_index=0
        self.image=self.frames[int(self.animation_index)]
    def update(self):
        self.animation()
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = score_font.render(f"Score: {current_time}",False,(64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return(current_time)
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Bob the Legend')
clock = pygame.time.Clock()
score_font = pygame.font.Font('Fonts/font.ttf', 50)
restart_font = pygame.font.Font('Fonts/font.ttf', 30)
game_active = False
game_started = False
score=0
start_time = 0 
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

bg_sound = pygame.mixer.Sound('audio/music.wav')
bg_sound.set_volume(0.2)
bg_sound.play(loops = -1)

sky_surface = pygame.image.load('Graphics/Sky.png').convert()
ground_surface = pygame.image.load('Graphics/ground.png').convert()

#MENU
menu_text_surf1 = restart_font.render("Bob The Legend",False,(64,64,64))
menu_text_rect1 = menu_text_surf1.get_rect(center = (400,100))

menu_bob_surf =  pygame.image.load('Graphics/Player/player_stand.png').convert_alpha()
menu_bob_scaled = pygame.transform.scale2x(menu_bob_surf)
menu_bob_rect= menu_bob_surf.get_rect(center = (400,200))

menu_text_surf2 = restart_font.render("Press enter to run",False,(64,64,64))
menu_text_rect2 = menu_text_surf2.get_rect(center = (400,350))


#RESTART
restart_surface = restart_font.render("If u want Restart Press: ENTER KEY",False,(64,64,64))
restart_rect = restart_surface.get_rect(center =(400,100))


#Timer 

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1400)


#MAIN CODE 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active == False and game_started:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_active = True
                    start_time = int(pygame.time.get_ticks()/1000)
                    score = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        if game_started == False and game_active == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_started = True
                    game_active = True
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail'])))
    if game_active and game_started:

        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        display_score()
        score = display_score()

        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
        
    elif game_started == False and game_active == False:
            screen.fill('#c0e8ec')
            screen.blit(menu_text_surf1, menu_text_rect1)
            screen.blit(menu_bob_scaled, menu_bob_rect)
            screen.blit(menu_text_surf2, menu_text_rect2)
            
    else:
        screen.fill('#c0e8ec')
        screen.blit(restart_surface,restart_rect)
        screen.blit(menu_bob_scaled,menu_bob_rect)
        
        player_gravity = 0
        restart_score_surf = restart_font.render(f'Score: {score}',False,(64,64,64))
        restart_score_rect = restart_score_surf.get_rect(center = (400,350))
        screen.blit(restart_score_surf,restart_score_rect)

    pygame.display.update()
    clock.tick(60)

