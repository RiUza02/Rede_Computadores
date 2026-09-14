import socket
import threading
from comandos import processar_comando

# Mapeamento dos clientes ativos {nome_cliente: socket_cliente}
clientes = {}
lock = threading.Lock()


# Trata a conexão de cada cliente individualmente
def tratar_cliente(cliente, endereco):
    print(f'[INFO] Cliente conectado com sucesso: {endereco}')
    nome_cliente = None  # Inicializa o nome do cliente como None

    try:
        # Recebe a primeira mensagem do cliente, que deve ser o nome de usuário
        primeira_mensagem = cliente.recv(1024).decode('utf-8').strip()
        if primeira_mensagem:
            nome_cliente = primeira_mensagem
            with lock:
                clientes[nome_cliente] = cliente
            print(f'[INFO] Nome do cliente registrado: {nome_cliente} para o endereço {endereco}')

        while True:
            mensagem = cliente.recv(1024).decode('utf-8')

            # Trata encerramento silencioso da conexão
            if not mensagem:
                print(f'[INFO] Conexão finalizada pelo cliente: {endereco}')
                break

            # Processa o comando importado do módulo 'comandos'
            continuar = processar_comando(
                mensagem=mensagem,
                cliente=cliente,
                endereco=endereco,
                nome_cliente=nome_cliente,
                clientes=clientes,
                lock=lock
            )

            # Se o comando retornou False (ex: 'exit'), encerra o loop da thread
            if not continuar:
                break

    except (ConnectionResetError, BrokenPipeError):
        print(f'[ERRO] Conexão perdida inesperadamente com o cliente: {endereco}')
    finally:
        # Garante a remoção do cliente do dicionário ao desconectar
        if nome_cliente:
            with lock:
                clientes.pop(nome_cliente, None)
        print(f'[INFO] Conexão encerrada e recursos liberados para: {endereco}')
        cliente.close()


# Configuração do endereço e porta do servidor
HOST = '127.0.0.1'
PORTA = 4444


def iniciar_servidor():
    # Inicialização do socket TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen()

    print(f'[INFO] Servidor ativo e aguardando conexões em {HOST}:{PORTA}')

    try:
        while True:
            cliente, endereco = servidor.accept()

            # Aloca uma nova thread para o cliente aceito
            thread_cliente = threading.Thread(
                target=tratar_cliente,
                args=(cliente, endereco),
                daemon=True
            )
            thread_cliente.start()

    except KeyboardInterrupt:
        print('\n[INFO] Encerramento do servidor solicitado pelo administrador (Ctrl+C).')

    finally:
        print('[INFO] Servidor finalizado. Socket principal fechado.')
        servidor.close()


if __name__ == '__main__':
    iniciar_servidor()