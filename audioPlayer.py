import PySimpleGUI as sg
import textwrap
from audioPlayerFunctions import convertToBase64, toogleInterfaceMusica, audioAtualizarVideo, tempoExibicao, deletarTempsFinalizar, carregarProximaMusica, botoesVideos, botaoDownloadMusica, botaoVolume, unpauseOnButton
from pygame import mixer

import time


def audioPlayerInterface(videosGlobal, playlistGlobal, Index):
    ##################### SETUP ###########################
    sg.theme("DarkPurple3")

    botaoPlayImagem = convertToBase64("resources/botaoPlay.png")
    botaoPauseImagem = convertToBase64("resources/botaoPause.png")
    botaoSkipEsquerdo = convertToBase64("resources/botaoSkipesquerdo.png")
    botaoSkipDireito = convertToBase64("resources/botaoSkipDireito.png")

    coluna1 = [
        [sg.Image(key="ImagemPlaylist", pad=(0, 10))],
        [sg.Text('', key="Titulo", font=('Arial', 11, 'bold'))],
        [sg.Text(pad=(0, 10), key="-TempoAtual-"), sg.Text("", key="-pad1-", pad=(127, 0)), sg.Text(pad=(0, 10), key="-TempoTotal-")],
        [sg.Slider(range=(0, 60), orientation='horizontal', size=(35, 15), key='-Slider-', disable_number_display=True)],
        [sg.Text("", pad=(0, 10), key="-pad2-")],
        [sg.Button('', image_data=botaoSkipEsquerdo, key="BotaoSkipEsquerda"),
         sg.Button('', image_data=botaoPauseImagem, key="BotaoPausePlay", pad=(17, 0)),
         sg.Button('', image_data=botaoSkipDireito, key="BotaoSkipDireita")],
        [sg.Text("", pad=(0, 1))]
    ]

    coluna2 = [
        [
         sg.Image("resources/carregamentoLoop.gif", pad=(113, 200), key="-GIF-")
        ]
    ]

    coluna3 = [
        [
            sg.Text("VOLUME:", key="-volumeTitulo-", pad=(130, 0))
        ],
        [
            sg.Text("", key="-avisos-", pad=(55, 0)), sg.Slider(range=(0, 100), default_value=30, orientation='horizontal', size=(25, 15), pad=(48, 0), key='-volumeSlider-')
        ]
    ]

    coluna4 = [
        [
            sg.Text("", pad=(0, 3))
        ],
        [
            sg.Button(' Download ', key="BotaoDownload"),
            sg.Button('  Link  ', pad=(12, 0), key="BotaoLink"),
            sg.Button('  Volume  ', pad=(10, 0), key="BotaoVolume"),
            sg.Button('  Fechar  ', pad=(10, 0), key="BotaoFechar")
        ]
    ]


    layout = [
        [sg.pin(sg.Column(coluna1, key='-col1-', visible=False, expand_y=True))],
        [sg.pin(sg.Column(coluna2, key='-col2-', visible=True, vertical_alignment='center', justification='center'))],
        [sg.pin(sg.Column(coluna3, key='-col3-', visible=False, vertical_alignment='center', justification='center'))],
        [sg.pin(sg.Column(coluna4, key='-col4-', visible=False, vertical_alignment='center', justification='center'))]
    ]

    ##################### INIT ###########################
    durVideo = 1e-6
    videoAtual = 0
    mixer.init()
    window = sg.Window(title='YoutubePlaylistRandomizer', layout=layout, margins=(75, 50))
    window.perform_long_operation(lambda : audioAtualizarVideo(videoAtual, videosGlobal, Index, window, "-Slider-"), '-update-')

    current_time = 0
    last_time = 0
    pauseTimeStart = 0
    pauseTimeEnd = 0

    starting = True
    changeVolume = False

    ##################### LOOP ###########################
    paused = False
    start_time = int(round(time.time() * 100))
    while (True):
        event, values = window.read(timeout=25)

        window.Element('-GIF-').UpdateAnimation('resources/carregamentoLoop.gif', time_between_frames=0)


        if not paused and not starting:
            try:
                current_time = int(round(time.time() * 100)) - start_time
                last_time = int(values['-Slider-'])
                exhibition_time = tempoExibicao(last_time)
                window['-TempoAtual-'].update(value=exhibition_time)
                if last_time - current_time // 100 == 0 or last_time - current_time // 100 == -1:
                    window['-Slider-'].update(value=current_time // 100)

                else:
                    start_time -= (last_time * 100 - current_time)
                    mixer.music.set_pos(last_time)
            except:
                pass

        else:
            try:
                slider_time = int(values['-Slider-'])
                exhibition_time = tempoExibicao(slider_time)
                window['-TempoAtual-'].update(value=exhibition_time)

            except:
                pass
        if event == '-update-':
            starting = values[event]

        if event == "-DownloadEnd-":
            window.refresh()
            window['-Slider-'].update(value=0)

            nLista, videosGlobal, Index, unavaliable, botao = values[event]

            if unavaliable == False:
                numVideo = Index[nLista]
                tituloVideo = videosGlobal['Título'][numVideo]
                tituloVideoCortado = textwrap.wrap(tituloVideo, 41)
                durVideo = videosGlobal['Duração'][numVideo]

                import requests
                from FuncoesAdicionais import ConverterParaPNG
                imagem = requests.get(videosGlobal['Thumb'][numVideo])
                png_data = ConverterParaPNG(imagem)

                exhibition_time = tempoExibicao(0)
                exhibition_video_lenght = tempoExibicao(durVideo)

                start_time = int(round(time.time() * 100))

                toogleInterfaceMusica(True, window)

            else:
                if botao == "BotaoSkipEsquerda":
                    videoAtual -= 1
                else:
                    videoAtual += 1
                starting = carregarProximaMusica(window, videoAtual, videosGlobal, Index, botao)

            ###################### SETUP ##########################

            window["ImagemPlaylist"].update(png_data)
            window["Titulo"].update(tituloVideoCortado[0])
            window["-TempoAtual-"].update(exhibition_time)
            window["-TempoTotal-"].update(exhibition_video_lenght)
            window["-Slider-"].update(range=(0, durVideo))

            starting = False

        if event == "BotaoFechar" or event == sg.WINDOW_CLOSED:
            mixer.music.stop()
            mixer.music.unload()
            deletarTempsFinalizar()
            break

        if event == "BotaoPausePlay":
            if not paused:
                mixer.music.pause()
                window["BotaoPausePlay"].update(image_data=botaoPlayImagem)
                paused = True
                pauseTimeStart = int(round(time.time() * 100)) - start_time
            else:
                mixer.music.unpause()
                window["BotaoPausePlay"].update(image_data=botaoPauseImagem)
                paused = False
                pauseTimeEnd = int(round(time.time() * 100)) - start_time
                start_time += pauseTimeEnd - pauseTimeStart

        if event == "BotaoSkipEsquerda":
            videoAtual, changeVolume = botoesVideos(videoAtual, Index, event)
            starting = carregarProximaMusica(window, videoAtual, videosGlobal, Index, event)
            window.refresh()
            window['-Slider-'].update(value=0)
            paused, pauseTimeEnd, start_time = unpauseOnButton(start_time, pauseTimeStart, window, botaoPauseImagem)

        if event == "BotaoSkipDireita":
            videoAtual, changeVolume = botoesVideos(videoAtual, Index, event)
            starting = carregarProximaMusica(window, videoAtual, videosGlobal, Index, event)
            window.refresh()
            window['-Slider-'].update(value=0)
            window["BotaoPausePlay"].update(image_data=botaoPauseImagem)
            paused, pauseTimeEnd, start_time = unpauseOnButton(start_time, pauseTimeStart, window, botaoPauseImagem)


        if int(values['-Slider-']) == durVideo and starting == False:
            videoAtual, changeVolume = botoesVideos(videoAtual, Index, "-Slider-")
            starting = carregarProximaMusica(window, videoAtual, videosGlobal, Index, "-Slider-")
            window.refresh()
            window['-Slider-'].update(value=0)
            paused, pauseTimeEnd, start_time = unpauseOnButton(start_time, pauseTimeStart, window, botaoPauseImagem)

        if event == "BotaoLink":
            url = f"https://www.youtube.com/watch?v={videosGlobal['ID'][numVideo]}&list={playlistGlobal['id'][0]}"
            from FuncoesAdicionais import AbrirNavegador
            AbrirNavegador(url)

        if event == "BotaoDownload":
            botaoDownloadMusica(window, videosGlobal['Título'][numVideo])

        if event == "BotaoVolume":
            changeVolume = botaoVolume(window, changeVolume)

        if starting == False:
            volume = values['-volumeSlider-']
            mixer.music.set_volume(volume/100)

    window.close()

