from django.urls import path, include
from rest_framework.routers import DefaultRouter
from home.views import CaptchaView, ValidateCaptchaView, AuthResetView, AuthLoginView, ChangePasswordView, AlunoModelViewSet, TurmaModelViewSet, MatriculaModelViewSet, NotasModelViewSet, InstituicaoModelViewSet, ProfessorModelViewSet, HabilitacaoModelViewSet, DisciplinaModelViewSet, HistoricoModelViewSet


router = DefaultRouter()
router.register("alunos", AlunoModelViewSet)
router.register("turmas", TurmaModelViewSet)
router.register("matriculas", MatriculaModelViewSet)
router.register("notas", NotasModelViewSet)
router.register("instituicao", InstituicaoModelViewSet)
router.register("professores", ProfessorModelViewSet)
router.register("habilitacoes", HabilitacaoModelViewSet)
router.register("disciplinas", DisciplinaModelViewSet)
router.register("historicos", HistoricoModelViewSet)


urlpatterns = [
    path("", include(router.urls)),

    path('api/captcha/', CaptchaView.as_view(), name='captcha'),
    path('api/validate-captcha/', ValidateCaptchaView.as_view(), name='validate-captcha'),
    path('auth_reset/', AuthResetView.as_view(), name="auth_reset"),
    path('auth_login/', AuthLoginView.as_view(), name="auth_login"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
]
