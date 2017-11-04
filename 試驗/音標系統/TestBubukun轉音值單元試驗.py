from unittest.case import TestCase, skip
from 臺灣言語工具.音標系統.Bunun.Bubukun import Bubukun


class Bubukun轉音值單元試驗(TestCase):

    @skip('長元音的性質猶未確定')
    def test_單元音(self):
        self.assertEqual(
            Bubukun("baak").音值(),
            [['b', 'aː', 'k']]
        )

    def test_雙元音(self):
        self.assertEqual(
            Bubukun("mais").音值(),
            [['m', 'a', 'i', 's']]
        )

    def test_雙音節短元音(self):
        self.assertEqual(
            Bubukun("tuza").音值(),
            [['t', 'u'], ['ð', 'a']]
        )

    @skip('長元音的性質猶未確定')
    def test_雙音節長元音(self):
        self.assertEqual(
            Bubukun("tuzaa").音值(),
            [['t', 'u'], ['ð', 'aː']]
        )

    def test_補喉入聲(self):
        self.assertEqual(
            Bubukun("adasun").音值(),
            [['ʔ', 'a'], ['d', 'a'], ['s', 'u', 'n']]
        )

    def test_元音分開(self):
        self.assertEqual(
            Bubukun("a-apnum").音值(),
            [['ʔ', 'a'], ['a', 'p'], ['n', 'u', 'm']]
        )

    @skip('長元音的性質猶未確定')
    def test_音節分開(self):
        self.assertEqual(
            Bubukun("cinus-uvaazan").音值(),
            [['ts', 'i'], ['n', 'u', 's'], ['u'], ['v', 'aː'], ['ð', 'a', 'n']]
        )

    def test_預設音標就是家己(self):
        self.assertEqual(Bubukun("iskaan").預設音標(), 'iskaan')

    def test_無合法(self):
        拼音 = Bubukun("iskaan！")
        self.assertIsNone(拼音.音標)
        self.assertEqual(拼音.音值(), [])
