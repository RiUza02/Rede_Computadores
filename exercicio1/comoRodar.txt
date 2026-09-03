================================================================================
 MANUAL DE INSTRUÇÕES - SISTEMA CLIENTE-SERVIDOR ECHO (PYTHON)
================================================================================

1. REQUISITOS PRÉVIOS
--------------------------------------------------------------------------------
- Python 3.x instalado no sistema.
- Dois arquivos salvos na mesma pasta:
  * echo_server.py  (Código do Servidor Multi-threaded)
  * echo_cliente.py (Código do Cliente)


2. PASSOS PARA EXECUÇÃO
--------------------------------------------------------------------------------

PASSO 1: Iniciar o Servidor
1. Abra um terminal de comando (CMD, PowerShell ou Terminal Linux/Mac).
2. Navegue até a pasta onde os arquivos estão salvos.
3. Execute o comando:
   python echo_server.py

O terminal exibirá a confirmação:
"[INFO] Servidor ativo e aguardando conexões em 127.0.0.1:4444"


PASSO 2: Conectar um ou mais Clientes
1. Abra um NOVO terminal (mantenha o terminal do servidor em execução).
2. Navegue até a mesma pasta.
3. Execute o cliente informando seu nome de usuário e o host:
   python echo_cliente.py <nome_usuario> 127.0.0.1

Exemplo:
   python echo_cliente.py Yuri 127.0.0.1

(Para testar a concorrência, abra outros terminais adicionais e execute o 
mesmo comando alterando apenas o nome do usuário).


3. COMANDOS DISPONÍVEIS NO CLIENTE
--------------------------------------------------------------------------------

Após a conexão, você verá o prompt "Digite um comando:". Utilize as instruções:

- Repetir uma mensagem (Echo):
  Sintaxe: echo <sua mensagem>
  Exemplo: echo Olá, mundo!
  Retorno: Olá, mundo!

- Encerrar a sessão do cliente:
  Sintaxe: exit
  Retorno: Conexão finalizada com sucesso.

- Trata de Comandos Inválidos:
  Se você digitar qualquer frase sem o prefixo "echo " ou diferente de "exit", 
  o sistema retornará uma mensagem de erro com as orientações de sintaxe.
================================================================================