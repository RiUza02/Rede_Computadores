import socket
import sys

# Valida os argumentos da linha de comando
if len(sys.argv) < 3:
    print("[ERRO] Uso correto: python echo_cliente.py <nome_usuario> <host>")
    sys.exit(1)

nome_usuario = sys.argv[1]
host = sys.argv[2]
porta = 4444

# Cria o socket e estabelece conexão com o servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((host, porta))
    print(f'[INFO] Conectado ao servidor {host}:{porta} como "{nome_usuario}".')

    while True:
        # Entrada de comandos pelo usuário
        mensagem = input('Digite um comando: ')
        
        # Envia a mensagem ao servidor
        cliente.sendall(mensagem.encode('utf-8'))
        
        # Verifica solicitação de encerramento
        if mensagem.strip() == 'exit':
            print('[INFO] Encerrando sessão por comando do usuário.')
            break
        
        # Recebe e exibe a resposta do servidor
        resposta = cliente.recv(1024).decode('utf-8')
        print(f'[RESPOSTA] {resposta}')

except ConnectionRefusedError:
    print(f'[ERRO] Não foi possível conectar ao servidor {host}:{porta}. Verifique se ele está ativo.')

except (KeyboardInterrupt, EOFError):
    print('\n[INFO] Encerramento solicitado pelo usuário (Ctrl+C / Ctrl+D).')

finally:
    cliente.close()
    print('[INFO] Conexão finalizada com sucesso.')