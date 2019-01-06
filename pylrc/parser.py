from .classes import Lyrics, LyricLine
from .utilities import validateTimecode


def parse(lrc):
    lines = lrc.split('\n')
    lyrics = Lyrics()
    items = []

    for i in lines:
        if i.startswith('[ar:'):
            lyrics.artist = i.rstrip()[4:-1].lstrip()

        elif i.startswith('[ti:'):
            lyrics.title = i.rstrip()[4:-1].lstrip()

        elif i.startswith('[al:'):
            lyrics.album = i.rstrip()[4:-1].lstrip()

        elif i.startswith('[by:'):
            lyrics.author = i.rstrip()[4:-1].lstrip()

        elif i.startswith('[length:'):
            lyrics.length = i.rstrip()[8:-1].lstrip()

        elif i.startswith('[offset:'):
            try:
                lyrics.offset = int(i.rstrip()[8:-1].lstrip())
            except ValueError:
                pass

        elif i.startswith('[re:'):
            lyrics.editor = i.rstrip()[4:-1].lstrip()

        elif i.startswith('[ve:'):
            lyrics.version = i.rstrip()[4:-1].lstrip()

        elif len(i.split(']')[0]) >= len('[0:0:0]'):
            if validateTimecode(i.split(']')[0] + ']'):
                while validateTimecode(i.split(']')[0] + ']'):
                    timecode = i.split(']')[0] + ']'
                    text = ''.join(i.split(']')[-1]).rstrip()
                    lyric_line = LyricLine(timecode, text=text)
                    items.append(lyric_line)

                    i = i[len(timecode)::]

    lyrics.extend(sorted(items))

    if not lyrics.offset == 0:
        millis = lyrics.offset

        mins = int(millis / 60000)
        millis %= millis / 60000

        secs = int(millis / 1000)
        millis %= millis / 1000

        for i in lyrics:
            i.shift(minutes=mins, seconds=secs, milliseconds=millis)

    return lyrics
