import pygame
import sys
import random
pygame.init()

#tela 
LARGURA_JANELA = 1900
ALTURA_JANELA = 1000
tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption("Aim Vasco")

#cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

#algumas imagens do jogo
def carregar_imagem(caminho, largura, altura):
    imagem = pygame.image.load(caminho)
    imagem = pygame.transform.scale(imagem, (largura, altura))
    return imagem

cenario = carregar_imagem('bgmark.png', LARGURA_JANELA, ALTURA_JANELA)
jogador_imagem = carregar_imagem("flamengo.png", 40, 40)
alvo_imagem = carregar_imagem("vasco2.png", 100, 100)
icone_imagem1 = carregar_imagem("arma.png", 500, 500)
icone_imagem2 = carregar_imagem("arma2.png", 500, 500)

#fonte de escrita 
fonte = pygame.font.SysFont(None, 36)
#estados do jogo
ESTADO_INICIO = 0
ESTADO_JOGANDO = 1
ESTADO_FIM = 2

class Jogo:
    def __init__(self):
        self.estado = ESTADO_INICIO
        self.pontuacao = 0
        self.tempo_limite = 30
        self.tempo_inicial = pygame.time.get_ticks()

        self.jogador = Jogador()
        self.alvo = Alvo()

    def iniciar_jogo(self):
        self.estado = ESTADO_JOGANDO
        self.tempo_inicial = pygame.time.get_ticks()
        self.pontuacao = 0
        self.jogador.reset()
        self.alvo.reset()


    def reiniciar_jogo(self):
        self.iniciar_jogo()

    def desenhar_botao(self, texto, cor, x, y, largura, altura):
        pygame.draw.rect(tela, cor, (x, y, largura, altura))
        texto_botao = fonte.render(texto, True, PRETO)
        tela.blit(texto_botao, (x + (largura - texto_botao.get_width()) // 2, y + (altura - texto_botao.get_height()) // 2))

    def verificar_clique_no_alvo(self, mouse_x, mouse_y):
        if self.alvo.retangulo.collidepoint(mouse_x, mouse_y):
            self.alvo.mover_para_uma_nova_posicao()
            self.pontuacao += 1

    def atualizar_estado_jogo(self):
        tempo_atual = (pygame.time.get_ticks() - self.tempo_inicial) // 1000
        if self.estado == ESTADO_JOGANDO and tempo_atual >= self.tempo_limite:
            self.estado = ESTADO_FIM

    def desenhar_estado(self):
        tela.blit(cenario, (0, 0))
        if self.estado == ESTADO_INICIO:
            tela.blit(icone_imagem1, (LARGURA_JANELA // 2 - icone_imagem1.get_width() - 10, ALTURA_JANELA // 2 - icone_imagem1.get_height() - 50))
            tela.blit(icone_imagem2, (LARGURA_JANELA // 2 + 10, ALTURA_JANELA // 2 - icone_imagem2.get_height() - 50))
            self.desenhar_botao("Iniciar Jogo", VERMELHO, LARGURA_JANELA // 2 - 100, ALTURA_JANELA // 2, 200, 50)
            self.desenhar_botao("Configurações", VERMELHO, LARGURA_JANELA // 2 - 100, ALTURA_JANELA // 2 + 100, 200, 50)
        elif self.estado == ESTADO_JOGANDO:
            tela.blit(self.alvo.imagem, self.alvo.posicao)
            tela.blit(self.jogador.imagem, self.jogador.posicao)
            texto_pontuacao = fonte.render("Pontuação: " + str(self.pontuacao), True, VERMELHO)
            tela.blit(texto_pontuacao, (10, 10))
            tempo_restante = max(0, self.tempo_limite - (pygame.time.get_ticks() - self.tempo_inicial) // 1000)
            texto_tempo = fonte.render("Tempo Restante: " + str(tempo_restante), True, VERMELHO)
            tela.blit(texto_tempo, (LARGURA_JANELA - texto_tempo.get_width() - 10, 10))
        elif self.estado == ESTADO_FIM:
            texto_fim = fonte.render("Fim de jogo! Pontuação: " + str(self.pontuacao), True, BRANCO)
            tela.blit(texto_fim, (LARGURA_JANELA // 2 - texto_fim.get_width() // 2, ALTURA_JANELA // 2 - 100))
            self.desenhar_botao("Reiniciar Jogo", VERMELHO, LARGURA_JANELA // 2 - 100, ALTURA_JANELA // 2 - 50, 200, 50)
            self.desenhar_botao("Voltar ao Início", VERMELHO, LARGURA_JANELA // 2 - 100, ALTURA_JANELA // 2 + 10, 200, 50)

class Jogador:
    def __init__(self):
        self.imagem = jogador_imagem
        self.largura = 40
        self.altura = 40
        self.posicao = [LARGURA_JANELA // 2 - self.largura // 2, ALTURA_JANELA - 50]
        self.velocidade = 5

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.posicao[0] -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.posicao[0] += self.velocidade
        if teclas[pygame.K_UP]:
            self.posicao[1] -= self.velocidade
        if teclas[pygame.K_DOWN]:
            self.posicao[1] += self.velocidade

        #adicionando bordas para o jogador o alvo não sair da tela
        self.posicao[0] = max(0, min(self.posicao[0], LARGURA_JANELA - self.largura))
        self.posicao[1] = max(0, min(self.posicao[1], ALTURA_JANELA - self.altura))

    def reset(self):
        self.posicao = [LARGURA_JANELA // 2 - self.largura // 2, ALTURA_JANELA - 50]

class Alvo:
    def __init__(self):
        self.imagem = alvo_imagem
        self.largura = 100
        self.altura = 100
        self.posicao = [random.randint(0, LARGURA_JANELA - self.largura), random.randint(0, ALTURA_JANELA - self.altura)]
        self.retangulo = pygame.Rect(self.posicao[0], self.posicao[1], self.largura, self.altura)

    def mover_para_uma_nova_posicao(self):
        self.posicao = [random.randint(0, LARGURA_JANELA - self.largura), random.randint(0, ALTURA_JANELA - self.altura)]
        self.retangulo.topleft = self.posicao

    def reset(self):
        self.mover_para_uma_nova_posicao()

# Instanciar o jogo
jogo = Jogo()
clock = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if jogo.estado == ESTADO_JOGANDO:
                jogo.verificar_clique_no_alvo(mouse_x, mouse_y)
            elif jogo.estado == ESTADO_INICIO:
                if LARGURA_JANELA // 2 - 100 <= mouse_x <= LARGURA_JANELA // 2 + 100 and ALTURA_JANELA // 2 <= mouse_y <= ALTURA_JANELA // 2 + 50:
                    jogo.iniciar_jogo()
                elif LARGURA_JANELA // 2 - 100 <= mouse_x <= LARGURA_JANELA // 2 + 100 and ALTURA_JANELA // 2 + 100 <= mouse_y <= ALTURA_JANELA // 2 + 150:
                    jogo.configuracoes()
                    pass
            elif jogo.estado == ESTADO_FIM:
                if LARGURA_JANELA // 2 - 100 <= mouse_x <= LARGURA_JANELA // 2 + 100 and ALTURA_JANELA // 2 - 50 <= mouse_y <= ALTURA_JANELA // 2:
                    jogo.reiniciar_jogo()
                elif LARGURA_JANELA // 2 - 100 <= mouse_x <= LARGURA_JANELA // 2 + 100 and ALTURA_JANELA // 2 + 10 <= mouse_y <= ALTURA_JANELA // 2 + 60:
                    jogo.estado = ESTADO_INICIO

    if jogo.estado == ESTADO_JOGANDO:
        teclas = pygame.key.get_pressed()
        jogo.jogador.mover(teclas)
        jogo.atualizar_estado_jogo()
    jogo.desenhar_estado()
    pygame.display.flip()
    #fps 
    clock.tick(120)
