import matplotlib.pyplot as plt
import numpy as np
import json
import agc


def plotFunction(function, function_name="", cant_individuos=100,
                 dimensiones=(2, 4, 8), generaciones=2000, fact_mut=0.5, avg_dim=5):
    genera_lista = np.arange(0, generaciones + 100, 100)

    for dimension in dimensiones:
        for i in range(avg_dim):
            algo = agc.AGC(function, cant_individuos, dimension, generaciones,
                          fact_mut)
            algo.run()

            if i == 0:
                promedio_mejor = algo._mejores_historico
            else:
                promedio_mejor = [
                    (g + h) / 2
                    for g, h in zip(algo._mejores_historico, promedio_mejor)
                ]

        # Promedio 5 ejecuciones de dimension actual
        filename_prefix = f'{function_name}_dim_{dimension}'
        saveData(filename_prefix, promedio_mejor)
        promedio_mejor = np.array(promedio_mejor)
        # plotData(genera_lista, promedio_mejor, filename_prefix)

    plt.figure()
    for dimension in dimensiones:
        filename_prefix = f'{function_name}_dim_{dimension}'
        promedio_mejor = readData(filename_prefix)
        promedio_mejor = np.array(promedio_mejor)
        plt.plot(genera_lista, promedio_mejor)
    plt.savefig(f'{function_name}_all.png')


def plotData(data_x, data_y, filename):
    plt.figure()
    plt.plot(data_x, data_y)
    plt.savefig(filename + '.png')


def readData(filename):
    data = {}
    with open(filename + '.json', 'r') as fp:
        data = json.load(fp)
    return data


def saveData(filename, data):
    with open(filename + '.json', 'w') as fp:
        json.dump(data, fp)
