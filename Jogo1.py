from random import randint
import pygame
from pygame import font
from pygame import display
from pygame.image import load
from pygame.transform import scale
from pygame.sprite import *
from pygame import event
from pygame.locals import *
from pygame.time import Clock

#Uniesp Centro Universitário
#Introdução a Programação
#Lucas dos Santos Alves
#Gabriel Montenegro Pires de Andrade
#Hugo Luann Pedrosa Carneiro Honório

pygame.init()

#Carregando as músicas do jogo.

pygame.mixer.music.set_volume(0.30)
musica_menu = pygame.mixer.music.load("musicas/trilhafundo.wav")
pygame.mixer.music.play(-1)
musica_colisao = pygame.mixer.Sound("musicas/colisao.wav")
musica_gameover = pygame.mixer.Sound("musicas/gamerover.wav")
musica_ganhar = pygame.mixer.Sound("musicas/trilhavitoria.wav")

#Configurando janela do jogo e fontes.

tamanho = 800, 600
fonte = font.SysFont('comicsans', 50)
fonte_perdeu = font.SysFont('comicsans', 300)

superficie = display.set_mode(
    size=tamanho
)

#Definindo título do jogo.

display.set_caption(
    'Star Wars: O resgate'
)

#Carregando todas as imagens do jogo e as ajustando ao tamanho da janela.

fundo = scale(
    load('imagens/fundo.jpg'),
    tamanho
)
menu = scale(
    load('imagens/menu.jpg'),
    tamanho
)
fundo2 = scale(
    load('imagens/deserto.jpeg'),
    tamanho
)
ganhar = scale(
    load('imagens/ganhar.jpg'),
    tamanho
)
perder = scale(
    load('imagens/perder.jpg'),
    tamanho
)
introducao = scale(
    load('imagens/intoducao.jpg'),
    tamanho
)
instrucoes = scale(
    load('imagens/instrucoes.jpg'),
    tamanho
)
introducao2 = scale(
    load('imagens/introducao2.jpg'),
    tamanho
)

final = scale(
    load('imagens/final.jpeg'),
    tamanho
)

#Implementando a lógica das sprites.

class Nave(Sprite):
    def __init__(self, municao):
        super().__init__()

        self.image = load('imagens/nave.png')
        self.rect = self.image.get_rect()
        self.municao = municao
        self.velocidade = 2

    def atirar_municao(self):
        if len(self.municao) < 15:
            self.municao.add(
                Municao(*self.rect.center)
            )

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade


class Municao(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = load('imagens/municao.png')
        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def update(self):
        self.rect.x += 1

        if self.rect.x > tamanho[0]:
            self.kill()


class Inimigo(Sprite):
    def __init__(self):
        super().__init__()

        self.image = load('imagens/inimigo.png')
        self.rect = self.image.get_rect(
            center=(800, randint(20, 580))
        )

    def update(self):
        global perdeu
        self.rect.x -= 0.1

        if self.rect.x == 0:
            self.kill()
            perdeu = True


grupo_inimigos = Group()
grupo_municao = Group()
nave = Nave(grupo_municao)
grupo_nave = GroupSingle(nave)

grupo_inimigos.add(Inimigo())

#Carregando as variáveis.

clock = Clock()
mortes = 0
round = 0
perdeu = False
iniciar = 0
vari = 0
vari2 = 0

#Carregando a lógica do jogo

while True:
    # Loop de eventos
    clock.tick(120)  # FPS

    if round % 200 == 0:
        if mortes < 20:
            grupo_inimigos.add(Inimigo())
        for i in range(int(mortes / 20)):
            grupo_inimigos.add(Inimigo())

    # Espaço dos eventos

    for evento in event.get():  # Events
        if evento.type == QUIT:
            pygame.quit()

        if evento.type == KEYUP:
            if evento.key == K_SPACE:
                Nave.atirar_municao(self=nave)
                musica_colisao.play()
        if evento.type == KEYUP:
            if evento.key == K_SPACE:
                iniciar = iniciar+1
                vari = iniciar+2
                vari2 = iniciar+2


    if groupcollide(grupo_municao, grupo_inimigos, True, True):
        mortes += 1

    # Espaço do display

    if iniciar == 0:
        superficie.blit(menu, (0, 0))

    elif iniciar == 1:
        superficie.blit(introducao, (0, 0))

    elif iniciar == 2:
        superficie.blit(instrucoes, (0, 0))

    elif mortes <=50:
        superficie.blit(fundo, (0, 0))

        fonte_mortes = fonte.render(
            f'Mortes: {mortes}',
            True,
            (255, 255, 255)
        )

        superficie.blit(fonte_mortes, (10, 40))

        grupo_nave.draw(superficie)
        grupo_inimigos.draw(superficie)
        grupo_municao.draw(superficie)

        grupo_nave.update()
        grupo_inimigos.update()
        grupo_municao.update()
        vari = 0

    elif iniciar == iniciar and iniciar>vari:
        superficie.blit(introducao2, (0, 0))

    elif mortes<=100:
        superficie.blit(fundo2, (0, 0))

        fonte_mortes = fonte.render(
            f'Mortes: {mortes}',
            True,
            (0, 0, 0)
        )

        superficie.blit(fonte_mortes, (10, 40))

        grupo_nave.draw(superficie)
        grupo_inimigos.draw(superficie)
        grupo_municao.draw(superficie)

        grupo_nave.update()
        grupo_inimigos.update()
        grupo_municao.update()
        vari2 = 0

    elif iniciar == iniciar and iniciar>vari2:
        pygame.mixer.music.stop()
        musica_ganhar.play()
        superficie.blit(final, (0, 0))

    else:
        superficie.blit(ganhar, (0, 0))

    if perdeu:
        pygame.mixer.music.stop()
        musica_gameover.play()
        superficie.blit(perder, (0, 0))

    round += 1
    display.update()
