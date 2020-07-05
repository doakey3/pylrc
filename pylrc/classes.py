from .utilities import unpackTimecode, findEvenSplit


class LyricLine:
    """An object that holds a lyric line and it's time"""

    def __init__(self, timecode, text=""):
        self.hours = 0
        self.minutes, self.seconds, self.milliseconds = unpackTimecode(timecode)
        self.time = sum([(self.hours * 3600), (self.minutes * 60),
                         self.seconds, (self.milliseconds / 1000)])
        self.text = text

    def shift(self, minutes=0, seconds=0, milliseconds=0):
        """Shift the timecode by the given amounts"""

        self.addMinutes(minutes)
        self.addSeconds(seconds)
        self.addMillis(milliseconds)

    def addMillis(self, milliseconds):
        summation = self.milliseconds + milliseconds
        if summation >= 1000 or summation <= -1000:
            self.milliseconds = summation % (1000 if (summation > 0) else -1000)
            self.addSeconds(int(summation / 1000))
        else:
            self.milliseconds = summation
        self._check()

    def addSeconds(self, seconds):
        summation = self.seconds + seconds
        if summation >= 60 or summation <= -60:
            self.seconds = summation % (60 if (summation > 0) else -60)
            self.addMinutes(int(summation / 60))
        else:
            self.seconds = summation
        self._check()

    def addMinutes(self, minutes):
        summation = self.minutes + minutes
        if summation >= 60 or summation <= -60:
            self.minutes = summation % (60 if (summation > 0) else -60)
            self.addHours(int(summation / 60))
        else:
            self.minutes = summation
        self._check()

    def addHours(self, hours):
        summation = self.hours + hours
        if summation > 23:
            self.hours = 23
        elif summation < 0:
            self.hours = 0
            self.minutes = 0
            self.seconds = 0
            self.milliseconds = 0
        else:
            self.hours = summation
        self._check()

    def _check(self):
        if self.hours < 0 < self.minutes:
            self.hours += 1
            self.minutes -= 60
        elif self.minutes < 0 < self.hours:
            self.hours -= 1
            self.minutes += 60
        if self.minutes < 0 < self.seconds:
            self.minutes += 1
            self.seconds -= 60
        elif self.seconds < 0 < self.minutes:
            self.minutes -= 1
            self.seconds += 60
        if self.seconds < 0 < self.milliseconds:
            self.seconds += 1
            self.milliseconds -= 1000
        elif self.milliseconds < 0 < self.seconds:
            self.seconds -= 1
            self.milliseconds += 1000
        self.time = sum([(self.hours * 3600), (self.minutes * 60),
                         self.seconds, (self.milliseconds / 1000)])

    def __lt__(self, other):
        """For sorting instances of this class"""
        return self.time < other.time


class Lyrics(list):
    """A list that holds the contents of the lrc file"""

    def __init__(self, items=None):

        super().__init__()
        if items is None:
            items = []
        self.artist = ""
        self.album = ""
        self.title = ""
        self.author = ""
        self.lrc_creator = ""
        self.length = ""
        self.offset = 0

        self.extend(items)

    def toSRT(self):
        """Returns an SRT string of the LRC data"""

        if not self[-1].text.rstrip() == "":
            timecode = ''.join(['[', str(self[-1].minutes), ':',
                                str(self[-1].seconds), '.',
                                str(self[-1].milliseconds), ']'])
            end_line = LyricLine(timecode, "")
            end_line.shift(seconds=5)
            self.append(end_line)

        output = []
        for i in range(len(self) - 1):
            if not self[i].text == '':
                srt = str(i) + '\n'
                start_hours = "%02d" % self[i].hours
                start_min = "%02d" % self[i].minutes
                start_sec = "%02d" % self[i].seconds
                start_milli = "%03d" % self[i].milliseconds
                start_timecode = ''.join([start_hours, ':', start_min,
                                          ':', start_sec, ',', start_milli])
                end_hours = "%02d" % self[i + 1].hours
                end_min = "%02d" % self[i + 1].minutes
                end_sec = "%02d" % self[i + 1].seconds
                milliseconds = self[i + 1].milliseconds - 1
                end_milli = "%03d" % (0 if milliseconds < 0 else milliseconds)
                end_timecode = ''.join([end_hours, ':', end_min,
                                        ':', end_sec, ',', end_milli])

                srt = srt + start_timecode + ' --> ' + end_timecode + '\n'
                if len(self[i].text) > 31:
                    srt = srt + findEvenSplit(self[i].text) + '\n'
                else:
                    srt = srt + self[i].text + '\n'
                output.append(srt)

        return '\n'.join(output).rstrip()

    def toLRC(self):
        output = []
        if self.artist != "":
            output.append('[ar:' + self.artist + ']')
        if self.album != "":
            output.append('[al:' + self.album + ']')
        if self.title != "":
            output.append('[ti:' + self.title + ']')
        if self.author != "":
            output.append('[au:' + self.author + ']')
        if self.lrc_creator != "":
            output.append('[by:' + self.lrc_creator + ']')
        if self.length != "":
            output.append('[length:' + self.length + ']')
        if self.offset != 0:
            output.append('[offset:' + str(self.offset) + ']')

        if output:
            output.append('')

        for i in self:
            minutes = "%02d" % i.minutes
            seconds = "%02d" % i.seconds
            milliseconds = ("%02d" % i.milliseconds)[0:2]

            lrc = ''.join(['[', minutes, ':', seconds, '.', milliseconds, ']'])
            lrc += i.text
            output.append(lrc)
        return '\n'.join(output).rstrip()
