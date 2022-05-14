from django.http import HttpResponse
from rest_framework.utils import json
from rest_framework.views import APIView
from main import parsing


class getApi(APIView):
    def get(self, request):
        result = json.loads(request.body.decode('utf8'))
        email = result.get('useremail')
        songname = result.get('songname')

        # TODO : parsing 함수 호출 -> 해당 함수에서 롤직 처리하고 firebase 업롤드까지 확인!
        parsing(email, songname)
        return HttpResponse(email + " " + songname)
