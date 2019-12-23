import os
import sys
import unittest

import pylrc

FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(FILE_PATH))


class TestMatches(unittest.TestCase):
    def setUp(self):
        self.static_path = os.path.join(FILE_PATH, 'tests', 'static')

    def test_lrc_to_srt(self):
        path = os.path.join(self.static_path, 'lrc_to_srt')
        for file in os.listdir(path):
            if file.endswith('.lrc'):
                lrc_path = os.path.join(path, file)
                lrc_file = open(lrc_path)
                lrc_text = lrc_file.read()
                lrc_file.close()

                sub = pylrc.parse(lrc_text)

                srt_file = open(os.path.splitext(lrc_path)[0] + '.srt')
                srt_text = srt_file.read()
                srt_file.close()

                self.assertEqual(sub.toSRT(), srt_text)

    def test_offset(self):
        song_path = os.path.join(self.static_path, 'P!nk - Bridge of Light.lrc')

        with open(song_path, "r", encoding="UTF-8") as song_file:
            lrc_text = pylrc.parse(song_file.read())

            self.assertEqual(lrc_text.offset, -15000)

            self.assertEqual(lrc_text[0].hours, 0)
            self.assertEqual(lrc_text[0].minutes, 0)
            self.assertEqual(lrc_text[0].seconds, -13)
            self.assertEqual(lrc_text[0].milliseconds, -270)

            self.assertEqual(lrc_text[4].hours, 0)
            self.assertEqual(lrc_text[4].minutes, 0)
            self.assertEqual(lrc_text[4].seconds, 1)
            self.assertEqual(lrc_text[4].milliseconds, 890)

            self.assertEqual(lrc_text[24].hours, 0)
            self.assertEqual(lrc_text[24].minutes, 1)
            self.assertEqual(lrc_text[24].seconds, 29)
            self.assertEqual(lrc_text[24].milliseconds, 0)

            self.assertEqual(lrc_text[32].hours, 0)
            self.assertEqual(lrc_text[32].minutes, 1)
            self.assertEqual(lrc_text[32].seconds, 56)
            self.assertEqual(lrc_text[32].milliseconds, 400)

    def test_shifting_millis(self):
        line = pylrc.parser.LyricLine(timecode="[2:2.2]", text="")

        line.addMillis(-300)
        self.assertEqual(1, line.seconds)
        self.assertEqual(900, line.milliseconds)

        line.addMillis(100)
        self.assertEqual(2, line.seconds)
        self.assertEqual(0, line.milliseconds)

        line.addMillis(-122040)
        self.assertEqual(0, line.minutes)
        self.assertEqual(0, line.seconds)
        self.assertEqual(-40, line.milliseconds)

        line.addMillis(50)
        self.assertEqual(10, line.milliseconds)

    def test_shifting_seconds(self):
        line = pylrc.parser.LyricLine(timecode="[2:2.2]", text="")

        line.addSeconds(-62)
        self.assertEqual(1, line.minutes)
        self.assertEqual(0, line.seconds)
        self.assertEqual(200, line.milliseconds)

        line.addSeconds(-61)
        self.assertEqual(0, line.minutes)
        self.assertEqual(0, line.seconds)
        self.assertEqual(-800, line.milliseconds)

        line.addSeconds(16)
        self.assertEqual(0, line.minutes)
        self.assertEqual(15, line.seconds)
        self.assertEqual(200, line.milliseconds)

        line.addSeconds(3666)
        self.assertEqual(1, line.hours)
        self.assertEqual(1, line.minutes)
        self.assertEqual(21, line.seconds)
        self.assertEqual(200, line.milliseconds)


if __name__ == '__main__':
    unittest.main()
