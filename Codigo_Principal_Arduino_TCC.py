#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import serial
import time
import re
from datetime import datetime
import pandas as pd

port = "COM7"
s1 = serial.Serial(port,9600)


# In[ ]:


def captura_informacao():
    
    dfpzem = pd.read_csv('./base/Dados_PZEM.csv', sep=';')
    dfpzem = dfpzem.tail(3)
    soma_medida = dfpzem['Potência'].sum()
    
    return soma_medida


# In[ ]:


def prioridade(df, potencia_medida, potencia_maxima, comando, ultimo_comando):
    print('toaqui', comando, ultimo_comando)
    if comando != '':
        intervalo = 3
        equip1 = df['Nome do Equipamento'][0]
        comando_equip1_ligar = list(df_comandos[df_comandos['Nome do Equipamento'] == equip1]['Comando_Ligar'])[0]
        comando_equip1_desligar = list(df_comandos[df_comandos['Nome do Equipamento'] == equip1]['Comando_Desligar'])[0]
        equip2 = df['Nome do Equipamento'][1]
        comando_equip2_ligar = list(df_comandos[df_comandos['Nome do Equipamento'] == equip2]['Comando_Ligar'])[0]
        comando_equip2_desligar = list(df_comandos[df_comandos['Nome do Equipamento'] == equip2]['Comando_Desligar'])[0]
        equip3 = df['Nome do Equipamento'][2]
        comando_equip3_ligar = list(df_comandos[df_comandos['Nome do Equipamento'] == equip3]['Comando_Ligar'])[0]
        comando_equip3_desligar = list(df_comandos[df_comandos['Nome do Equipamento'] == equip3]['Comando_Desligar'])[0]
        if comando != ultimo_comando:
            s1.write(bytes(comando, "utf-8"))

        time.sleep(3)
        grava_info_pzem()
        soma_medida = captura_informacao()

        print(soma_medida)

        if soma_medida > potencia_maxima:
            s1.write(bytes(comando_equip3_desligar, "utf-8"))
            arquivo_desligar = open('arquivo_desligar.txt', 'w')
            arquivo_desligar.close()
            arquivo_desligar = open('arquivo_desligar.txt', 'a')
            arquivo_desligar.write('Desligar '+df_comandos['Nome do Equipamento'][2])
            arquivo_desligar.close()
            time.sleep(3)
            grava_info_pzem()
            soma_medida = captura_informacao()
            if soma_medida > potencia_maxima:
                s1.write(bytes(comando_equip2_desligar, "utf-8"))
                arquivo_desligar = open('arquivo_desligar.txt', 'w')
                arquivo_desligar.close()
                arquivo_desligar = open('arquivo_desligar.txt', 'a')
                arquivo_desligar.write('Desligar '+df_comandos['Nome do Equipamento'][1])
                arquivo_desligar.close()
                time.sleep(3)
                grava_info_pzem()
                soma_medida = captura_informacao()
                if soma_medida > potencia_maxima:
                    s1.write(bytes(comando_equip1_desligar, "utf-8"))
                    arquivo_desligar = open('arquivo_desligar.txt', 'w')
                    arquivo_desligar.close()
                    arquivo_desligar = open('arquivo_desligar.txt', 'a')
                    arquivo_desligar.write('Desligar '+df_comandos['Nome do Equipamento'][0])
                    arquivo_desligar.close()
                    time.sleep(3)
                    grava_info_pzem()
                    soma_medida = captura_informacao()
        else:
            if comando != ultimo_comando:
                s1.write(bytes(comando, "utf-8"))
                grava_info_pzem()


# In[ ]:


potencia_maxima = 200


# In[ ]:


def grava_info_pzem():
#     try:
#     time.sleep(2)
    info = s1.read_all()
    
    if info != b'' and len(str(info))>=173:
        dados = str(info).replace("b'", '').replace("'", '').split('#')[-2]
#         print('toaqui2')
        dados = dados.split('|||')[0:3]

        df_final = pd.read_csv('./base/Dados_PZEM.csv', sep=';')

        df = pd.DataFrame()
        # 
        df['Data/Hora'] = []
        df['Tensão'] = []
        df['Corrente'] = []
        df['Potência'] = []
        df['Equipamento'] = []

        lista_data = []
        lista_tensao = []
        lista_corrente = []
        lista_potencia = []
        lista_equipamento = []

