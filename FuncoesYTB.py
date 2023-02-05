import json
from googleapiclient.errors import HttpError


def receber_service():
    from Google import Create_Service
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    return service


def receber_playlist(service, playlist_id):
    playlist = []
    try:
        response = service.playlists().list(
            part='contentDetails,snippet,status',
            id=playlist_id,
            maxResults=50
        ).execute()

        playlist.extend(response.get('items'))
        nextPageToken = response.get('nextPageToken')
        nextPageToken
        return playlist
    except HttpError as e:
        errMsg = json.loads(e.content)
        print ('HTTP Error')
        print (errMsg['error']['message'])
        return []


def receber_playlist_items(service, playlist_id):
    playlist_items = []
    try:
        response = service.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50
        ).execute()

        playlist_items.extend(response['items'])
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = service.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=nextPageToken
            ).execute()

            playlist_items.extend(response['items'])
            nextPageToken = response.get('nextPageToken')
        print("Playlist carregada com sucesso!")
        return playlist_items

    except HttpError as e:
        errMsg = json.loads(e.content)
        print('HTTP Error:')
        print(errMsg['error']['message'])
        return []

    except Exception as e:
        errMsg = json.loads(e.content)
        print('Error:')
        print(errMsg['error']['message'])
        return []


def receber_info_videos(service, videoId):
    video_info = service.videos().list(
        id=videoId,
        part='snippet,contentDetails,statistics'
    ).execute()['items'][0]

    video_response = [video_info['id'], video_info['snippet']['title'], video_info['snippet']['publishedAt'],
                    video_info['contentDetails']['duration'], video_info['statistics']['viewCount'], video_info['snippet']['thumbnails']['medium']['url']]
    return video_response


def procurar_playlist(service, playlistId):
    playlist = receber_playlist(service, playlistId)
    playlistItems = receber_playlist_items(service, playlistId)
    return playlist, playlistItems


from ExportarXL import InformacoesPlaylist, InformacoesVideos


def pesquisar_playlist_basic_info(playlistURL):
    service = receber_service()
    playlistId = playlistURL.split('list=')[1].split('&')[0]
    playlist, playlistItems = procurar_playlist(service, playlistId)
    return service, playlist, playlistItems


def pesquisar_playlist(service, playlist, playlistItems):
    info_playlist_videos = []
    numVideosIndisponiveis = 0
    for video in range(0, len(playlistItems)):
        try:
            info_playlist_videos.append(receber_info_videos(service, playlistItems[video]['contentDetails']['videoId']))
            print(f'Vídeo {video}')
        except:
            numVideosIndisponiveis += 1

    playlistDF = InformacoesPlaylist(playlist, numVideosIndisponiveis)
    videosDF = InformacoesVideos(playlist, info_playlist_videos)


    return playlistDF, videosDF