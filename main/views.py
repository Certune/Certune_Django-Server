from django.shortcuts import render, redirect
from django.shortcuts import render
from .form import FileUploadForm
from .models import fileUpload
from firebase_admin import credentials
from firebase_admin import storage
from uuid import uuid4
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib import messages
import pyrebase
import os
from pydub import AudioSegment

config = {
    "apiKey": "AIzaSyCfJ-uvXEAEXTUzro8O69v01a2EhWy-Y9Q",
  "authDomain": "certune-73ce6.firebaseapp.com",
  "databaseURL": "https://certune-73ce6-default-rtdb.firebaseio.com",
  "projectId": "certune-73ce6",
  "storageBucket": "certune-73ce6.appspot.com",
  "messagingSenderId": "738446921024",
  "appId": "1:738446921024:web:acc5c89be384476d6cbea5",
  "measurementId": "G-J44P7PS6G5",
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


#파일 업로드
def main(request):
    if request.method == 'POST':
        name = request.file['name']
        file = request.FILES['audioFile']
        fileupload = fileUpload(
           name=name,
            audioFile=file,
        )
        fileupload.save()
        return redirect('main')
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'main.html', context)


    #     file_save = default_storage.save(file.name, file)
    #     storage.child("songs/"+file.name).put(file.name)
    #     # delete = default_storage.delete(file.name)
    #     # messages.success(request, "File upload in Firebase Storage successful")
    #     print("upload success!")
    #     return redirect('main')
    # else:
    #     return render(request, 'main.html')


def fileUpload(file):
    blob = storage.put('songs/'+file)
    #new token and metadata 설정
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token} #access token이 필요.
    blob.metadata = metadata

    #upload file
    blob.upload_from_filename(filename='./songs'+file, content_type='wav')
    print(blob.public_url)

def execute():
    baseAudio = AudioSegment.from_file("C:/Users/mok33/PycharmProjects/pitchdetection/신호등_이무진.wav")

    t1 = 21.63691 * 1000
    t2 = 26.89413 * 1000

    newAudio = baseAudio[t1:t2]
    newAudio.export("1.wav", format="wav")

    fileUpload("1.wav")

execute()