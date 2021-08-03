import os
import tkinter as tk

import routeros_api

# Cria instancia da janela
window = tk.Tk()
window.title('Eu sei a Marca by Eduardo Filho')
window.configure(bg='#111010')
lado, cima = (window.winfo_screenwidth() - 700), (window.winfo_screenheight() - 300)
window.geometry('%dx%d+0+0' % (lado, cima))

diret = "/"
filename = "bg.png"


#  Metodo encontra onde está o arquivo, no computador para poder evitar problemas com uso do programa em outros PCs
def achar_arq():
    for roots, dirs, files in os.walk(diret):

        if filename in files:
            print(os.path.join(roots, filename))
        if filename not in files:
            print('None')

    print(achar_arq())


# imagem de fundo
imgbg = tk.PhotoImage(file=filename)
lbBg = tk.Label(window, image=imgbg)
lbBg.place(x=0, y=0, relwidth=1, relheight=1)  # Utilizando place para mostrar label atrás do gerenciador .pack()

# Label que será usada para mostrar na tela os resultados do método ONCLICK()
lbOut = tk.Label(window, font=('Helvitica', 15, 'bold'), text=' ', bg='#070708', fg='white')
outText = ''
lbOut['text'] = outText

# Imagem da logo no taskbar
diret2 = '/'
filelogo = 'logo.png'


#  Metodo encontra onde está o arquivo, no computador para poder evitar problemas com uso do programa em outros PCs
def achar_arq():
    for roots, dirs, files in os.walk(diret2):

        if filename in files:
            print(os.path.join(roots, filelogo))
        if filename not in files:
            print('None')

    print(achar_arq())
imglogo = tk.PhotoImage(file=filelogo)
window.wm_iconphoto(True, imglogo)


