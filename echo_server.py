import socket
import threading

# Trata a conexão de cada cliente individualmente
def tread(cliente, endereco):
    print(f'[INFO] Cliente conectado com sucesso: {endereco}')

    try:
        while True:
            mensagem = cliente.recv(1024).decode('utf-8')
            
            # Trata encerramento silencioso da conexão
            if not mensagem:
                print(f'[INFO] Conexão finalizada pelo cliente: {endereco}')
                break
            
            # Comando de encerramento
            if mensagem.strip() == 'exit':
                print(f'[INFO] Cliente {endereco} enviou o comando de saída (exit).')
                break
            
            # Comando de eco
            elif mensagem.startswith('echo '):
                conteudo = mensagem[5:]
                print(f'[INFO] Mensagem processada para {endereco}: "{conteudo}"')
                cliente.sendall(conteudo.encode('utf-8'))

            elif mensagem.strip() == 'echo':
                print(f'[INFO] Comando echo recebido de {endereco} sem conteúdo.')
                cliente.sendall(''.encode('utf-8'))
            
            # Tratamento de erro para comandos desconhecidos
            else:
                print(f'[AVISO] Comando inválido recebido de {endereco}: "{mensagem}"')
                resposta_erro = "ERRO: Comando não reconhecido. Sintaxe válida: 'echo <mensagem>' ou 'exit'."
                cliente.sendall(resposta_erro.encode('utf-8'))
    
    except (ConnectionResetError, BrokenPipeError):
        print(f'[ERRO] Conexão perdida inesperadamente com o cliente: {endereco}')
    finally:
        print(f'[INFO] Conexão encerrada e recursos liberados para: {endereco}')
        cliente.close()


# Configuração do endereço e porta do servidor
host = '127.0.0.1'
porta = 4444

# Inicialização do socket TCP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((host, porta))
servidor.listen()

print(f'[INFO] Servidor ativo e aguardando conexões em {host}:{porta}')

try:
    while True:
        cliente, endereco = servidor.accept()
        
        # Aloca uma nova thread para o cliente aceito
        treadCliente = threading.Thread(
            target=tread,
            args=(cliente, endereco),
            daemon=True     
        )
        treadCliente.start()

except KeyboardInterrupt:
    print('\n[INFO] Encerramento do servidor solicitado pelo administrador (Ctrl+C).')

finally:
    print('[INFO] Servidor finalizado. Socket principal fechado.')
    servidor.close()