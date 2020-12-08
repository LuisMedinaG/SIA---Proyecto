import agc


class Criterio:
    def __init__(self, penalty):
        self._penalty = penalty

    def getPenalty(self):
        return self._penalty


class CriterioHorasMuertas(Criterio):
    def EvaluarCriterio(self, timeTable, HoursOfDay=14, DaysInWeek=6):
        factor = 0
        len_grp = len(timeTable.grupos)
        for i in range(DaysInWeek - 1):
            for j, g in enumerate(timeTable.grupos):
                if j == len_grp - 1:
                    break
                if i in g.dias:
                    cur_h_fin = g.getHoraFin()
                    sig_h_ini = timeTable.grupos[j + 1].h_inicio
                    if sig_h_ini <= cur_h_fin:
                        continue
                    gap = (sig_h_ini - cur_h_fin) // 100
                    factor += sumOfSquares(gap)
        return factor


class CriterioGruposEmpalmados(Criterio):
    def EvaluarCriterio(self, timeTable, HoursOfDay=14, DaysInWeek=6):
        factor = 0
        len_grp = len(timeTable.grupos)
        for i in range(DaysInWeek - 1):
            for j, g in enumerate(timeTable.grupos):
                if j == len_grp - 1:
                    break
                if i in g.dias:
                    cur_h_fin = g.getHoraFin()
                    sig_h_ini = timeTable.grupos[j + 1].h_inicio
                    if sig_h_ini >= cur_h_fin:
                        continue
                    gap = abs(sig_h_ini - cur_h_fin) // 100
                    factor += sumOfSquares(gap)
        return factor


class CriterioDiasLibres(Criterio):
    def __init__(self, penalty, min_dias_libres):
        super().__init__(penalty)
        self._min_dias_libres = min_dias_libres

    def EvaluarCriterio(self, timeTable, DaysInWeek=6):
        dias_distintos = set()
        for g in timeTable.grupos:
            for d in g.dias:
                dias_distintos.add(d)
        dias_ocupados = len(dias_distintos)
        dias_libres_reales = DaysInWeek - dias_ocupados
        diff_dias_libres = self._min_dias_libres - dias_libres_reales
        if diff_dias_libres <= 0:
            return 0
        return sumOfSquares(diff_dias_libres)


class Materia:
    def __init__(self, id_, clave, nombre="", MIN_VALUE=0, MAX_VALUE=0):
        self.id_ = id_
        self.clave = clave
        self.nombre = nombre
        self.grupos = []
        self.MIN_VALUE = MIN_VALUE
        self.MAX_VALUE = MAX_VALUE

    def addGrupo(self, grupo):
        self.grupos.append(grupo)
        self.MAX_VALUE += 1

    def __repr__(self):
        return f"{self.clave}: {self.MAX_VALUE}"


class Grupo:
    def __init__(self, id_materia, nrc, h_inicio, duracion, dias, profesor):
        self.id_materia = id_materia
        self.nrc = nrc
        self.h_inicio = h_inicio
        self.duracion = duracion
        self.dias = dias
        self.profesor = profesor

    def getHoraFin(self):
        return self.h_inicio + self.duracion

    def __eq__(self, other):
        return self.nrc == other.nrc

    def __lt__(self, other):
        return self.h_inicio < other.h_inicio

    def __repr__(self):
        return f"{self.id_materia} {self.nrc} | {self.h_inicio} - {self.getHoraFin()} | {self.dias}\n"

def sumOfSquares(num):
    return num * (num + 1) * (2 * num + 1)

def main():
    criterios = []
    min_dias_libres = 4
    criterios.append(CriterioDiasLibres(15, min_dias_libres))
    criterios.append(CriterioGruposEmpalmados(20))
    criterios.append(CriterioHorasMuertas(10))
    # Posibles criterios: hora llegada, hora salida, puntaje maestro, etc.

    id_mater = 0
    materias = []
    materia = Materia(id_mater, "i5884", "algoritmia")
    materia.addGrupo(
        Grupo(id_mater, "a0", 700, 355, [0, 2], "garcia merin, martin"))
    materia.addGrupo(Grupo(id_mater, "a1", 700, 355, [4], "garcia merin, martin"))
    materias.append(materia)
    id_mater += 1

    materia = Materia(id_mater, "i5885", "seminario algoritmia")
    materia.addGrupo(Grupo(id_mater, "sa5", 700, 355, [0, 2], "garcia lora, martin"))
    materia.addGrupo(Grupo(id_mater, "sa5", 900, 155, [0, 2], "garcia lora, martin"))
    materia.addGrupo(Grupo(id_mater, "sa0", 1100, 155, [0, 2], "garcia lora, martin"))
    # materia.addGrupo(Grupo(id_mater, "sa0", 700, 155, [1, 3], "garcia lora, martin"))
    # materia.addGrupo(
    #     Grupo(id_mater, "sa1", 1100, 155, [1, 3], "garcia lora, martin"))
    # materia.addGrupo(
    #     Grupo(id_mater, "sa2", 1300, 155, [1, 3], "garcia lora, martin"))
    # materia.addGrupo(
    #     Grupo(id_mater, "sa3", 1500, 155, [1, 3], "garcia lora, martin"))
    # materia.addGrupo(
    #     Grupo(id_mater, "sa4", 1700, 155, [1, 3], "garcia lora, martin"))
    
    materias.append(materia)
    id_mater += 1

    # timeSlot = TimeSlot(700, 155, 0)
    materia = Materia(id_mater, "i5884", "programacion")
    materia.addGrupo(Grupo(id_mater, "p0", 900, 155, [0, 2], "cera valdez, lia"))
    materia.addGrupo(Grupo(id_mater, "p1", 1300, 155, [0, 2], "garcia meli, juan"))
    materia.addGrupo(Grupo(id_mater, "p2", 1300, 55, [0, 2], "garcia meli, juan"))
    materia.addGrupo(Grupo(id_mater, "p3", 700, 355, [4], "garcia meli, juan"))
    materias.append(materia)
    id_mater += 1

    cant_individuos = 10
    generaciones = 100
    fact_mut = 0.5
    alelos = len(materias)

    ag = agc.AGC(cant_individuos, alelos, generaciones, fact_mut, materias,
                 criterios, False)
    ag.run()


if __name__ == '__main__':
    main()
