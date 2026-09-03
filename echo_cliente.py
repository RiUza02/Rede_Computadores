import socket
import sys

#garante que o host e a porta
if len(sys.argv) < 3:
    sys.exit(1)
tela = sys.argv[1]
host = sys.argv[2]
print(tela, host)
porta = 4444

#conecta com o servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, porta))
print(f'Acho que os cara tão no teto. (cliente {tela} conectado: {host},{porta})')

try:
    while True:
        #mensagem do usuário
        mensagem = input('o que você quer falar? ')
        
        #enviando a mensagem
        cliente.sendall(mensagem.encode('utf-8'))
        
        if(mensagem.strip() == 'exit'):
            print(f'vou sair daqui (cliente {tela} desconectado: {host},{porta})')
            break
        
        #imprime a resposta do servidor
        resposta = cliente.recv(1024).decode('utf-8')
        print(f'você escuta "{resposta}" vindo do teto')
        
except (KeyboardInterrupt, EOFError):
    #garante que o programa não quebre com ctrl+c ou ctrl+d
    pass

finally:
    #fecha a coneção
    print('\nporque ele repete o que eu falo? Vou é sair daqui (cliente desconectado)') 
    cliente.close()