def Onclick():
    print('Onclick')
    host = enHost.get()
    login = enLogin.get()
    print(host)
    # LISTA (TUPLE) DE IP DOS CONCENTRADORES
    address_list = [
        ('aldeota1', '172.17.0.92'), ('aldeotai', '172.17.0.92'),
        ('aldeota2', '172.17.0.137'), ('aldeotaii', '172.17.0.137'),
        ('aquiraz', '172.17.0.125'), ('aquir', '172.17.0.125'),
        ('coacu', '172.17.0.97'), ('coaçu', '172.17.0.97'),

        ('damas', '172.17.0.65'),
        ('diasmacedo', '172.17.0.49'),

        ('esperanca', '172.17.0.87'), ('esperança', '172.17.0.87'),

        ('guararapes', '172.17.0.11'), ('guarara', '172.17.0.11'), ('guararape', '172.17.0.11'),

        ('messejana1', '172.17.0.12'), ('messejanai', '172.17.0.12'), ('josedealencar1', '172.17.0.12'),

        ('messejana2', '172.17.0.96'), ('messejanaii', '172.17.0.96'),

        ('messejanashell', '172.17.0.134'), ('messejananovo', '172.17.0.134'), ('postoms', '172.17.0.134'),
        ('passare', '172.17.0.8'), ('passaré', '172.17.0.8'),
        ('pedrabranca', '172.17.0.10'), ('pedra', '172.17.0.10'),

        ('portodunas', '172.17.0.25'),
        ('portodasdunas', '172.17.0.25'),
        ('portaldunas', '172.17.0.25'),
        ('portaldasdunas', '172.17.0.25'),

        ('saogerardo', '172.17.0.105'),
        ('viasul', '172.20.3.2')]

    # ADICIONA LISTA A PARA UM DICIONARIO
    address_dict = dict(address_list)

    # iniciando
    user = 'suporte'  # NOME DE USUARIO PARA LOGAR NO MIKROTIK
    senha = 'oluap186'  # SENHA PARA LOGAR NO MIKROTIK
    ip = 'RECEBE IP'  # IP OU DOMÍNIO DO MIKROTIK
    concentrador = host.strip()  # RECEBE DADOS DO IP OU NOME DO MK, E TIRA ESPACOS
    sempontos = str(
        ''.join(concentrador.split('.')))  # TIRA PONTOS DA VARIAVEL concentrador E PARA PODER CONFERIR SE É IP OU NOME
    # print(sempontos)
    pontosespaco = str(
        ''.join(sempontos.lower().split(' ')))  # TIRA PONTOS E ESPACOS PARA ACHAR O NOME NO DICIONARIO address_list
    # print(pontosespaco)
    espaco = str(
        ''.join(concentrador.lower().split(' ')))  # TIRA ESPACOS PARA RECEBER IP CORRETAMENTE (CASO TENHAM DIGITADO IP)
    # print(espaco)

    if pontosespaco.isnumeric():  # SE SEM PONTOS E ESPACOS SAO NUMERICOS
        ip = espaco  # RECEBE O IP DIGITADO
    else:
        nome = pontosespaco
        if nome in address_dict:
            ip = address_dict[nome]
            print(ip)
        else:
            outText = str('Não encontrei o nome desse Concentrador, pode tentar de novo?')
            lbOut['text'] = outText
            return

    # FAZ CONEXÃO VIA api NO MIKROTIK DIGITADO
    connection = routeros_api.RouterOsApiPool(host=ip, username=user, password=senha, plaintext_login=True)
    api = connection.get_api()
    list_address = api.get_resource('/interface/pppoe-server')  # COMANDO PARA PEGAR DADOS DOS CLIENTES PPPOE
    # API

    pppoe = login.strip()

    # r - recebera um dicionario sobre o usuario pppoe digitado
    r = str(list_address.get(user=pppoe))

    # verifica se consiguiu achar pppoe no mikrotik
    if r == '[]':
        outText = 'Não achei o PPPOE, cliente pode estar Off,\n não ser desse concentrador,\n ou você escreveu ' \
                  'errado, tente de novo '
        lbOut['text'] = outText
        connection.disconnect()
        return
    else:
        pass

    # a - responsavel por encontrar a primeira posicao no dicionirio r para calcula feito abaixo
    a = ''.join(r.split()).find('remote-address')

    # b - Calcula a posicao do MAC ADDRESS a partir da variavel - a
    b = ''.join(r.split())[int(a + 17):int(a + 17 * 2)]
    # print(b)

    # https://api.macvendors.com/FC-A1-3E-2A-1C-33 link de api

    from requests import get
    mac_request = get('https://api.macvendors.com/{}'.format(b))  # ENVIA MAC ADDRESS CAPTURADO PELA API

    if mac_request.status_code == 404:
        print('Mac não encontrado, por favor tente novamente!\n{:=^50}'.format(''))
        outText = ('Mac não encontrado, por favor tente novamente!\n{:=^50}'.format(''))
        lbOut['text'] = outText
        connection.disconnect()
    else:
        print(mac_request)
        print(('\n{:=^50}'.format(' ' + mac_request.text + ' ')).upper())
        outText = str('\n{:=^50}'.format(' ' + mac_request.text + ' ')).upper()
        lbOut['text'] = outText
        connection.disconnect()
        return


# Lable que mostra o TITULO
lbTitle = tk.Label(window, bg='#070708', fg='#85FC88', text='DESCUBRA A MARCA DO ROTEADOR DO CLIENTE',
                   font=('Helvetica', 15, 'bold'))

# label textos 1 concentrador
lbText1 = tk.Label(window, fg='#85FC88', bg='#070708', text='Digite o nome completo ou IP do concentrador : ',
                   font=('Helvetica', 12, 'bold'))

lbText2 = tk.Label(window, fg='#B9f7bb', bg='#070708', text="Ex: Messejana 1 ou 172.17.0.12",
                   font=("Arial", 8, 'italic'))

# Input (ENTRY) que recebe concentrador
enHost = tk.Entry(window, width=30, bg='white')

# TEXTOS 2 PPPoE
lbText3 = tk.Label(window, text='Digite o PPPoE do cliente: ', font=('Helvetica', 12, 'bold'), bg='#070708',
                   fg='#85FC88')

enLogin = tk.Entry(window, width=30, bg='white')

btn = tk.Button(window, command=Onclick, text='Descobrir a Marca', width=30, bg='#68F56B', fg='#151515',
                font=('Helvetica', 12, 'bold'))

lbTitle.pack(pady=20)
lbText1.pack(anchor='w', padx=20)
enHost.pack(padx=50, anchor='w')
lbText2.pack(anchor='w', padx=30, after=enHost)
lbText3.pack(anchor='w', padx=20, pady=1), enLogin.pack(padx=50, anchor='w')
btn.pack(pady=20)
lbOut.pack()

# Define tamanho da Janela
# window.geometry = ("1280, 720")
# Mantem Janela aberta
window.mainloop()
