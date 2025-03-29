from django.contrib import admin
from .models import CustomUser, ModelAuditSettings, Notas, Matricula, Turma, Aluno, Instituicao, Professor, Habilitacao, Disciplina, Historico

admin.site.register(CustomUser)
admin.site.register(ModelAuditSettings)
admin.site.register(Notas)
admin.site.register(Matricula)
admin.site.register(Turma)
admin.site.register(Aluno)
admin.site.register(Instituicao)
admin.site.register(Professor)
admin.site.register(Habilitacao)
admin.site.register(Disciplina)
admin.site.register(Historico)
