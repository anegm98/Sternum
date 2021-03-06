import unittest
import glob
from kmer import kmer_maker
from decode import decoder


class testKmer(unittest.TestCase):

    def test_splice_fasta_overlapping(self):
        """
        Test splicing fasta overlapping kmers
        """
        fileName = "data/KR233687.fasta"
        fastaFile = decoder(fileName)
        kmer = kmer_maker(13, fastaFile, True)
        self.assertIn(["GAGATCTAATGTC", 0], kmer.kmers["KR233687.2.1"])
        self.assertIn(["TAATGGTGGCATA", 579], kmer.kmers["KR233687.2.1"])
        self.assertIn(["ATTCAGTTGATAG", 1], kmer.kmers["KR233687.2.2"])
        self.assertIn(["ATGGTCATCAATT", 1123], kmer.kmers["KR233687.2.2"])
        self.assertEqual(2, kmer.seqCount)

    def test_splice_fasta_Nonoverlapping(self):
        """
        Test splicing fasta nonoverlapping kmers
        """
        fileName = "data/KR233687.fasta"
        fastaFile = decoder(fileName)
        kmer = kmer_maker(13, fastaFile, False)
        self.assertIn(["GAGATCTAATGTC", 0], kmer.kmers["KR233687.2.1"])
        self.assertIn(["TCAATCCCGCACT", 13], kmer.kmers["KR233687.2.1"])
        self.assertIn(["TTCGGATGGTCAT", 1118], kmer.kmers["KR233687.2.2"])
        self.assertNotIn(["AGATCTAATGTCT", 1], kmer.kmers["KR233687.2.1"])
        self.assertEqual(2, kmer.seqCount)

    def test_splice_fastq_overlapping(self):
        """
        Test splicing fastq overlapping kmers
        """
        fileName = "data/ERR1293055_first100.fastq"
        fastaFile = decoder(fileName)
        kmer = kmer_maker(13, fastaFile, True)
        self.assertIn(["TCCTCTTTCTTTC", 33], kmer.kmers["ERR1293055.5"])
        self.assertIn(["GTTGGGATCAATA", 0], kmer.kmers["ERR1293055.40"])
        self.assertIn(["CTCTTCTACTTCT", 0], kmer.kmers["ERR1293055.1"])
        self.assertIn(["TCAAATGTTCCTT", 288], kmer.kmers["ERR1293055.100"])
        self.assertEqual(100, kmer.seqCount)

    def test_splice_fastq_Nonoverlapping(self):
        """
        Test splicing fastq nonoverlapping kmers
        """
        fileName = "data/ERR1293055_first100.fastq"
        fastaFile = decoder(fileName)
        kmer = kmer_maker(13, fastaFile, False)
        self.assertIn(["CTCTTCTACTTCT", 0], kmer.kmers["ERR1293055.1"])
        self.assertIn(["GTTGGGATCAATA", 0], kmer.kmers["ERR1293055.40"])
        self.assertIn(["ATTCAAATGTTCC", 286], kmer.kmers["ERR1293055.100"])
        self.assertNotIn("TCCACTTCACTTT", kmer.kmers["ERR1293055.90"])
        self.assertEqual(100, kmer.seqCount)

    def test_dump(self):
        """
        Test storing kmers to disk
        """
        fileName = "data/ERR1293055_first100.fastq"
        fastaFile = decoder(fileName)
        kmer = kmer_maker(13, fastaFile, False)
        kmer.dump()
        file = open("_39_ERR1293055.40.kmers")
        lines = file.read()
        self.assertIn("GTTGGGATCAATA", lines)
        file.close()

    def test_load(self):
        """
        Test storing kmers to disk
        """
        fileName = "data/ERR1293055_first100.fastq"
        fastaFile = decoder(fileName)
        kmer = kmer_maker(13, fastaFile, False)
        kmer.dump()
        kmer.load("", 3)
        self.assertIn("ERR1293055.3", kmer.kmers)
        kmer.dump()
        kmer.load("", 4)
        self.assertIn("ERR1293055.7", kmer.kmers)
        kmer.load("", -1)
        self.assertIn("ERR1293055.100", kmer.kmers)

    def test_zclear(self):
        """
        Test deleting kmers' files from disk
        """
        fileName = "data/ERR1293055_first100.fastq"
        fastaFile = decoder(fileName)
        kmer = kmer_maker(13, fastaFile, False)
        kmer.dump()
        kmer.clear()
        files = glob.glob(kmer.filePrefix+"_*"+kmer.fileExten)
        self.assertEqual(dict(), kmer.kmers)
        self.assertEqual(files, [])


if __name__ == '__main__':
    unittest.main()
