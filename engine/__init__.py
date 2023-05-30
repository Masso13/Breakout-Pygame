import pygame
from pygame.locals import KEYDOWN, QUIT, K_p, K_r, K_LEFT, K_RIGHT
from random import randint
from engine.constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont("arial", 20, True)
        self.clock = pygame.time.Clock()
    
    def update_blocks(self):
        blocks = []
        for n in range(len(self.blocks_)):
            block = self.blocks_[n]
            blocks.append(pygame.draw.rect(self.screen, block[0], block[1]))
        return blocks
    
    def generate_blocks(self):
        self.blocks_ = []
        for layer in range(1, 3):
            for n in range(AMOUNT_B*layer):
                if layer == 1:
                    self.blocks_.append([COLORS[randint(0, 3)], (n*WIDTH_BLOCKS_B, HEIGHT/4, WIDTH_BLOCKS_B, HEIGHT_BLOCKS)])
                else:
                    self.blocks_.append([COLORS[randint(0, 3)], (n*WIDTH_BLOCKS_B, (HEIGHT/4)-HEIGHT_BLOCKS, WIDTH_BLOCKS_B, HEIGHT_BLOCKS)])

    def render_label(self, text):
        label = self.font.render(text, False, (255, 255, 255))
        ret_label = label.get_rect()
        ret_label.center = (WIDTH/2, HEIGHT/2)

        self.screen.blit(label, ret_label)

    def interrupt(self, text, type):
        stoped = True
        while stoped:
            self.render_label(text)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_p and type == "pause":
                        stoped = False
                    elif event.key == K_r and type == "gameover" or type == "win":
                        self.reset_game()
                        stoped = False
                if event.type == QUIT:
                        pygame.quit()
                        exit()
            pygame.display.update()

    def random_dir(self):
        return [-1, 1][randint(0, 1)]

    def set_init_position(self):
        self.px, self.py = WIDTH/2, HEIGHT/1.07
        self.bx, self.by = WIDTH/2, HEIGHT/2
    
    def reset_game(self):
        self.generate_blocks()
        self.set_init_position()
        self.dir_bx, self.dir_by = self.random_dir(), -1

    def start(self):
        self.reset_game()
        while True:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            blocks = self.update_blocks()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        self.interrupt("Jogo Pausado (P)", "pause")
                if event.type == QUIT:
                        pygame.quit()
                        exit()

            dir_px = 0
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                dir_px = -1
            elif keys[K_RIGHT]:
                dir_px = 1
            
            self.px+=VELOCITY_BAR*dir_px
            self.px = max(0, min(self.px, WIDTH - 100))

            if self.bx <= 0 or self.bx >= WIDTH:
                self.dir_bx *= -1
            if self.by <= 0:
                self.dir_by *= -1
            
            self.bx += VELOCITY_BOL*self.dir_bx
            self.by += VELOCITY_BOL*self.dir_by

            bar = pygame.draw.rect(self.screen, (200, 200, 200), (self.px, self.py, 100, 7))
            bol = pygame.draw.circle(self.screen, (200, 200, 200), (self.bx, self.by), 7)

            if self.by >= HEIGHT/1.07:
                self.interrupt("Você Perdeu (R)", "gameover")
            
            if bol.colliderect(bar):
                self.dir_bx *= self.random_dir()
                self.dir_by *= -1
            
            for i, block in enumerate(blocks):
                if bol.colliderect(block):
                    self.dir_bx *= 1
                    self.dir_by *= -1
                    del self.blocks_[i]
                    break
            
            if len(self.blocks_) == 20:
                self.interrupt("Você Ganhou (R)", "win")
            
            pygame.display.update()