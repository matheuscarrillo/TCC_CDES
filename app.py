###Bibliotecas

#flask permite a conexão entre o front e backend
from flask import Flask, render_template, redirect, request, url_for, flash

#Seta as configurações iniciais do arduino
# import liga_arduino

#Utilizado para manipular planilhas do excel
import pandas as pd
#Arduino
import serial
#Utilizado para delays
import time

import struct
import PZEM

#Criar gráfico interativos no html ou python
import pygal

#Biblioteca utilizada para alterar o estilo do Pygal (mudar fonte, cores)
from pygal.style import Style

#Configuração incial
app = Flask(__name__)
app.secret_key = 'fei'


#Seta os botoes como desligado
dict_status = {
'Sistema_OffGrid': False,
'Botao_1': False,
'Botao_2': True,
'Botao_3': False}

#Estilo de gráfico dos equipamentos
custom_style_equipamentos = Style(
  background='transparent',
  foreground='#000000',
  foreground_strong='#000000',
  foreground_subtle='#000000',
  label_font_size=18,
  title_font_size=25,
  legend_font_size=22,
  opacity='1',
  opacity_hover='1',
  transition='400ms ease-in',
  colors=('#006EAA', '#FFC000', '#7B7C7E', '#578439'))

#Estilo de gráfico do sistema
custom_style_sistema = Style(
  background='transparent',
  foreground='#000000',
  foreground_strong='#000000',
  foreground_subtle='#000000',
  label_font_size=18,
  title_font_size=25,
  legend_font_size=22,
  opacity='1',
  opacity_hover='1',
  transition='400ms ease-in',
  colors=('#000182', '#C00000'))



