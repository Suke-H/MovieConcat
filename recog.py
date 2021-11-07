import speech_recognition as sr
import pandas as pd
import subprocess
import os
 
# # 文字起こし対象のファイル
# text_video_path = "C:/Users/suke0/Desktop/その他/Maverix/movie_concat/movie/657978544.062511.mp4"
 
# # テキスト用音声データの出力先
# audio_text_path = "C:/Users/suke0/Desktop/その他/Maverix/movie_concat/audio_text.mp3"
# audio_change_wav = "C:/Users/suke0/Desktop/その他/Maverix/movie_concat/audio_text.wav"
 
# # テキスト保存場所
# text_date = "C:/Users/suke0/Desktop/その他/Maverix/movie_concat/text.txt"
# # csv保存場所
# csv_date = "C:/Users/suke0/Desktop/その他/Maverix/movie_concat/text.csv"

# 文字起こし対象のファイル
text_video_path = "movie/657978544.062511.mp4"
 
# テキスト用音声データの出力先
audio_text_path = "audio/audio_text.mp3"
audio_change_wav = "audio/audio_text.wav"
 
# テキスト保存場所
text_date = "txt/text.txt"
# csv保存場所
csv_date = "csv/text.csv"
 
# mp4→mp3へ変換
def out_text(text_video_path, audio_text_path):
    out_audio = subprocess.run(
        [
            "ffmpeg",
            "-i",
            text_video_path,
            "-acodec",
            "libmp3lame",
            "-ab",
            "256k",
            audio_text_path,
        ]
    )
    print(out_audio)
 
# mp3からwavに変換
def audio_transcript(audio_change_wav):
    transcript = subprocess.run(
        [
            "ffmpeg",
            "-i",
            audio_text_path,
            "-vn",
            "-ac",
            "1",
            "-ar",
            "44100",
            "-acodec",
            "pcm_s16le",
            "-f",
            "wav",
            audio_change_wav,
        ]
    )
    print(transcript)
 
 
def audio_text_change(audio_change_wav, text_date, csv_date):
    # 文字起こし
    r = sr.Recognizer()
    with sr.AudioFile(audio_change_wav) as source:
        audio = r.record(source)
        text = r.recognize_google(audio, language="ja-JP").replace(" ", "\n")
        print(text)
    # textへの書き出し
    open_text = open(text_date, "x", encoding="utf_8")
    open_text.write(text)
    open_text.close()
    # txtをcsvに変換
    read_text = pd.read_csv(text_date)
    read_text.to_csv(csv_date, index=None)
 
 
out_text(text_video_path, audio_text_path)
 
# mp3が生成するまでにタイムラグがあるので、生成されるのを待つ処理
while os.path.isfile(audio_text_path):
    audio_transcript(audio_change_wav)
    print("change end")
    if os.path.isfile(audio_change_wav):
        print("break!!")
        break
 
audio_text_change(audio_change_wav, text_date, csv_date)