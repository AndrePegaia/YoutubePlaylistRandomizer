import os
import pandas as pd


def converter_duracao(duracao):
    import re
    try:
        h = int(re.search('\d+H', duracao)[0][:-1]) * 60 ** 2 if re.search('\d+H', duracao) else 0  # hour
        m = int(re.search('\d+M', duracao)[0][:-1]) * 60 if re.search('\d+M', duracao) else 0  # minute
        s = int(re.search('\d+S', duracao)[0][:-1]) if re.search('\d+S', duracao) else 0  # second
        return h + m + s
    except Exception as e:
        print(e)
        return 0


def InformacoesPlaylist(playlist, numVideosIndisponiveis):
    playlistInfo = {'nome': playlist[0]['snippet']['title'], 'id': playlist[0]['id'],
                    'thumb': playlist[0]['snippet']['thumbnails']['medium']['url'],
                    'data': str(playlist[0]['snippet']['publishedAt']),
                    'canal': playlist[0]['snippet']['channelTitle'],
                    'qtdVideos': playlist[0]['contentDetails']['itemCount'],
                    'qtdVideosIndisponiveis': numVideosIndisponiveis}
    df = pd.DataFrame(data=playlistInfo, index=[0])
    return df


def InformacoesVideos(playlist, info_playlist_videos):
    ID, URL, TITULO, DATA, DURACAO, VIEWS, THUMB = [], [], [], [], [], [], []

    for video in range(0, len(info_playlist_videos)):
        ID.append(info_playlist_videos[video][0])
        URL.append(f"https://www.youtube.com/watch?v={info_playlist_videos[video][0]}&list={playlist[0]['id']}")
        TITULO.append(info_playlist_videos[video][1])
        DATA.append(info_playlist_videos[video][2])
        DURACAO.append(converter_duracao(info_playlist_videos[video][3]))
        VIEWS.append(info_playlist_videos[video][4])
        THUMB.append(info_playlist_videos[video][5])
    df = pd.DataFrame(list(zip(ID, URL, TITULO, DATA, DURACAO, VIEWS, THUMB)))
    df.columns = ['ID', 'URL', 'Título', 'Autor', 'Duração', 'Views', 'Thumb']
    return df


def exportarPlaylistXL(playlistGlobal, videosGlobal):
    if not os.path.exists('Playlists Info'):
        os.makedirs('Playlists Info')

    nomePasta = f"Playlist {playlistGlobal['nome'][0]}"
    path = f'Playlists Info/{nomePasta}'
    if not os.path.exists(path):
        os.makedirs(path)

    playlistGlobal.to_excel(f'{path}/playlistInfo.xlsx', index=False)
    videosGlobal.to_excel(f'{path}/playlistVideosInfo.xlsx', index=False)