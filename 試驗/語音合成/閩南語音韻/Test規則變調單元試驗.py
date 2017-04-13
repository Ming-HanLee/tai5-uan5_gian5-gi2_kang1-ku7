# -*- coding: utf-8 -*-
from unittest.case import TestCase
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from 臺灣言語工具.語音合成.閩南語音韻.變調.規則變調 import 規則變調


class 規則變調單元試驗(TestCase):

    def test_規則變調(self):
        原本 = ('s', 'ui', '2')
        變調了 = ('s', 'ui', '1')
        self.assertEqual(規則變調.變調(原本), 變調了)

    def test_喉入聲(self):
        原本 = ('kh', 'ah', '4')
        變調了 = ('kh', 'a', '2')
        self.assertEqual(規則變調.變調(原本), 變調了)

    def test_ptk入聲(self):
        原本 = ('k', 'ut', '8')
        變調了 = ('k', 'ut', '10')
        self.assertEqual(規則變調.變調(原本), 變調了)

    def test_無合法的音標愛錯誤(self):
        with self.assertRaises(解析錯誤):
            規則變調.變調(('g', 'ua', '0'))
        with self.assertRaises(解析錯誤):
            規則變調.變調(('g', 'ua', '4'))
        with self.assertRaises(解析錯誤):
            規則變調.變調(('g', 'uah', '2'))
        with self.assertRaises(解析錯誤):
            規則變調.變調(('g', 'uat', '2'))
