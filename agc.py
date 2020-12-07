import copy
import numpy as np
import heapq

class TimeTable:
    def __init__(self, grupos):
        self.grupos = grupos

    def fitness(self, criterios):
        f = 0
        for criterio in criterios:
            f += criterio.getPenalty() * criterio.EvaluarCriterio(self)
        return f

    def __repr__(self):
        return f"{self.grupos}"

    def printTable(self):
        for i in range(6):
            print(f"DIA | {i}")
            for g in self.grupos:
                if i in g.dias and g:
                    print(f"    | {g.h_inicio:04d} - {g.getHoraFin():04d}")
            print('-'*10)


class Individuo:
    def __init__(self, alelos, cromosoma):
        self._alelos = alelos
        self._cromosoma = cromosoma
        self._fitness = 0

    def __lt__(self, other):
        return self._fitness < other._fitness

    def __repr__(self):
        return f"{self._cromosoma} = {self._fitness}, "

class AGC:
    def __init__(self,
                 cantidad_individuos,
                 alelos,
                 generaciones,
                 p,
                 materias,
                 criterios,
                 maxim=True):
        self._cantidad_individuos = cantidad_individuos
        self._alelos = alelos
        self._generaciones = generaciones
        self._p = p
        self._maxim = maxim
        self._individuos = np.array([])

        self._materias = materias
        self._criterios = criterios

    def run(self):
        self.crearIndividuos()
        self._mejor_historico = self._individuos[0]

        generacion = 1
        while generacion <= self._generaciones:
            self.evaluaIndividuos()
            return
            self.mejor()
            hijos = np.array([])
            while len(hijos) < len(self._individuos):
                padre1 = self.ruleta()
                padre2 = self.ruleta()
                while padre1 == padre2:
                    padre2 = self.ruleta()
                h1, h2 = self.cruza(self._individuos[padre1],
                                    self._individuos[padre2])
                hijos = np.append(hijos, [h1])
                hijos = np.append(hijos, [h2])
            self.mutacion(hijos)
            self._individuos = np.copy(hijos)
            if generacion % 100 == 0:
                print(f"Generación: {generacion} Mejor Histórico: "
                      f"{self._mejor_historico._cromosoma} "
                      f"{self._mejor_historico._fitness :.10f}")
                print(self.makeHorarioFromCromosoma(self._mejor_historico._cromosoma))

            generacion += 1

    def crearIndividuos(self):
        for i in range(self._cantidad_individuos):
            valores = []
            for materia in self._materias:
                r_idx = np.random.randint(materia.MIN_VALUE, materia.MAX_VALUE)
                valores.append(r_idx)
            cromosoma = np.array(valores)
            individuo = Individuo(self._alelos, cromosoma)
            self._individuos = np.append(self._individuos, [individuo])

    def makeHorarioFromCromosoma(self, cromosoma):
        grupos = []
        for i, alelo in enumerate(cromosoma):
            materia = self._materias[i]
            grupo = materia.grupos[alelo]
            heapq.heappush(grupos, grupo)
        return TimeTable(grupos)

    def evaluaIndividuos(self):
        for i in self._individuos:
            horario = self.makeHorarioFromCromosoma(i._cromosoma)
            i._fitness = horario.fitness(self._criterios)
            if not self._maxim:
                i._fitness *= -1

    def ruleta(self):
        f_sum = np.sum([i._fitness for i in self._individuos])
        r = np.random.randint(np.abs(f_sum + 1), dtype=np.int64)
        if f_sum < 0:
            r *= -1
        k = 0
        F = self._individuos[k]._fitness
        if f_sum < 0:
            while F > r and k < len(self._individuos) - 1:
                k += 1
                F += self._individuos[k]._fitness
        else:
            while F < r and k < len(self._individuos) - 1:
                k += 1
                F += self._individuos[k]._fitness
        return k

    def cruza(self, i1, i2):
        h1 = copy.deepcopy(i1)
        h2 = copy.deepcopy(i2)

        s = self._alelos - 1
        punto_cruza = np.random.randint(s) + 1
        h1._cromosoma[punto_cruza:], h2._cromosoma[
            punto_cruza:] = h2._cromosoma[punto_cruza:], h1._cromosoma[
                punto_cruza:]
        return h1, h2

    def mutacion(self, hijos):
        for h in hijos:
            for a in range(len(h._cromosoma)):
                if np.random.rand() < self._p:
                    h._cromosoma[a] = np.random.randint(
                        self._materias[a].MIN_VALUE,
                        self._materias[a].MAX_VALUE)

    def mejor(self):
        for i in self._individuos:
            if i._fitness > self._mejor_historico._fitness:
                self._mejor_historico = copy.deepcopy(i)
