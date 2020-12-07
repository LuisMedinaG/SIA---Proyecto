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
        for i in range(DaysInWeek):
            for j, g in enumerate(timeTable.grupos):
                if j == len_grp - 1:
                    break
                if i in g.dias:
                    cur_h_fin = g.getHoraFin()
                    sig_h_ini = timeTable.grupos[j + 1].h_inicio
                    if sig_h_ini <= cur_h_fin:
                        continue
                    gap = abs(sig_h_ini - cur_h_fin) // 100
                    factor += gap * (gap + 1) * (2 * gap + 1)
        return factor


class CriterioGruposEmpalmados(Criterio):
    def EvaluarCriterio(self, timeTable):
        return 0


class CriterioDiasLibres(Criterio):
    def EvaluarCriterio(self, timeTable):
        # return timetable.SelectMany(t => t.Events).Select(e => e.Day).Distinct().Count();
        # Cuenta de dias distintos
        return 0


class Materia:
    def __init__(self, clave, nombre="", MIN_VALUE=0, MAX_VALUE=0):
        self.clave = clave
        self.nombre = nombre
        self.grupos = []
        self.MIN_VALUE = MIN_VALUE
        self.MAX_VALUE = MAX_VALUE

    def appendGrupo(self, grupo):
        self.grupos.append(grupo)
        self.MAX_VALUE += 1

    def __repr__(self):
        return f"{self.clave}: {self.MAX_VALUE}"


class Grupo:
    def __init__(self, nrc, h_inicio, duracion, dias, profesor):
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
        return f"{self.nrc} | {self.h_inicio} | {self.dias}"


def main():
    criterios = []
    # criterios.append(CriterioDiasLibres(10))
    # criterios.append(CriterioGruposEmpalmados(20))
    criterios.append(CriterioHorasMuertas(10))
    # Posibles criterios: hora llegada, hora salida, puntaje maestro, etc.

    materias = []
    materiaAlgoritmia = Materia("i5884", "algoritmia")
    # timeSlot = TimeSlot(700, 155, 0)
    grupo = Grupo("42269", 700, 155, [0, 2], "garcia hernandez, martin")
    materiaAlgoritmia.appendGrupo(grupo)
    grupo = Grupo("59565", 900, 155, [1, 3], "espinoza valdez, aurora")
    materiaAlgoritmia.appendGrupo(grupo)
    grupo = Grupo("59829", 1700, 155, [1, 3], "GOMEZ ANAYA, DAVID ALEJANDRO")
    materiaAlgoritmia.appendGrupo(grupo)

    materias.append(materiaAlgoritmia)
    materiaAlgoritmia = Materia("i5884", "algoritmia")
    # timeSlot = TimeSlot(700, 155, 0)
    grupo = Grupo("42269", 1700, 155, [0, 2], "garcia hernandez, martin")
    materiaAlgoritmia.appendGrupo(grupo)
    grupo = Grupo("59565", 1500, 155, [1, 3], "espinoza valdez, aurora")
    materiaAlgoritmia.appendGrupo(grupo)

    materias.append(materiaAlgoritmia)
    materiaBaseDeDatos = Materia("i5890", "base de datos")
    grupo = Grupo("59601", 1100, 155, [0, 2], "GOMEZ VALDIVIA, JAIME ROBERTO")
    materiaBaseDeDatos.appendGrupo(grupo)
    grupo = Grupo("59565", 1100, 155, [1, 3], "URIBE NAVA, SERGIO JAVIER")
    materiaBaseDeDatos.appendGrupo(grupo)
    grupo = Grupo("59565", 700, 155, [0, 2], "URIBE NAVA, SERGIO JAVIER")
    materiaBaseDeDatos.appendGrupo(grupo)
    grupo = Grupo("59565", 700, 155, [4], "URIBE NAVA, SERGIO JAVIER")
    materiaBaseDeDatos.appendGrupo(grupo)
    grupo = Grupo("59565", 1500, 155, [1, 3], "URIBE NAVA, SERGIO JAVIER")
    
    materias.append(materiaBaseDeDatos)

    materiaBaseDeDatos = Materia("i5890", "base de datos")
    grupo = Grupo("59601", 1100, 155, [0, 2], "GOMEZ VALDIVIA, JAIME ROBERTO")
    materiaBaseDeDatos.appendGrupo(grupo)
    grupo = Grupo("59565", 1700, 155, [1, 3], "URIBE NAVA, SERGIO JAVIER")
    materiaBaseDeDatos.appendGrupo(grupo)
    grupo = Grupo("59565", 1300, 155, [0, 2], "URIBE NAVA, SERGIO JAVIER")
    materiaBaseDeDatos.appendGrupo(grupo)
    grupo = Grupo("59565", 1500, 155, [1, 3], "URIBE NAVA, SERGIO JAVIER")

    materias.append(materiaBaseDeDatos)

    cant_individuos = 100
    generaciones = 300
    fact_mut = 0.5
    alelos = len(materias)

    ag = agc.AGC(cant_individuos, alelos, generaciones, fact_mut, materias,
                 criterios, False)
    ag.run()
    print(ag._individuos)


if __name__ == '__main__':
    main()
