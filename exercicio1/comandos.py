import threading


def comando_exit(mensagem, cliente, endereco, **kwargs):
    # Comando de encerramento
    print(f'[INFO] Cliente {endereco} enviou o comando de saída (exit).')
    return False  # Retorna False para indicar que o loop deve ser encerrado


def comando_echo(mensagem, cliente, endereco, **kwargs):
    # Comando de eco (o servidor envia de volta a mensagem recebida)
    if mensagem.startswith('echo '):
        conteudo = mensagem[5:]
        print(f'[INFO] Mensagem processada para {endereco}: "{conteudo}"')
        cliente.sendall(conteudo.encode('utf-8'))
    elif mensagem.strip() == 'echo':
        print(f'[INFO] Comando echo recebido de {endereco} sem conteúdo.')
        cliente.sendall(''.encode('utf-8'))
    return True


def comando_chat(mensagem, cliente, endereco, nome_cliente, clientes, lock, **kwargs):
    # Comando de chat (o servidor processa a mensagem para outro cliente)
    partes = mensagem.split(' ', 2)
    if len(partes) == 3:
        destinatario = partes[1]
        conteudo = partes[2]

        with lock:
            socket_destinatario = clientes.get(destinatario)

        print(f'[INFO] Mensagem de chat processada para {destinatario}: "{conteudo}"')

        # Envia a mensagem para o destinatário, se ele estiver conectado
        if socket_destinatario:
            socket_destinatario.sendall(f'Mensagem de {nome_cliente}: {conteudo}'.encode('utf-8'))
            cliente.sendall(f'Mensagem enviada para {destinatario}.'.encode('utf-8'))
        # Se o destinatário não estiver conectado, envia uma mensagem de erro ao remetente
        else:
            print(f'[AVISO] Destinatário "{destinatario}" não encontrado para {endereco}.')
            resposta_erro = f'ERRO: Destinatário "{destinatario}" não encontrado.'
            cliente.sendall(resposta_erro.encode('utf-8'))
    else:
        print(f'[AVISO] Formato de mensagem de chat inválido recebido de {endereco}: "{mensagem}"')
        resposta_erro = "ERRO: Formato de mensagem de chat inválido. Sintaxe válida: 'chat <destinatário> <mensagem>'."
        cliente.sendall(resposta_erro.encode('utf-8'))
    
    return True


# Mapeamento de comandos do servidor
MAPA_COMANDOS = {
    'exit': comando_exit,
    'echo': comando_echo,
    'chat': comando_chat,
}


def processar_comando(mensagem, cliente, endereco, nome_cliente, clientes, lock):
    """
    Identifica o comando recebido e delega o processamento para a função apropriada.
    """
    comando_prefixo = mensagem.strip().split(' ', 1)[0]
    handler = MAPA_COMANDOS.get(comando_prefixo)

    if handler:
        return handler(
            mensagem=mensagem,
            cliente=cliente,
            endereco=endereco,
            nome_cliente=nome_cliente,
            clientes=clientes,
            lock=lock
        )

    # Tratamento de erro para comandos desconhecidos
    print(f'[AVISO] Comando inválido recebido de {endereco}: "{mensagem}"')
    resposta_erro = "ERRO: Comando não reconhecido. Sintaxe válida: 'echo <mensagem>' ou 'exit'."
    cliente.sendall(resposta_erro.encode('utf-8'))
    return True