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
            self.assertEqual(lrc_text[0].seconds, -14)
            self.assertEqual(lrc_text[0].milliseconds, 730)

            self.assertEqual(lrc_text[4].hours, 0)
            self.assertEqual(lrc_text[4].minutes, 0)
            self.assertEqual(lrc_text[4].seconds, 1)
            self.assertEqual(lrc_text[4].milliseconds, 890)

            self.assertEqual(lrc_text[24].hours, 0)
            self.assertEqual(lrc_text[24].minutes, 1)
            self.assertEqual(lrc_text[24].seconds, 29)
            self.assertEqual(lrc_text[24].milliseconds, 0)

            self.assertEqual(lrc_text[32].hours, 0)
            self.assertEqual(lrc_text[32].minutes, 2)
            self.assertEqual(lrc_text[32].seconds, -4)
            self.assertEqual(lrc_text[32].milliseconds, 400)


if __name__ == '__main__':
    unittest.main()
