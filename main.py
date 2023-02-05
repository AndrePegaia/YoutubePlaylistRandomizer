import PySimpleGUI as sg
import os

from FuncoesYTB import pesquisar_playlist, pesquisar_playlist_basic_info
from FuncoesAdicionais import AbrirNavegador, atualizarDadosPlaylist, criarTempPlaylist
from ExportarXL import exportarPlaylistXL
from ImportarXL import importarPlaylistXL
from audioPlayer import audioPlayerInterface

path = os.path.abspath("")
newPath = path.replace(os.sep, '/')

playlistGlobal = []
videosGlobal = []

sg.theme("DarkBlue13")

def carregarTemp():
    playlist, playlistvideos = importarPlaylistXL("temp/Playlist")

    import requests
    from FuncoesAdicionais import ConverterParaPNG
    imagem = requests.get(playlist['thumb'][0])
    png_data = ConverterParaPNG(imagem)

    coluna1 = [
        [sg.Text("PLAYLIST RANDOMIZER", pad=(0, 35))],
        [sg.Text("Insira a URL da Playlist: ")],
        [sg.In(size=(50, 10), enable_events=True, key="BarraPesquisa")],
        [sg.Button("Pesquisar", size=(10, 0)), sg.Text("", size=(40, 1), key="Aguarde", pad=(30, 10))],
        [sg.Text("", pad=(0, 5))],
        [sg.Text("Insira o caminho da pasta da playlist: ")],
        [sg.In(size=(40, 10), enable_events=True, key="BarraBrowse"),
         sg.FolderBrowse("Procurar", initial_folder=os.path.abspath(newPath + "/Playlists Info"), size=(8, 0))],
        [sg.Button("Importar", size=(10, 0)), sg.Text("", size=(40, 1), key="ImportadoPlaylist", pad=(30, 10))],
        [sg.Text("", pad=(0, 10))],
        [sg.Button("Fechar", size=(20, 1), pad=(100, 0))],
        [sg.Text("", pad=(0, 10))]
    ]

    coluna2 = [
        [sg.Text(f"Título: {playlist['nome'][0]}", size=(40, 1), key="tituloPlaylist", pad=(0, 10))],
        [sg.Image(png_data, key="ImagemPlaylist", pad=(0, 10))],
        [sg.Text(f"Autor: {playlist['canal'][0]}", size=(40, 1), key="nomeDoAutor")],
        [sg.Text(f"{playlist['qtdVideos'][0]} Vídeos", size=(40, 1), key="qtdVideos")],
        [sg.Button("Abrir", visible=True, key="BotaoAbrir"),
         sg.Button("Exportar", visible=True, key="BotaoExportarPlaylist", pad=(0, 10)),
         sg.Button("Randomizar", visible=True, key="BotaoRandomizar")],
        [sg.Button("Tocar", visible=True, key="BotaoTocar"),
         sg.Button("Tocar aleatório", visible=True, key="BotaoTocarRandom", pad=(0, 10))],
        [sg.Text("", size=(40, 1), key="ExportadoPlaylist")]
    ]

    layout = [
        [
            sg.Column(coluna1),
            sg.VSeparator(pad=(50, 0)),
            sg.Column(coluna2)
        ]
    ]

    playlistGlobal = playlist
    videosGlobal = playlistvideos

    return layout, playlistGlobal, videosGlobal

