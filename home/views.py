from dj_rql.drf import RQLFilterBackend
from home.filters import AlunoFilterClass, TurmaFilterClass, MatriculaFilterClass, NotasFilterClass, InstituicaoFilterClass, ProfessorFilterClass, HabilitacaoFilterClass, DisciplinaFilterClass, HistoricoFilterClass
from home.models import CustomUser, Aluno, Turma, Matricula, Notas, Instituicao, Professor, Habilitacao, Disciplina, Historico
from home.serializers import CPFSerializer, LoginSerializer, ChangePasswordSerializer, CaptchaSerializer, AlunoModelSerializer, TurmaModelSerializer, MatriculaModelSerializer, NotasModelSerializer, InstituicaoModelSerializer, ProfessorModelSerializer, HabilitacaoModelSerializer, DisciplinaModelSerializer, HistoricoModelSerializer
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions, status, views, response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.db import transaction
from django.utils.crypto import get_random_string
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.hashers import check_password
# from rest_framework_simplejwt.views import TokenObtainPairView
# from django.contrib.auth.hashers import make_password
# from django.core.exceptions import ObjectDoesNotExist
# from django.core.cache import cache


class AlunoModelViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoModelSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = AlunoFilterClass
    permission_classes = [permissions.AllowAny]


class TurmaModelViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaModelSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = TurmaFilterClass
    permission_classes = [permissions.AllowAny]


class MatriculaModelViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaModelSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = MatriculaFilterClass
    permission_classes = [permissions.AllowAny]


class NotasModelViewSet(viewsets.ModelViewSet):
    queryset = Notas.objects.all()
    serializer_class = NotasModelSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = NotasFilterClass
    permission_classes = [permissions.AllowAny]


class InstituicaoModelViewSet(viewsets.ModelViewSet):
    queryset = Instituicao.objects.all()
    serializer_class = InstituicaoModelSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = InstituicaoFilterClass
    permission_classes = [permissions.AllowAny]


class ProfessorModelViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorModelSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = ProfessorFilterClass
    permission_classes = [permissions.AllowAny]


class HabilitacaoModelViewSet(viewsets.ModelViewSet):
    queryset = Habilitacao.objects.all()
    serializer_class = HabilitacaoModelSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = HabilitacaoFilterClass
    permission_classes = [permissions.AllowAny]


class DisciplinaModelViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaModelSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = DisciplinaFilterClass
    permission_classes = [permissions.AllowAny]


class HistoricoModelViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoModelSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = HistoricoFilterClass
    permission_classes = [permissions.AllowAny]


class CaptchaView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        CaptchaStore.remove_expired()

        captcha_key = CaptchaStore.generate_key()
        captcha_image_url1 = captcha_image_url(captcha_key)

        data = {
            'captcha_key': captcha_key,
            'captcha_image': captcha_image_url1,
        }

        serializer = CaptchaSerializer(data)
        return Response(serializer.data)


class ValidateCaptchaView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        captcha_key = request.data.get('captcha_key')
        captcha_value = request.data.get('captcha_value')

        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
            if captcha.response == captcha_value.lower():
                captcha.delete()
                return Response({'message': 'Captcha válido'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Captcha inválido'}, status=status.HTTP_400_BAD_REQUEST)
        except CaptchaStore.DoesNotExist:
            return Response({'message': 'Captcha inválido'}, status=status.HTTP_400_BAD_REQUEST)


class AuthResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CPFSerializer(data=request.data)
        if serializer.is_valid():
            cpf = serializer.validated_data['cpf']
            try:
                with transaction.atomic():
                    usuario = CustomUser.objects.get(cpf=cpf)
                    senha_temporaria = get_random_string(8)
                    usuario.set_password(senha_temporaria)
                    usuario.is_temporary_password = True
                    usuario.save()

                    send_mail(
                        "Redefinição de Senha",
                        f"Use a seguinte senha temporária para acessar: {senha_temporaria}.",
                        'jeffersonguedes@edu.unifor.br',
                        [usuario.email],
                        fail_silently=False,
                    )

                    return Response(
                        {"message": "Um e-mail com a senha temporária foi enviado."},
                        status=status.HTTP_200_OK
                    )
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "CPF não encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            cpf = serializer.validated_data['cpf']
            password = serializer.validated_data['password']
            user = CustomUser.objects.get(cpf=cpf)

            if check_password(password, user.password):
                if user.is_temporary_password:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {"message": "Login bem-sucedido. Redirecionando para alteração de senha.",
                         "auth_login": "auth_register",
                         "access": str(refresh.access_token),
                         "refresh": str(refresh),
                         },
                        status=status.HTTP_200_OK,
                    )
                else:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {"message": "Login bem-sucedido. Redirecionando para a página inicial.",
                         "auth_login": "access",
                         "access": str(refresh.access_token),
                         "refresh": str(refresh),
                         },
                        status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    {"error": "CPF ou senha incorretos."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user

            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"error": "A senha atual está incorreta."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(serializer.validated_data['new_password'])
            user.is_temporary_password = False
            user.save()

            update_session_auth_hash(request, user)

            return Response(
                {"message": "Senha alterada com sucesso."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, )
