import socket
import threading

#trata cada cliente por separado
def tread(cliente, endereco):
    
    #avisa que tem um cliente
    print(f'To escutando um cara aqui. (servidor conectado: {endereco})')

    #escuta e repete
    try:
        while True:
                    #recebe a mensagem do cliente
                    mensagem = cliente.recv(1024).decode('utf-8')
                                        
                    #para se não tiver mensagem
                    if not mensagem:
                        print(f'Não escuto mais ninguém, vou sair (cliente desconectado: {endereco})')
                        break
                    
                    
                    
                    #comando exit (avisa que o cliente quer sair)
                    if mensagem.strip() == 'exit':
                        print(f'O cara na sala {endereco} saiu, não consigo escutar mais (cliente desconectado: {endereco})')
                        break
                    
                    
                    
                    #comando echo (reenvia a mensagem)
                    elif mensagem.startswith('echo '):
                        #tira a palavra echo da mensagem
                        conteudo = mensagem[5:]
                        print(f'Escutei "{conteudo}" vindo da sala {endereco}, vou repetir (mensagem recebida)')
                        cliente.sendall(conteudo.encode('utf-8'))
                        
                        
                        
                    #comandos invalidos
                    else:
                        print(f'Escutei, mas não entendi o que o cara na sala {endereco} falou (comando inválido: {mensagem})')
                        #reenvia a mensagem para o cliente
                        cliente.sendall("Fala direito, parça! (comando inválido)".encode('utf-8'))
    
    
    #trata a desconexão do cliente
    except (ConnectionResetError, BrokenPipeError):
        print(f'Cliente desconectado: {endereco}')
    finally:
        print(f'Quero escutar o cara na sala {endereco} mais não (servidor desconectado)')
        cliente.close()





#porta e host
host = '127.0.0.1'
porta = 4444

#cria o host e configura a porta
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #permite que o socket seja reutilizado
servidor.bind((host, porta))
servidor.listen()

#mensagem de boas vindas :)
print(f'Vou escutar um pouquinho. (servidor escutando: {host},{porta})')
try:
    while True:
        #faz a conexão com o cliente
        cliente, endereco = servidor.accept()
        
        #cria treads
        treadCliente = threading.Thread(
                                        target=tread,
                                        args=(cliente, endereco),
                                        daemon=True     
                                        )
        
        #inicia a tread
        treadCliente.start()
        
#trata o ctrl+c para sair do servidor
except KeyboardInterrupt:
    print('\nvou é sair daqui (servidor desconectado)')

#encera a conexão com o cliente
finally:
    print(f'quero escutar mais não (servidor desconectado)')
    servidor.close()
        