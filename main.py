import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pydub import AudioSegment


def parsing(email, song):
    user_name = email
    song_name = song

    # 서비스 계정의 비공개 키 파일이름
    cred = credentials.Certificate("/Users/pcy/Documents/EWHA/certune-73ce6-firebase-adminsdk-bmoay-8513b6e787.json")
    default_app = firebase_admin.initialize_app(cred)

    # firebase 설정 초기화 및 연결
    config = {
        "apiKey": "AIzaSyCfJ-uvXEAEXTUzro8O69v01a2EhWy-Y9Q",
        "authDomain": "certune-73ce6.firebaseapp.com",
        "databaseURL": "https://certune-73ce6-default-rtdb.firebaseio.com",
        "projectId": "certune-73ce6",
        "storageBucket": "certune-73ce6.appspot.com",
        "messagingSenderId": "738446921024",
        "appId": "1:738446921024:web:acc5c89be384476d6cbea5",
        "measurementId": "G-J44P7PS6G5"
    }
    firebase = pyrebase.initialize_app(config)

    # storage 레퍼런스 가져오기
    storage = firebase.storage()

    # storage에서 mp3 파일 다운받기
    file_name = song_name + ".mp3"

    # TODO : recorded_sound.wav 대신 사용자 노래 음성 파일 가져오기
    path_on_cloud = "User/" + user_name + "/songs/" + song_name + "/recorded_sound.wav"
    print(path_on_cloud)
    storage.child(path_on_cloud).download(user_name + "_" + file_name)

    # Song 컬렉션 내 문서 읽어오기
    db = firestore.client()
    users_ref = db.collection(u'Song')
    docs = users_ref.stream()

    # 각 소절별 start time, end time 가져오기
    for doc in docs:
        if doc.id == song_name:
            # 소절별 시작 시간, 끝나는 시간을 담을 startTime, endTime 리스트 생성 및 초기화
            start_time = []
            end_time = []

            sentence_list = doc.to_dict().get("sentence")

            # for i in range(len(sentence_list)):
            #     note_list = sentence_list[i]["notes"]
            #     for j in range(len(note_list)):
            #         start_time.append(note_list[j]["start_time"])
            #         end_time.append(note_list[j]["end_time"])
            for i in range(len(sentence_list)):
                start_time.append(sentence_list[i]["start_time"])
                end_time.append(sentence_list[i]["end_time"])

    # base_audio = AudioSegment.from_file(user_name + "_" + file_name)
    base_audio = AudioSegment.from_file(user_name + "_" + file_name)
    file_index = 0

    # 소절별 시작 시간과 끝나는 시간을 받아와 음원을 자르고 storage에 업로드
    for t1, t2 in zip(start_time, end_time):
        if t1 != '':
            file_name = str(file_index) + ".mp3"
            t1 = float(t1) * 1000
            t2 = float(t2) * 1000
            new_audio = base_audio[t1:t2]
            new_audio.export(file_name, format="mp3")
            file_index += 1

            path_on_cloud = "User/" + user_name + "/songs/" + song_name + "/" + file_name
            path_local = file_name
            storage.child(path_on_cloud).put(path_local)


def views():
    return None


parsing("nitronium007@gmail.com", "신호등")