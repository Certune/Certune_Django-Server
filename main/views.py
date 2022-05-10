from django.http import HttpResponse
from rest_framework.views import APIView


class getApi(APIView):
    def get(self, request):
        email = self.request.data.get("useremail")
        songname = self.request.data.get("songname")

        return HttpResponse(email + " 얍 " + songname)