def aplicacao():
    try:
        layout, playlistGlobal, videosGlobal = carregarTemp()

    except:
        coluna1 = [
            [sg.Text("PLAYLIST RANDOMIZER", pad=(0, 35))],
            [sg.Text("Insira a URL da Playlist: ")],
            [sg.In(size=(50, 10), enable_events=True, key="BarraPesquisa")],
            [sg.Button("Pesquisar", size=(10, 0)), sg.Text("", size=(40, 1), key="Aguarde", pad=(30, 10))],
            [sg.Text("", pad=(0, 5))],
            [sg.Text("Insira o caminho da pasta da playlist: ")],
            [sg.In(size=(40, 10), enable_events=True, key="BarraBrowse"),
             sg.FolderBrowse("Procurar", initial_folder=os.path.abspath(newPath + "/Playlists Info"), size=(8, 0))],
            [sg.Button("Importar", size=(10, 0)), sg.Text("", size=(40, 1), key="ImportadoPlaylist", pad=(30, 10))],
            [sg.Text("", pad=(0, 10))],
            [sg.Button("Fechar", size=(20, 1), pad=(100, 0))],
            [sg.Text("", pad=(0, 10))]
        ]

        coluna2 = [
            [sg.Text(size=(40, 1), key="tituloPlaylist", pad=(0, 10))],
            [sg.Image(key="ImagemPlaylist", pad=(0, 10))],
            [sg.Text(size=(40, 1), key="nomeDoAutor")],
            [sg.Text(size=(40, 1), key="qtdVideos")],
            [sg.Button("Abrir", visible=False, key="BotaoAbrir"),
             sg.Button("Exportar", visible=False, key="BotaoExportarPlaylist", pad=(0, 10)),
             sg.Button("Randomizar", visible=False, key="BotaoRandomizar")],
        [sg.Button("Tocar", visible=False, key="BotaoTocar"),
         sg.Button("Tocar aleatório", visible=False, key="BotaoTocarRandom", pad=(0, 10))],
            [sg.Text(size=(40, 1), key="ExportadoPlaylist")]
        ]

        layout = [
            [
                sg.Column(coluna1),
                sg.VSeparator(pad=(50, 0)),
                sg.Column(coluna2)
            ]
        ]

    window = sg.Window(title='YoutubePlaylistRandomizer', layout=layout, margins=(75, 50))

    pesquisaURL = ""

    while True:
        event, values = window.read()

        if event == "BarraPesquisa":
            pesquisaURL = values["BarraPesquisa"]

        if event == "Pesquisar":
            if pesquisaURL.__contains__("youtube.com"):
                try:
                    window["Aguarde"].update("Carregando informações da playlist....")
                    window.perform_long_operation(lambda:pesquisar_playlist_basic_info(pesquisaURL), 'FIM_DA_PESQUISA_BASICA')

                except:
                    window["Aguarde"].update("Erro na pesquisa!! Tente novamente!")
            else:
                window["Aguarde"].update("Link inválido!! Tente novamente!!")

        if event == 'FIM_DA_PESQUISA_BASICA':
            service, playlist, playlistItems = values[event]
            if playlist:
                numVideos = playlist[0]['contentDetails']['itemCount']
                tempoCarregamento = f"{int((int(numVideos)/10)//60)} min {int((int(numVideos)/10)%60 + 1)} s"
                window["Aguarde"].update(f"Carregando {numVideos} vídeos. Tempo estimado: {tempoCarregamento}")
                window.perform_long_operation(lambda: pesquisar_playlist(service, playlist, playlistItems),'-FIM_DA_PESQUISA-')

            else:
                window["Aguarde"].update("Erro na pesquisa!! Insira um URL válido!")

        if event == '-FIM_DA_PESQUISA-':
            playlistDF, videosDF = values[event]
            playlistGlobal, videosGlobal = atualizarDadosPlaylist(window, playlistDF, videosDF)
            window["Aguarde"].update("Playlist encontrada com sucesso!!")
            criarTempPlaylist(playlistDF, videosDF)

        if event == "Importar":
            try:
                playlistImportada, playlistVideosImportados = importarPlaylistXL(values["BarraBrowse"])
                playlistGlobal, videosGlobal = atualizarDadosPlaylist(window, playlistImportada, playlistVideosImportados)
                window["ImportadoPlaylist"].update("Playlist importada com sucesso!")
                criarTempPlaylist(playlistImportada, playlistVideosImportados)

            except:
                window["ImportadoPlaylist"].update("Selecione uma pasta válida!")

        if event == "Fechar" or event == sg.WINDOW_CLOSED:
            break

        if event == "BotaoAbrir":
            url = f"https://www.youtube.com/watch?v={videosGlobal['ID'][0]}&list={playlistGlobal['id'][0]}"
            AbrirNavegador(url)

        if event == "BotaoRandomizar":
            playlistSize = playlistGlobal['qtdVideos'][0]

            import random
            randomIndex = [*range(0, playlistSize - 1)]
            random.shuffle(randomIndex)
            url = f"https://www.youtube.com/watch?v={videosGlobal['ID'][randomIndex[0]]}&list={playlistGlobal['id'][0]}"
            AbrirNavegador(url)

        if event == "BotaoExportarPlaylist":
            try:
                exportarPlaylistXL(playlistGlobal, videosGlobal)
                window["ExportadoPlaylist"].update("Playlist exportada com sucesso!")

            except:
                window["ExportadoPlaylist"].update("Erro na exportação da Playlist!")

        if event == "BotaoTocar":
            Index = [*range(0, int(playlistGlobal['qtdVideos']) - int(playlistGlobal['qtdVideosIndisponiveis']))]
            audioPlayerInterface(videosGlobal, playlistGlobal, Index)

        if event == "BotaoTocarRandom":
            import random
            randomIndex = [*range(0, int(playlistGlobal['qtdVideos']) - int(playlistGlobal['qtdVideosIndisponiveis']))]
            random.shuffle(randomIndex)
            audioPlayerInterface(videosGlobal, playlistGlobal, randomIndex)

    window.close()


aplicacao()