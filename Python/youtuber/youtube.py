from pytube import YouTube


class YouTuber(object):
    def __init__(self):
        pass

    def _authenticate(self):
        pass

    def scan_yt_playlist(self, playlist_name):
        pass

    def download(self, audio=True, video=False):
        pass


if __name__ == '__main__':

    # creating YouTube object
    yt = YouTube("https://www.youtube.com/watch?v=1csFTDXXULY")

    # accessing audio streams of YouTube obj.(first one, more available)
    stream = yt.streams.filter(only_audio=True).first()
    # downloading a video would be: stream = yt.streams.first()

    # download into working directory
    stream.download()