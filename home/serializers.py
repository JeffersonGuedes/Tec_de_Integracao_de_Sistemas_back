from rest_framework import serializers
from home.models import  Aluno, Turma, Matricula, Notas, Instituicao, Professor, Habilitacao, Disciplina, Historico, CustomUser
# from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from captcha.serializers import CaptchaModelSerializer
from django.contrib.auth.models import User


class AlunoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'


class TurmaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'


class MatriculaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = '__all__'


class NotasModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notas
        fields = '__all__'


class InstituicaoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituicao
        fields = '__all__'


class ProfessorModelSerializer(serializers.ModelSerializer):
    instituicao = serializers.PrimaryKeyRelatedField(
        queryset=Instituicao.objects.all(),
        write_only=False
    )
    instituicao_nome = serializers.CharField(
        source='instituicao.nome',
        read_only=True
    )

    class Meta:
        model = Professor
        fields = '__all__'
        extra_kwargs = {
            'instituicao': {'required': True}
        }


class HabilitacaoModelSerializer(serializers.ModelSerializer):
    professor = serializers.CharField(source='professor.nome')
    especializacao = serializers.CharField(source='professor.especializacao')
    disciplina = serializers.CharField(source='disciplina.nome')

    class Meta:
        model = Habilitacao
        fields = '__all__'


class DisciplinaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'


class HistoricoModelSerializer(serializers.ModelSerializer):
    professor = serializers.CharField(source='professor.nome')
    especializacao = serializers.CharField(source='professor.especializacao')
    disciplina = serializers.CharField(source='disciplina.nome')

    class Meta:
        model = Historico
        fields = '__all__'
        

class CaptchaSerializer(serializers.Serializer):
    captcha_key = serializers.CharField()
    captcha_image = serializers.SerializerMethodField()

    def get_captcha_image(self, obj):
        return captcha_image_url(obj['captcha_key'])


class CheckCaptchaModelSerializer(CaptchaModelSerializer):
    sender = serializers.EmailField()

    class Meta:
        model = User
        fields = ("captcha_code", "captcha_hashkey", "sender")


class CPFSerializer(serializers.Serializer):
    cpf = serializers.CharField(max_length=14)


class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField(max_length=14)
    password = serializers.CharField(max_length=128)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return data

    def validateRepet(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("Senha não pode ser igual.")
        return data
