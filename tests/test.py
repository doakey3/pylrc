import os
import sys
import unittest
import ntpath

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(file_path))

import pylrc

class TestMatches(unittest.TestCase):
    def setUp(self):
        self.static_path = os.path.join(file_path, 'tests', 'static')
        
    def test_lrc_to_srt(self):
        for file in os.listdir(self.static_path):
            if file.endswith('.lrc'):
                lrc_path = os.path.join(self.static_path, file)
                lrc_file = open(lrc_path)
                lrc_text = lrc_file.read()
                lrc_file.close()
                
                sub = pylrc.parse(lrc_text)
                
                srt_file = open(os.path.splitext(lrc_path)[0] + '.srt')
                srt_text = srt_file.read()
                srt_file.close()
                
                self.assertEqual(sub.toSRT(), srt_text)
                
if __name__ == '__main__':
    unittest.main()
