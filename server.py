from xmlrpc.server import SimpleXMLRPCServer
import threading

TAMANHO_TABULEIRO = 10

class Servidor:
    def __init__(self):
        self.tabuleiro = [[' ' for _ in range(TAMANHO_TABULEIRO)] for _ in range(TAMANHO_TABULEIRO)]
        self.jogador_atual = 'X'
        self.vencedor = None
        self.jogadores_conectados = 0
        self.jogador_x_conectado = False
        self.jogador_o_conectado = False

    def conectar_jogador(self):
        if not self.jogador_x_conectado:
            self.jogador_x_conectado = True
            self.jogadores_conectados += 1
            return "X"
        elif not self.jogador_o_conectado:
            self.jogador_o_conectado = True
            self.jogadores_conectados += 1
            return "O"
        else:
            return None

    def esperar_jogadores(self):
        return self.jogadores_conectados == 2
    
    def get_jogador_atual(self):
        return self.jogador_atual
    
    def get_vencedor(self):
        return self.vencedor

    def mostrar_tabuleiro(self):
        # cabeçalho das colunas
        indices = "    " + "  ".join([f"{i:2}" for i in range(1, TAMANHO_TABULEIRO+1)]) + "\n"
        separador = "   " + "-" * (TAMANHO_TABULEIRO * 4 + 1) + "\n"

        # linhas do tabuleiro
        tabuleiro_str = ""
        for i, linha in enumerate(self.tabuleiro, 1):
            linha_str = f"{i:2} | " + " | ".join(linha) + " |\n"
            tabuleiro_str += linha_str + separador

        # retorna o tabuleiro com o cabeçalho
        return indices + separador + tabuleiro_str

    def fazer_jogada(self, linha, coluna):
        # decrementa linha e coluna para poder acessar a posição certa na matriz
        linha -= 1
        coluna -= 1

        # verifica se o a posição é válida ou se já está ocupada
        if linha < 0 or linha >= TAMANHO_TABULEIRO or coluna < 0 or coluna >= TAMANHO_TABULEIRO:
            return "Posição inválida!"

        if self.tabuleiro[linha][coluna] != ' ':
            return "Posição já ocupada!"

        # faz a jogada
        self.tabuleiro[linha][coluna] = self.jogador_atual

        # verifica vitória
        if self.verificar_vitoria(linha, coluna):
            self.jogo_terminado = True
            self.vencedor = self.jogador_atual
            return f"Jogador {self.jogador_atual} venceu!"

        # alterna o jogador
        self.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'

        return "Jogada realizada com sucesso!"

    def verificar_vitoria(self, linha, coluna):
        return (self.verificar_horizontal(linha, coluna) or
                self.verificar_vertical(linha, coluna) or
                self.verificar_diagonal_principal(linha, coluna) or
                self.verificar_diagonal_secundaria(linha, coluna))

    def verificar_horizontal(self, linha, coluna):
        contagem = 1
        for i in range(1, 5):
            if (coluna + i < TAMANHO_TABULEIRO) and (self.tabuleiro[linha][coluna + i] == self.jogador_atual):
                contagem += 1
            else:
                break
        for i in range(1, 5):
            if (coluna - i >= 0) and (self.tabuleiro[linha][coluna - i] == self.jogador_atual):
                contagem += 1
            else:
                break
        return contagem >= 5

    def verificar_vertical(self, linha, coluna):
        contagem = 1
        for i in range(1, 5):
            if (linha + i < TAMANHO_TABULEIRO) and (self.tabuleiro[linha + i][coluna] == self.jogador_atual):
                contagem += 1
            else:
                break
        for i in range(1, 5):
            if (linha - i >= 0) and (self.tabuleiro[linha - i][coluna] == self.jogador_atual):
                contagem += 1
            else:
                break
        return contagem >= 5

    def verificar_diagonal_principal(self, linha, coluna):
        contagem = 1
        for i in range(1, 5):
            if (linha + i < TAMANHO_TABULEIRO) and (coluna + i < TAMANHO_TABULEIRO) and (self.tabuleiro[linha + i][coluna + i] == self.jogador_atual):
                contagem += 1
            else:
                break
        for i in range(1, 5):
            if (linha - i >= 0) and (coluna - i >= 0) and (self.tabuleiro[linha - i][coluna - i] == self.jogador_atual):
                contagem += 1
            else:
                break
        return contagem >= 5

    def verificar_diagonal_secundaria(self, linha, coluna):
        contagem = 1
        for i in range(1, 5):
            if (linha + i < TAMANHO_TABULEIRO) and (coluna - i >= 0) and (self.tabuleiro[linha + i][coluna - i] == self.jogador_atual):
                contagem += 1
            else:
                break
        for i in range(1, 5):
            if (linha - i >= 0) and (coluna + i < TAMANHO_TABULEIRO) and (self.tabuleiro[linha - i][coluna + i] == self.jogador_atual):
                contagem += 1
            else:
                break
        return contagem >= 5

def iniciar_servidor():
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    servidor = Servidor()
    server.register_instance(servidor)
    print("Servidor iniciado e aguardando jogadores...")

    # thread para esperar os jogadores
    threading.Thread(target=servidor.esperar_jogadores).start()

    server.serve_forever()

iniciar_servidor()
