import unittest
import os
from reporter import reporter
from tests.test_mapper import initiate_case


class testReporter(unittest.TestCase):

    def test_file_maker(self):
        """
        Test mapping case with no batches
        """
        sternum = initiate_case(-1)
        reporter(sternum)
        file = open("ERR1293055.sam")
        line = file.readline()
        file.close()
        self.assertIn("ERR1293055.19\t0\tKR233687.2.1\t728\t255\t*\t*\t0\
\tCTGGCGGAGAAGTGAGAAAT", line)
        os.remove("ERR1293055.sam")


if __name__ == '__main__':
    unittest.main()
