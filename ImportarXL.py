def importarPlaylistXL(path):
    pathPlaylistInfo = path + "/playlistinfo.xlsx"
    pathVideosInfo = path + "/playlistVideosInfo.xlsx"

    import pandas as pd
    playlistImportada = pd.read_excel(pathPlaylistInfo)
    playlistVideosImportados = pd.read_excel(pathVideosInfo)
    return playlistImportada, playlistVideosImportados