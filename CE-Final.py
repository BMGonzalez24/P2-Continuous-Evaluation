__author__ = 'Bruno Gonzalez, 56941.'

import matplotlib.pyplot as grafico
import csv

def limpa_converte (dados, lista_colunas, pred_filtragem, funs_converter):
    dadosInteressantes = filter(pred_filtragem, dados)
    for i in lista_colunas:
        dadosInteressantes = filter(lambda x: len(x[i]) != 0, dadosInteressantes)
    dadosBonitos = [  ]
    for i in list(dadosInteressantes):
        valores = {  }
        for coluna, funcao in zip(columns, fun_conv):
            valor = {coluna: funcao(i[coluna])}
            valores.update(valor)
        dadosBonitos.append(valores)
    return dadosBonitos

def media_movel (yy, janela):
    final = []
    for index in range(0, len(yy)):
        soma = []
        soma.append(yy[index])
        while len(soma)-1 < index:
            soma.append(yy[index-len(soma)])
            if len(soma) == janela:
                break
        final.append(sum(soma)/len(soma))
    return final

def desvio_padrao (yy, janela):
    final = []
    media = media_movel(yy,janela)
    for index in range(0, len(yy)):
        soma = []
        soma.append( ( yy[index] - media[index] ) **2)
        while len(soma)-1 < index:
            soma.append( ( yy[index-len(soma)] - media[index] ) **2)
            if len(soma) == janela:
                break
        final.append( (sum(soma)/len(soma) )**(1/2) )
    return final

def tracar (abcissas, ordenadas, parametros, janela=30):   
    betweenSuperior = (list(map(lambda u, o: u+2*o, media_movel(ordenadas,janela), desvio_padrao(ordenadas,janela))))
    betweenInferior = (list(map(lambda u, o: u-2*o, media_movel(ordenadas,janela), desvio_padrao(ordenadas,janela))))

    grafico.title(parametros['Titulo'])
    grafico.ylabel(parametros['LadoY'])
    grafico.xlabel(parametros['LadoX'])

    grafico.plot(abcissas, ordenadas, linestyle="", marker='.', color='Green')
    grafico.plot(media_movel(abcissas,janela), media_movel(ordenadas,janela), color=parametros['Cor'])
    
    grafico.fill_between(abcissas, betweenSuperior, betweenInferior, alpha=0.2, color=parametros['Cor'])
    print(grafico.show())

def sakura (ficheiro_csv):
    anos = []
    dias = []
    with open(ficheiro_csv, 'r') as ficheiro:
        leitor = csv.reader(ficheiro, delimiter=';')
        for i in leitor :
            if i[1] != '' and i[0].isnumeric() == True:
                anos.append(int(i[0]))
                dias.append(int(i[1]))
    costumizacao = {
        'Titulo': 'Registo Histórico da Data de Florescimento das Cerejeiras em Quioto',
        'LadoX' : 'Ano DC',
        'LadoY' : 'Dias após inicio do ano',
        'Cor'   : '#ff00ff'
    }
    tracar(anos, dias, costumizacao)

def conv_minutos(coluna):
    filtrado = []
    minutos  = []
    for i in coluna:
        filtrado.append(i[8:10]+i[11:13]+i[14:16])

    for y in filtrado:
        minutos.append(int(y[5:7]) + (int(y[3:5])*60) + (int(y[0:2])*1440))
    return minutos

def organizar(mins,magn):
    dicionario = {}
    for index in range(len(mins)):
        if mins[index] in dicionario:
            dicionario[mins[index]].append(float(magn[index]))
        else:
            dicionario[mins[index]] = [float(magn[index])]
    mins = []
    magn = []
    for i,j in dicionario.items():
        mins.append(i)
    mins.sort()
    for i in mins:
        magn.append(sum(dicionario[i])/len(dicionario[i]))
    return mins, magn

def sismos (ficheiro_csv):
    data = []
    magn = []
    with open(ficheiro_csv, 'r', encoding="utf8") as ficheiro:
        leitor = csv.reader(ficheiro, delimiter=',')
        for i in leitor:
            if i[4] != '':
                data.append(i[0])
                magn.append(i[4])
    mins = conv_minutos(data[1:])

    costumizacao = {
        'Titulo': 'Sismos',
        'LadoX' : 'Minutos desde o início do mês',
        'LadoY' : 'Média das magnitudes',
        'Cor'   : '#ff00ff'
    }
    final = organizar(mins, magn[1:])
    tracar(final[0], final[1], costumizacao)