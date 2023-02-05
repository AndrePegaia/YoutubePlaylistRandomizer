import PySimpleGUI as sg
from pygame import mixer
import os
import yt_dlp

def unpauseOnButton(start_time, pauseTimeStart, window, botaoPauseImagem):
    import time
    paused = False
    window["BotaoPausePlay"].update(image_data=botaoPauseImagem)
    pauseTimeEnd = int(round(time.time() * 100)) - start_time
    start_time += pauseTimeEnd - pauseTimeStart
    return paused, pauseTimeEnd, start_time


def botaoVolume(window, changeVolume):
    if changeVolume == False:
        window["-avisos-"].update(visible=False)
        window["-volumeTitulo-"].update(visible=True)
        window["-volumeSlider-"].update(visible=True)
        window["-col3-"].update(visible=True)
        changeVolume = True
    else:
        window["-avisos-"].update(visible=False)
        window["-volumeTitulo-"].update(visible=False)
        window["-volumeSlider-"].update(visible=False)
        window["-col3-"].update(visible=False)
        changeVolume = False
    return changeVolume

def botaoDownloadMusica(window, titulo):
    import shutil
    import os

    try:
        for file in os.listdir("temp/Audio/Audio-MP3s"):
            if file.endswith(".mp3"):
                src = f"temp/Audio/Audio-MP3s/{file}"
                dst = "Downloads/MP3"
                shutil.copy(src, dst)
                tituloSemCaracteresEspeciais = ''.join(filter(str.isalpha, titulo))
                if tituloSemCaracteresEspeciais == "":
                    tituloSemCaracteresEspeciais = "TituloDesconhecido"
                os.rename(f"{dst}/{file}", f"{dst}/{tituloSemCaracteresEspeciais}.mp3")
        window["-avisos-"].update(visible=True)
        window["-avisos-"].update("Download realizado com sucesso!!!")
        window["-volumeTitulo-"].update(visible=False)
        window["-volumeSlider-"].update(visible=False)
        window["-col3-"].update(visible=True)

    except:
        window["-avisos-"].update(visible=True)
        window["-avisos-"].update("Erro no download")
        window["-volumeTitulo-"].update(visible=False)
        window["-volumeSlider-"].update(visible=False)
        window["-col3-"].update(visible=True)


def botoesVideos(videoAtual, Index, botao):
    changeVolume = False
    if botao == "BotaoSkipEsquerda":
        if videoAtual <= -len(Index):
            videoAtual = 0
        else:
            videoAtual -= 1

    elif botao == "BotaoSkipDireita" or botao == "-Slider-":
        if videoAtual >= len(Index):
            videoAtual = 0
        else:
            videoAtual += 1

    return videoAtual, changeVolume


def carregarProximaMusica(window, videoAtual, videosGlobal, Index, botao):
        mixer.music.stop()
        toogleInterfaceMusica(False, window)
        starting = audioAtualizarVideo(videoAtual, videosGlobal, Index, window, botao)

        return starting


def tempoExibicao(time):
    if int(time % 60) < 10:
        timeReturn = f"{int(time // 60)}:0{int(time % 60)}"
    else:
        timeReturn = f"{int(time // 60)}:{int(time % 60)}"
    return timeReturn


def convertToBase64(src):
    import base64
    binary_fc = open(src, 'rb').read()  # fc aka file_content
    base64_utf8_str = base64.b64encode(binary_fc).decode('utf-8')

    ext = src.split('.')[-1]
    dataurl = f'data:image/{ext};base64,{base64_utf8_str}'
    return base64_utf8_str


def toogleInterfaceMusica(bool, window):
    window["-col1-"].update(visible=bool)
    window["-col2-"].update(visible=not bool)
    window["-col3-"].update(visible=False)
    window["-col4-"].update(visible=bool)


def deletarTempsFinalizar():
    for file in os.listdir("temp/Audio"):
        if file.endswith(".m4a"):  # and not f"temp/Audio/Audio-MP3s/{videosGlobal['ID'][Index[nLista]]}.m4a":
            os.remove(f"temp/Audio/{file}")

    for file in os.listdir("temp/Audio/Audio-MP3s"):
        if file.endswith(".mp3"):
            os.remove(f"temp/Audio/Audio-MP3s/{file}")


def deletarTempsAntigos(nLista, videosGlobal, Index):
    import os
    try:
        mixer.music.unload()

        for file in os.listdir("temp/Audio"):
            if file.endswith(".m4a"):  # and not f"temp/Audio/Audio-MP3s/{videosGlobal['ID'][Index[nLista]]}.m4a":
                if file != f"temp/Audio/Audio-MP3s/{videosGlobal['ID'][Index[nLista]]}.m4a":
                    os.remove(f"temp/Audio/{file}")

        for file in os.listdir("temp/Audio/Audio-MP3s"):
            if file.endswith(".mp3") and file != f"temp/Audio/Audio-MP3s/{videosGlobal['ID'][Index[nLista]]}.mp3":
                os.remove(f"temp/Audio/Audio-MP3s/{file}")

    except:
        pass


def downloadVideo(id):
    ytdlp_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': f"temp/Audio/{id}.m4a",
        'ignoreerrors': True,
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    with yt_dlp.YoutubeDL(ytdlp_opts) as ydl:
        ydl.download(f"https://www.youtube.com/watch?v={id}")


def baixarConverterTocar(nLista, videosGlobal, Index, window, botao):
    if nLista >= len(Index):
        nLista = 0

    import os
    idVideo = videosGlobal["ID"][Index[nLista]]
    downloadVideo(idVideo)

    pasta = os.path.abspath("temp/Audio")
    from flacToMp3 import flac_to_mp3
    flac_to_mp3(pasta)

    try:
        mixer.music.load(f"temp/Audio/Audio-MP3s/{videosGlobal['ID'][Index[nLista]]}.mp3")
        mixer.music.play()
        os.remove(f"temp/Audio/{videosGlobal['ID'][Index[nLista]]}.m4a")
        unavaliable = False
        return nLista, videosGlobal, Index, unavaliable, botao

    except:
        unavaliable = True
        return nLista, videosGlobal, Index, unavaliable, botao


def audioAtualizarVideo(nLista, videosGlobal, Index, window, botao):
    starting = True

    deletarTempsAntigos(nLista, videosGlobal, Index)
    window.perform_long_operation(lambda: baixarConverterTocar(nLista, videosGlobal, Index, window, botao), '-DownloadEnd-')

    return starting