#Rota para tela inicial
#Essa configuração serve para enviar e receber informações na tela.
@app.route("/", methods=['GET', 'POST'])
def index():
    
    df_externo = pd.read_excel('Comando_Externo.xlsx')
    df_externo.fillna('', inplace=True)

    #Se algum botão for pressionado, entra nessa função
    if request.method == 'POST' or df_externo['Comando'][0] != 'N/A':

        #Liga/Desliga Off-Grid
        if "btn_liga_offgrid" in request.form:
            arquivo = open('acionamento_offgrid.txt', 'w')
            arquivo.write('Desligar Offgrid')
            arquivo.close()
            sist_offgrid = False
            dict_status.update({'Sistema_OffGrid': sist_offgrid})
        if "btn_desliga_offgrid" in request.form:
            arquivo = open('acionamento_offgrid.txt', 'w')
            arquivo.write('Ligar Offgrid')
            arquivo.close()
            sist_offgrid = True
            dict_status.update({'Sistema_OffGrid': sist_offgrid})

        #Liga/Desliga Lampada
        if "btn_liga_1" in request.form or df_externo['Comando'][0] == 'Desligar Lampada':
            arquivo = open('acionamento.txt', 'w')
            arquivo.write('Desligar Lampada')
            arquivo.close()

            df_externo['Comando'] = 'N/A'
            df_externo.to_excel('Comando_Externo.xlsx', index=False)


            df_ler = pd.read_excel('Ler_PZEM.xlsx')
            carga = df_ler['Leitura'][0]
            carga = carga-45
            df_ler['Leitura'] = carga
            df_ler.to_excel('Ler_PZEM.xlsx', index=False)
            
            botao_1 = False
            dict_status.update({'Botao_1': botao_1})
        if "btn_desliga_1" in request.form:
            arquivo = open('acionamento.txt', 'w')
            arquivo.write('Ligar Lampada')
            arquivo.close()
            arquivo_desligar = open('arquivo_desligar.txt', 'w')
            arquivo_desligar.close()


            df_ler = pd.read_excel('Ler_PZEM.xlsx')
            carga = df_ler['Leitura'][0]
            carga = carga+45
            df_ler['Leitura'] = carga
            df_ler.to_excel('Ler_PZEM.xlsx', index=False)

            botao_1 = True
            dict_status.update({'Botao_1': botao_1})

        #Liga/Desliga Geladeira
        if "btn_liga_2" in request.form :
            arquivo = open('acionamento.txt', 'w')
            arquivo.write('Desligar Geladeira')
            arquivo.close()

            botao_2 = False
            dict_status.update({'Botao_2': botao_2})
        if "btn_desliga_2" in request.form:
            arquivo = open('acionamento.txt', 'w')
            arquivo.write('Ligar Geladeira')
            arquivo.close()
            botao_2 = True
            dict_status.update({'Botao_2': botao_2})

        #Liga/Desliga Motor
        if "btn_liga_3" in request.form or df_externo['Comando'][0] == 'Desligar Motor':
            arquivo = open('acionamento.txt', 'w')
            arquivo.write('Desligar Motor')
            arquivo.close()

            df_externo['Comando'] = 'N/A'
            df_externo.to_excel('Comando_Externo.xlsx', index=False)

            
            df_ler = pd.read_excel('Ler_PZEM.xlsx')
            carga = df_ler['Leitura'][0]
            carga = carga-60
            df_ler['Leitura'] = carga
            df_ler.to_excel('Ler_PZEM.xlsx', index=False)

            botao_3 = False
            dict_status.update({'Botao_3': botao_3})
        if "btn_desliga_3" in request.form:
            arquivo = open('acionamento.txt', 'w')
            arquivo.write('Ligar Motor')
            arquivo.close()


            
            df_ler = pd.read_excel('Ler_PZEM.xlsx')
            carga = df_ler['Leitura'][0]
            carga = carga+60
            df_ler['Leitura'] = carga
            df_ler.to_excel('Ler_PZEM.xlsx', index=False)
            
            botao_3 = True
            dict_status.update({'Botao_3': botao_3})

        #Vai para a tela de config
        if "goto_config" in request.form:
            return redirect(url_for('configuracao'))

        #Vai para a tela de Dashboard
        if "goto_relatorio" in request.form:
            return redirect(url_for('relatorio'))

    # df_dados_pzem=pd.read_csv('./base/Dados_PZEM.csv', sep=';')
    # df_dados_pzem=df_dados_pzem.tail(3)
    # soma_potencias = df_dados_pzem['Potência'].sum()
    time.sleep(1)

    df_potenciatotal=pd.read_excel('./base/PotenciaTotal.xlsx')
    potencia_total= list(df_potenciatotal['Potencia Total'])[0]

    # arquivo_desligar= open('arquivo_desligar.txt', 'r')
    # status = arquivo_desligar.read()
    # print(status)
    # if status == "Desligar Motor":
    #     status_botao3 = False
    #     dict_status.update({'Botao_3':status_botao3})
    # elif status == "Desligar Lampada":
    #     status_botao1 = False
    #     dict_status.update({'Botao_1':status_botao1})


    df_ler = pd.read_excel('Ler_PZEM.xlsx')
    soma_potencias = df_ler['Leitura'][0]

    pct_pot_inv = 100*soma_potencias/potencia_total
        
    return render_template('index.html', status_offgrid=dict_status.get('Sistema_OffGrid'),status_botao1=dict_status.get('Botao_1'), status_botao2=dict_status.get('Botao_2'), status_botao3=dict_status.get('Botao_3'), soma_potencias=soma_potencias, pct_pot_inv=pct_pot_inv)

