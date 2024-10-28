import xmlrpc.client
import time
import os
import platform

# conectar ao servidor e obter o jogador
server = xmlrpc.client.ServerProxy("http://localhost:8000/")
jogador = server.conectar_jogador()
print(f"Você é o jogador {jogador}")

def limpar_terminal():
    sistema_operacional = platform.system()
    if sistema_operacional == 'Linux':
        os.system('clear')
    elif sistema_operacional == 'Windows':
        os.system('cls')

def exibir_tabuleiro():
    print(server.mostrar_tabuleiro())

def exibir_vencedor():
    vencedor = server.get_vencedor()
    
    limpar_terminal()
    exibir_tabuleiro()
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("                         FIM DE JOGO!")
    print(f"                         Vencedor: {vencedor}")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")

while not server.esperar_jogadores():
    print("Aguardando o outro jogador...")
    time.sleep(1)

def jogar():
    while True:
        jogador_atual = server.get_jogador_atual()

        limpar_terminal()
        exibir_tabuleiro()
        print(f"Jogador {jogador_atual} é o próximo.")

        if jogador != jogador_atual:
            print("Aguardando a vez do outro jogador...")
            while jogador != server.get_jogador_atual():
                time.sleep(1)
                if (server.get_vencedor()):
                    exibir_vencedor()
                    exit()
            continue

        linha = int(input("Digite a linha: "))
        coluna = int(input("Digite a coluna: "))

        # Enviar jogada para o servidor
        resultado = server.fazer_jogada(linha, coluna)
        
        if ("venceu" in resultado) or ("Jogo já terminou" in resultado):
            exibir_vencedor()
            exit()
        else:
            print(resultado)
            time.sleep(0.5)

jogar()
