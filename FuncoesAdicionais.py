def AbrirNavegador(url):
    import webbrowser
    webbrowser.open(url)


def ConverterParaPNG(imagem):
    from PIL import Image
    import io

    imgJPG = Image.open(io.BytesIO(imagem.content))
    png_bio = io.BytesIO()
    imgJPG.save(png_bio, format="PNG")
    png_data = png_bio.getvalue()

    return png_data


def atualizarDadosPlaylist(window, playlist, playlistvideos):
    window["BotaoAbrir"].update(visible=True)
    window["BotaoRandomizar"].update(visible=True)
    window["BotaoExportarPlaylist"].update(visible=True)
    window["BotaoTocar"].update(visible=True)
    window["BotaoTocarRandom"].update(visible=True)
    window["tituloPlaylist"].update(f"Título: {playlist['nome'][0]}")
    window["nomeDoAutor"].update(f"Autor: {playlist['canal'][0]}")
    window["qtdVideos"].update(f"{playlist['qtdVideos'][0]} Vídeos")
    window["ExportadoPlaylist"].update("")

    import requests

    imagem = requests.get(playlist['thumb'][0])
    png_data = ConverterParaPNG(imagem)
    window["ImagemPlaylist"].update(png_data)
    videosGlobal = playlistvideos

    playlistGlobal = playlist

    return playlistGlobal, videosGlobal


def criarTempPlaylist(playlistImportada, playlistVideosImportados):
    import os

    if not os.path.exists('temp'):
        os.makedirs('temp')

    path = f'temp/Playlist'
    if not os.path.exists(path):
        os.makedirs(path)

    playlistImportada.to_excel(f'{path}/playlistInfo.xlsx', index=False)
    playlistVideosImportados.to_excel(f'{path}/playlistVideosInfo.xlsx', index=False)