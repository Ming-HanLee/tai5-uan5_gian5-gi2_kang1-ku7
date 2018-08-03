# -*- coding: utf-8 -*-
from unittest.case import TestCase
from 臺灣言語工具.羅馬字.台語 import 新白話字


class 新白話字單元試驗(TestCase):

    def test_白話字(self):
        self.assertIsNotNone(新白話字('chhō͘').音標)

    def test_臺羅(self):
        self.assertIsNotNone(新白話字('tshō͘').音標)

    def test_違法(self):
        self.assertIsNone(新白話字('cō͘').音標)
