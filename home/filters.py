from dj_rql.filter_cls import AutoRQLFilterClass
from home.models import Aluno, Turma, Matricula, Notas, Instituicao, Professor, Habilitacao, Disciplina, Historico


class AlunoFilterClass(AutoRQLFilterClass):
    MODEL = Aluno


class TurmaFilterClass(AutoRQLFilterClass):
    MODEL = Turma


class MatriculaFilterClass(AutoRQLFilterClass):
    MODEL = Matricula


class NotasFilterClass(AutoRQLFilterClass):
    MODEL = Notas


class InstituicaoFilterClass(AutoRQLFilterClass):
    MODEL = Instituicao


class ProfessorFilterClass(AutoRQLFilterClass):
    MODEL = Professor


class HabilitacaoFilterClass(AutoRQLFilterClass):
    MODEL = Habilitacao


class DisciplinaFilterClass(AutoRQLFilterClass):
    MODEL = Disciplina


class HistoricoFilterClass(AutoRQLFilterClass):
    MODEL = Historico
