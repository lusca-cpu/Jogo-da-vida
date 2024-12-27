import pygame
import time

class Celula(pygame.sprite.Sprite):
    def __init__(self, pos, estado, grupo, matriz):
        super().__init__(grupo)
        self.image = pygame.Surface((20, 20))
        self.estado = estado  # 0 = morto, 1 = vivo
        self.vivo_morto()
        self.rect = self.image.get_rect(topleft=pos)
        self.matriz = matriz

    def vivo_morto(self):
        if self.estado == 0:
            self.image.fill('grey')
        else:
            self.image.fill('blue')

    def click(self):
        mouse = pygame.mouse.get_pressed()
        click = pygame.mouse.get_pos()  # Obtém a posição do clique apenas uma vez

        if mouse[0]:  # Botão esquerdo do mouse
            if self.rect.collidepoint(click):  # Verifica se o clique está na célula
                # Muda o estado da célula
                self.estado = 1 if self.estado == 0 else 0
                
                # Atualiza a célula na matriz
                i = self.rect.topleft[1] // 21  # Y da célula em matriz (divido por 21 para obter o índice)
                j = self.rect.topleft[0] // 21  # X da célula em matriz (divido por 21 para obter o índice)
                self.matriz[i][j] = self.estado

        self.vivo_morto()

    def update(self):
        self.click()


class Botao(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('botao.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 45))
        self.rect = self.image.get_rect(topleft=(90, 350))

        self.touche = False

    def update(self):
        if pygame.mouse.get_pressed()[0]:  # Botão esquerdo pressionado
            pos = pygame.mouse.get_pos()  # Posição do mouse
            if self.rect.collidepoint(pos):  # Verifica se clicou no botão
                self.touche = True
        else:
            self.touche = False


class JogoDaVida:
    def __init__(self):
        pygame.init()

        self.tela = pygame.display.set_mode((336, 400))
        self.tela.fill('white')
        pygame.display.set_caption("Jogo da Vida")

        self.relogio = pygame.time.Clock()
        self.rodando = True

        self.celulas = pygame.sprite.Group()
        self.matriz = self.criando_matriz()

        self.tempo_ultimo_clique = 0 
        self.intervalo_clique = 300

    def criando_matriz(self):
        x, y = 0, 0
        matrix = [[0] * 16 for _ in range(16)]

        # Configuração inicial das células vivas
        matrix[1][3] = 1
        matrix[2][4] = 1
        matrix[3][2] = 1
        matrix[3][3] = 1
        matrix[3][4] = 1

        # Criar células
        for i in range(16):
            for j in range(16):
                Celula((x, y), matrix[i][j], self.celulas, matrix)
                x += 21
            x = 0
            y += 21

        return matrix

    def vizinhos(self,matrix):
        linhas = len(matrix)
        colunas = len(matrix[0])
        count = 0
        for i in range(linhas):
            for j in range(colunas):
                count += matrix[i][j]

        return count-1

    def regras(self):
        matrix = self.matriz
        atualiza = []
        for i in range(16):
            for j in range(16):
                matrix2 = []
                for x in range(-1, 2):
                    linha = []
                    for y in range(-1, 2):
                        a, b = i + x, j + y
                        if 0 <= a < 16 and 0 <= b < 16:
                            linha.append(matrix[a][b])
                        else:
                            linha.append(0)
                    matrix2.append(linha)

                if matrix[i][j] == 1:
                    if (self.vizinhos(matrix2) < 2) or (self.vizinhos(matrix2) > 3):
                        atualiza.append([i, j])  
                else:
                    if self.vizinhos(matrix2) + 1 == 3:
                        atualiza.append([i, j])

        # Atualiza os estados das células
        for i in atualiza:
            if matrix[i[0]][i[1]] == 1:
                matrix[i[0]][i[1]] = 0
                # Atualize a cor na célula
                for celula in self.celulas:
                    if celula.rect.topleft == (i[1] * 21, i[0] * 21):
                        celula.estado = 0
                        celula.vivo_morto()
            else:
                matrix[i[0]][i[1]] = 1
                # Atualize a cor na célula
                for celula in self.celulas:
                    if celula.rect.topleft == (i[1] * 21, i[0] * 21):
                        celula.estado = 1
                        celula.vivo_morto()

    def rodar(self):
        ButtonGrups = pygame.sprite.Group()
        botao = Botao(ButtonGrups)

        while self.rodando:
            tempo_atual = pygame.time.get_ticks()
            self.relogio.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False

            # Limpa a tela
            self.tela.fill('white')

            self.celulas.update()

            if botao.touche and tempo_atual - self.tempo_ultimo_clique > self.intervalo_clique:
                self.regras()
                self.tempo_ultimo_clique = tempo_atual
                
            # Desenha os sprites
            self.celulas.draw(self.tela)
            ButtonGrups.draw(self.tela)
            ButtonGrups.update()

            # Atualiza a tela
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    jogo = JogoDaVida()
    jogo.rodar()