#Rota do relatório
#Essa configuração serve para enviar e receber informações na tela.
@app.route("/relatorio", methods=['GET', 'POST'])
def relatorio():

    #Grafico de barra, consumo por equipamento
    consumo_equip_dia = pygal.Bar(style=custom_style_equipamentos)
    consumo_equip_dia.title = 'Consumo por Equipamento Diário'
    consumo_equip_dia.x_labels = map(str, ['Dia 1', 'Dia 2', 'Dia 3', 'Dia 4', 'Dia 5'])
    consumo_equip_dia.add('Geladeira', [10, 10, 12, 11, 13])
    consumo_equip_dia.add('Iluminação',  [5, 4, 6, 5, 5])
    consumo_equip_dia.add('Motor',  [3,  2, 1, 4, 5])
    consumo_equip_dia.render()
    consumo_equip_dia = consumo_equip_dia.render_data_uri()

    #Grafico de barra, consumo sistema comparando com a geração no decorrer da semana
    geracao_consumo_semanal = pygal.Bar(style=custom_style_sistema)
    geracao_consumo_semanal.title = 'Geração x Consumo Semanal'
    geracao_consumo_semanal.x_labels = map(str, ['Dia 1', 'Dia 2', 'Dia 3', 'Dia 4', 'Dia 5'])
    geracao_consumo_semanal.add('Consumo',  [3,  3, 2, 2, 3])
    geracao_consumo_semanal.add('Geração', [2, 4, 5, 3, 6])
    geracao_consumo_semanal.render()
    geracao_consumo_semanal = geracao_consumo_semanal.render_data_uri()

    #Grafico de Pizza, detalhando o consumo de cada equipamento atual
    consumo_equip_atual = pygal.Pie(inner_radius=.4, style=custom_style_equipamentos )
    consumo_equip_atual.title = 'Consumo por Equipamento Atual'
    consumo_equip_atual.add('Geladeira', 11)
    consumo_equip_atual.add('Iluminação', 5)
    consumo_equip_atual.add('Motor', 3)
    consumo_equip_atual = consumo_equip_atual.render_data_uri()

    #Grafico de Linha, comparando o consumo pela geração
    geracao_consumo_pontual = pygal.Line(style=custom_style_sistema)
    geracao_consumo_pontual.title = 'Geração x Consumo Pontual'
    geracao_consumo_pontual.x_labels = map(str, ['00h', '02h', '04h', '06h', '08h', '10h', '12h', '14h', '16h', '18h', '20h', '22h'])
    geracao_consumo_pontual.add('Geração', [1, 2, 3, 4, 4, 5, 5, 4, 4, 3, 2, 1])
    geracao_consumo_pontual.add('Consumo',  [2 ,2, 2, 2, 4, 8, 5, 3, 2, 2, 1,1])
    geracao_consumo_pontual = geracao_consumo_pontual.render_data_uri()

    return render_template('relatorio.html', consumo_equip_dia=consumo_equip_dia, geracao_consumo_semanal=geracao_consumo_semanal, consumo_equip_atual=consumo_equip_atual, geracao_consumo_pontual=geracao_consumo_pontual)


