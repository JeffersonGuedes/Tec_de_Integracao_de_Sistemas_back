import json
import pika
from rest_framework import status, views, response
from core.tasks import generate_certificate, send_notification


class CertificateView(views.APIView):

    def post(self, request):
        data = request.data

        generate_certificate.delay(data)
        send_notification.delay(data)

        return response.Response(
            data={
                'status': 'ok',
                'message': 'Certificado gerado e enviado',
                'data': data
            },
            status=status.HTTP_201_CREATED
        )
