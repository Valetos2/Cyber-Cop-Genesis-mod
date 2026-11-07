"""No game files or network needed: regression tests for the publication guard."""
import unittest
from check_publication import problem

class PublicationTests(unittest.TestCase):
    def test_sources(self):
        for name,data in [('v36/build.py',b'print("hi")'),('AGENTS.md',b'# Rules'),('atlas38/template.html',b'<script>const data=__DATA__</script>'),('atlas38/test_ui.js',b'const x=1;'),('v36/symbols.json',b'{"CAMP":4294903808}')]:
            self.assertIsNone(problem(name,data))
    def test_private_files(self):
        for name in ['game.bin','game.gs0','disk.adf','disk.st','state.srm','archive.zip','frame.png','sound.wav','dump.asm','atlas38/Cyber-Cop_Atlas.html','atlas38/data.json','v36/st_items_pixels.json','amiga_research/maps.json']:
            self.assertIsNotNone(problem(name,b'innocent text'))
    def test_disguised_data(self):
        for name,data in [('x.py',b'\0'),('x.py',b'F'*4096),('v36/symbols.json',b'{"pixels":[1,2]}'),('x.md',b'data:image/png;base64,' + b'A'*256),('atlas38/template.html',b'data:image/png;base64,' + b'A'*256)]:
            self.assertIsNotNone(problem(name,data))
    def test_unsafe_paths(self):
        for name in ['../x.py','/x.py','upload/x.py','transfer_helpers/x.py']:
            self.assertIsNotNone(problem(name,b'pass'))

if __name__=='__main__':
    unittest.main()