#Rota de configuração
@app.route("/configuracao", methods=['GET', 'POST'])
def configuracao():


    df_prioridade=pd.read_excel('./base/Prioridades.xlsx')
    df_horarios=pd.read_excel('./base/Horarios_offgrid.xlsx')
    df_potenciatotal=pd.read_excel('./base/PotenciaTotal.xlsx')
    nivel_prioridade_geladeira = list(df_prioridade[df_prioridade['Nome do Equipamento']=="Geladeira"]['Nível Prioridade'])[0]
    nivel_prioridade_iluminacao = list(df_prioridade[df_prioridade['Nome do Equipamento']=="Iluminação"]['Nível Prioridade'])[0]
    nivel_prioridade_motor = list(df_prioridade[df_prioridade['Nome do Equipamento']=="Motor"]['Nível Prioridade'])[0]

    #Se algum dos botões for clicado, entra nessa função
    if request.method == "POST":
        #Ajuste de horário funcionamento Off-Grid
        if "aplica_horario" in request.form:
            hora_definida = request.form.get('text_horario')
            if (len(hora_definida.split(':')[0])==2) and (len(hora_definida.split(':')[1])==2):
                ultimo_horario = list(df_horarios['Horários OffGrid'])[-1]
                lista_horarios = [ultimo_horario, hora_definida]
                df_horarios['Horários OffGrid'] = lista_horarios
                df_horarios.to_excel('./base/Horarios_offgrid.xlsx', index=False)
            else:
                flash('Formato Incorreto! Insira o horário no formato HH:MM.', 'error')
        
        #Ajuste de prioridade dos equipamentos
        if "aplica_prioridade" in request.form:
            if request.form.get('equipamento') == 'geladeira':
                nivel_prioridade_geladeira = int(request.form.get('nivel_prioridade'))
                if nivel_prioridade_geladeira == nivel_prioridade_iluminacao:
                    nivel_prioridade_iluminacao = nivel_prioridade_iluminacao+1

                    if nivel_prioridade_iluminacao == nivel_prioridade_motor:
                        nivel_prioridade_motor = nivel_prioridade_motor+1

                    if nivel_prioridade_iluminacao>3:
                        nivel_prioridade_iluminacao = nivel_prioridade_iluminacao-2
                elif nivel_prioridade_geladeira == nivel_prioridade_motor:
                    nivel_prioridade_motor = nivel_prioridade_motor+1
                    if  nivel_prioridade_motor == nivel_prioridade_iluminacao:
                        nivel_prioridade_iluminacao = nivel_prioridade_iluminacao+1

                    if nivel_prioridade_motor>3:
                        nivel_prioridade_motor = nivel_prioridade_motor-2


            if request.form.get('equipamento') == 'iluminacao':
                nivel_prioridade_iluminacao = int(request.form.get('nivel_prioridade'))
                if nivel_prioridade_iluminacao  == nivel_prioridade_geladeira:
                    nivel_prioridade_geladeira = nivel_prioridade_geladeira+1
                    
                    if nivel_prioridade_geladeira == nivel_prioridade_motor:
                        nivel_prioridade_motor = nivel_prioridade_motor+1

                    if nivel_prioridade_geladeira>3:
                        nivel_prioridade_geladeira = nivel_prioridade_geladeira-2

                elif nivel_prioridade_iluminacao == nivel_prioridade_motor:
                    nivel_prioridade_motor = nivel_prioridade_motor+1
                    if nivel_prioridade_motor == nivel_prioridade_geladeira:
                        nivel_prioridade_geladeira = nivel_prioridade_geladeira+1

                    if nivel_prioridade_motor>3:
                        nivel_prioridade_motor = nivel_prioridade_motor-2


            if request.form.get('equipamento') == 'motor':
                nivel_prioridade_motor = int(request.form.get('nivel_prioridade'))
                if nivel_prioridade_motor  == nivel_prioridade_geladeira:
                    nivel_prioridade_geladeira = nivel_prioridade_geladeira+1

                    if nivel_prioridade_geladeira == nivel_prioridade_iluminacao:
                        nivel_prioridade_iluminacao = nivel_prioridade_iluminacao+1

                    if nivel_prioridade_geladeira>3:
                        nivel_prioridade_geladeira = nivel_prioridade_geladeira-2

                elif nivel_prioridade_motor == nivel_prioridade_iluminacao:
                    nivel_prioridade_iluminacao = nivel_prioridade_iluminacao+1
                    if nivel_prioridade_iluminacao == nivel_prioridade_geladeira:
                        nivel_prioridade_geladeira = nivel_prioridade_geladeira+1

                    if nivel_prioridade_iluminacao>3:
                        nivel_prioridade_iluminacao = nivel_prioridade_iluminacao-2

        if "aplica_potenciatotal" in request.form:
            potencia_total = int(request.form.get('text_potenciatotal'))
            df_potenciatotal['Potencia Total'] = [potencia_total]
            df_potenciatotal.to_excel('./base/PotenciaTotal.xlsx', index=False)

    potencia_total= list(df_potenciatotal['Potencia Total'])[0]

    #Salva planilha com as prioridades
    df_prioridade = pd.DataFrame()
    df_prioridade['Nível Prioridade'] = [nivel_prioridade_geladeira, nivel_prioridade_iluminacao, nivel_prioridade_motor]
    df_prioridade['Nome do Equipamento'] = ['Geladeira', 'Iluminação', 'Motor']
    df_prioridade['Comando_Ligar'] = ['1', '3', '2']
    df_prioridade['Comando_Desligar'] = ['A', 'C', 'B']
    df_prioridade['Nome do Equipamento'] = ['Geladeira', 'Iluminação', 'Motor']
    df_prioridade.sort_values(['Nível Prioridade'], ascending=True, inplace=True)
    df_prioridade.reset_index(inplace=True)
    df_prioridade.to_excel('./base/Prioridades.xlsx', index=False)
    
    return render_template('configuracao.html', prioridade=df_prioridade, horarios=df_horarios, pot_total= potencia_total)

if __name__ == "__main__":
    # liga_arduino
    # s1 = liga_arduino.s1
    # app.run(host="192.168.0.32", debug=False)
    
    app.run(debug=True)