#             print('toaqui')

        for i in dados:
            equipamento = i.split(' - ')[0]
            tensao = i.split(' - ')[1].split('|')[0]
            corrente = i.split(' - ')[1].split('|')[1]
            potencia = i.split(' - ')[1].split('|')[2]
            lista_data.append(datetime.now().strftime('%d/%m/%Y %H:%M'))
            lista_tensao.append(float(tensao.replace('Voltage: ', '').replace("NAN", "0").replace('V', '')))
            lista_corrente.append(float(corrente.replace('Current: ', '').replace("NAN", "0").replace('A', '')))
            lista_potencia.append(float(potencia.replace('Power: ', '').replace("NAN", "0").replace('W', '')))
            lista_equipamento.append(equipamento)

        df['Data/Hora'] = lista_data
        df['Tensão'] = lista_tensao
        df['Corrente'] = lista_corrente
        df['Potência'] = lista_potencia
        df['Equipamento'] = lista_equipamento

        df_final = pd.concat([df_final, df])
        df_final.to_csv('./base/Dados_PZEM.csv', sep=';', index=False)
#     except:
#         pass


# In[ ]:


ultimo_comando = ''


# In[ ]:


while True:
    
    df_comandos = pd.read_excel('./base/Prioridades.xlsx')
    
    acionamento_offgrid = open('acionamento_offgrid.txt', 'r')
    
    linha_off = acionamento_offgrid.read().split('\n')[-1]

    #Leitura do arquivo txt acionamento
    acionamento=open('acionamento.txt', 'r')

    #pega a ultima linha do arquivo txt
    linha = acionamento.read().split('\n')[-1]
#     print(linha)
    
    
    if linha_off == "Ligar Offgrid":

        if linha == 'Ligar Geladeira':
            #envia informação para o arduino
            prioridade(df_comandos, captura_informacao(), potencia_maxima, '1', ultimo_comando)
            ultimo_comando = '1'
        elif linha == 'Desligar Geladeira':
            prioridade(df_comandos, captura_informacao(), potencia_maxima, 'A', ultimo_comando)
            ultimo_comando = 'A'
        elif linha == 'Ligar Motor':
            prioridade(df_comandos, captura_informacao(), potencia_maxima, '2', ultimo_comando)
            ultimo_comando = '2'
        elif linha == 'Desligar Motor':
            prioridade(df_comandos, captura_informacao(), potencia_maxima, 'B', ultimo_comando)
            ultimo_comando = 'B'
        elif linha == 'Ligar Lampada':
            prioridade(df_comandos, captura_informacao(), potencia_maxima, '3', ultimo_comando)
            ultimo_comando = '3'
        elif linha == 'Desligar Lampada':
            prioridade(df_comandos, captura_informacao(), potencia_maxima, 'C', ultimo_comando)
            ultimo_comando = 'C'

        prioridade(df_comandos, captura_informacao(), potencia_maxima, '', ultimo_comando)

    else:
        
        if linha == 'Ligar Geladeira':
            #envia informação para o arduino
            s1.write(bytes(str(list(df_comandos[df_comandos['Nome do Equipamento']=='Geladeira']['Comando_Ligar'])[0]), 'utf-8'))
        elif linha == 'Desligar Geladeira':
            s1.write(bytes(str(list(df_comandos[df_comandos['Nome do Equipamento']=='Geladeira']['Comando_Desligar'])[0]), 'utf-8'))
        elif linha == 'Ligar Motor':
            s1.write(bytes(str(list(df_comandos[df_comandos['Nome do Equipamento']=='Motor']['Comando_Ligar'])[0]), 'utf-8'))
        elif linha == 'Desligar Motor':
            s1.write(bytes(str(list(df_comandos[df_comandos['Nome do Equipamento']=='Motor']['Comando_Desligar'])[0]), 'utf-8'))
        elif linha == 'Ligar Lampada':
            s1.write(bytes(str(list(df_comandos[df_comandos['Nome do Equipamento']=='Iluminação']['Comando_Ligar'])[0]), 'utf-8'))
        elif linha == 'Desligar Lampada':
            s1.write(bytes(str(list(df_comandos[df_comandos['Nome do Equipamento']=='Iluminação']['Comando_Desligar'])[0]), 'utf-8'))
        

    grava_info_pzem()
    
#     time.sleep(2)


# In[ ]:




