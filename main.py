import pygame, random
from pygame.locals import *

LARGURA, ALTURA = (800, 600)
VELOCIDADE_BARRA = 7.95
VELOCIDADE_BOLA = 8

px, py = (LARGURA//2, ALTURA/1.07)
bx, by = (LARGURA//2, ALTURA/2)

LARGURA_BLOCOS_C = LARGURA/20
LARGURA_BLOCOS_B = LARGURA/10

CORES = (
    (200, 0, 0),
    (200, 127, 0),
    (0, 200, 0),
    (0, 200, 127),
    (0, 0, 200),
    (127, 0, 200),
    (0, 127, 200),
    (200, 200, 0)
)

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))

relogio = pygame.time.Clock()

dir_bx, dir_by = ([-1, 1][random.randint(0, 1)], -1)


blocos_ = []
for _ in range(1, 3):
        for n in range(10*_):
            if _ == 1:
                blocos_.append([CORES[random.randint(0, 3)], (n*LARGURA_BLOCOS_B, ALTURA/4, LARGURA_BLOCOS_B, 20)])
            else:
                blocos_.append([CORES[random.randint(0, 3)], (n*LARGURA_BLOCOS_C, (ALTURA/4)-20, LARGURA_BLOCOS_C, 20)])

while True:
    blocos = []
    relogio.tick(30)
    tela.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    for n in range(len(blocos_)):
        bloco = blocos_[n]
        blocos.append(pygame.draw.rect(tela, bloco[0], bloco[1]))

    dir_px = 0

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        dir_px = -1
    if keys[K_RIGHT]:
        dir_px = 1

    px+=VELOCIDADE_BARRA*dir_px

    if px <= 0:
        px = 0
    elif LARGURA - px <= 100:
        px = LARGURA - 100
    
    if bx <= 0 or bx >= LARGURA:
        dir_bx *= -1
    if by <= 0:
        dir_by *= -1


    bx += VELOCIDADE_BOLA*dir_bx
    by += VELOCIDADE_BOLA*dir_by

    barra = pygame.draw.rect(tela, (200, 200, 200), (px, py, 100, 7))
    bola = pygame.draw.circle(tela, (200, 200, 200), (bx, by), 7)

    if by >= ALTURA/1.07:
        print("Perdeu")
        pygame.quit()
        exit()

    if bola.colliderect(barra):
        dir_bx *= [-1, 1][random.randint(0, 1)]
        dir_by *= -1

    for i, bloco in enumerate(blocos):
        if bloco.colliderect(bola):
            dir_bx *= 1
            dir_by *= -1
            blocos_.pop(i)

    pygame.display.update()