# -*- coding: utf-8 -*-
import xmlrpc.client


from 臺灣言語工具.翻譯.摩西工具.無編碼器 import 無編碼器
from 臺灣言語工具.基本元素.章 import 章
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.詞物件網仔 import 詞物件網仔
from 臺灣言語工具.基本元素.組 import 組
from 臺灣言語工具.基本元素.集 import 集
from 臺灣言語工具.基本元素.句 import 句
from 臺灣言語工具.基本元素.詞 import 詞


class 摩西用戶端():
    網址格式 = "http://{0}:{1}/{2}"
    未知詞記號 = '|UNK|UNK|UNK'

    def __init__(self, 位址='localhost', 埠='8080', 路徑='RPC2', 編碼器=無編碼器()):
        網址 = self.網址格式.format(位址, 埠, 路徑)
        self.主機 = xmlrpc.client.ServerProxy(網址)
        self.編碼器 = 編碼器

    def 翻譯(self, 物件):
        if isinstance(物件, 章):
            return self._翻譯章物件(物件)
        return self._翻譯句物件(物件)

    def _翻譯章物件(self, 來源章物件):
        結果章物件 = 章()
        來源新結構章物件 = 章()
        總分 = 0
        for 來源句物件 in 來源章物件.內底句:
            結果句物件, 來源新結構句物件, 分數 = self._翻譯句物件(來源句物件)
            結果章物件.內底句.append(結果句物件)
            來源新結構章物件.內底句.append(來源新結構句物件)
            總分 += 分數
        return 結果章物件, 來源新結構章物件, 總分

    def _翻譯句物件(self, 原本來源句物件):
        翻譯結果物件 = self._予摩西服務翻譯(原本來源句物件)
        結果詞物件陣列 = self._翻譯文本轉物件(翻譯結果物件['hyp'])
        結果對齊陣列, 來源對齊陣列 = self._對齊索引轉陣列(翻譯結果物件['align'], len(結果詞物件陣列))

        來源上後壁的位 = self._來源上後壁的位(來源對齊陣列)
        原本來源詞陣列 = 詞物件網仔.網出詞物件(原本來源句物件)
        self._加漏的詞物件(結果對齊陣列, 來源對齊陣列, 結果詞物件陣列, 原本來源詞陣列, 來源上後壁的位)

        結果句物件 = self._詞陣列照對齊轉句物件(結果詞物件陣列, 結果對齊陣列)
        來源新結構句物件 = self._詞陣列照對齊轉句物件(原本來源詞陣列, 來源對齊陣列)

        self._提對齊結果對組物件(結果句物件, 來源新結構句物件, 結果對齊陣列, 來源對齊陣列)
        return 結果句物件, 來源新結構句物件, 翻譯結果物件['totalScore']

    def _予摩西服務翻譯(self, 來源句物件):
        參數 = {
            "text": self.編碼器.編碼(物件譀鏡.看分詞(來源句物件).strip('｜\n\t ')),
            "align": "true",
            "report-all-factors": "true",
            'nbest': 1,
        }
        翻譯結果 = self.主機.translate(參數)
        return 翻譯結果['nbest'][0]

    def _翻譯文本轉物件(self, 翻譯文本):
        翻譯結果語句 = self.編碼器.解碼(翻譯文本)
        結果詞物件陣列 = []
        for 分詞 in 翻譯結果語句.split(' ')[:-1]:
            if 分詞 != '':
                if 分詞.endswith(self.未知詞記號):
                    詞物件 = 拆文分析器.轉做詞物件(分詞[:-len(self.未知詞記號)])
                    詞物件.屬性 = {'未知詞': True}
                else:
                    詞物件 = 拆文分析器.轉做詞物件(分詞)
                    詞物件.屬性 = {'未知詞': False}
                結果詞物件陣列.append(詞物件)
        return 結果詞物件陣列

    def _來源上後壁的位(self, 來源對齊陣列):
        來源上後壁的位 = 0
        for _頭, 尾 in 來源對齊陣列:
            if 來源上後壁的位 < 尾:
                來源上後壁的位 = 尾
        return 來源上後壁的位

    def _加漏的詞物件(self, 結果對齊陣列, 來源對齊陣列,
                結果詞物件陣列, 原本來源詞陣列, 來源上後壁的位):
        結果這馬位 = len(結果詞物件陣列)
        來源這馬位 = 來源上後壁的位
        for 詞物件 in 原本來源詞陣列[來源上後壁的位:]:
            結果詞物件陣列.append(詞(詞物件.內底字))
            結果對齊陣列.append((結果這馬位, 結果這馬位 + 1))
            結果這馬位 += 1
            來源對齊陣列.append((來源這馬位, 來源這馬位 + 1))
            來源這馬位 += 1
        return

    def _提對齊結果對組物件(self, 結果句物件, 來源新結構句物件, 結果對齊陣列, 來源對齊陣列):
        結果集陣列 = 結果句物件.內底集
        來源新結構集陣列 = 來源新結構句物件.內底集
        先後陣列 = self._取得來源詞先後(來源對齊陣列)
        for 結果集物件, 來源對齊 in zip(結果集陣列, 來源對齊陣列):
            來源頭 = 來源對齊[0]
            結果集物件.內底組[0].翻譯來源組物件 = 來源新結構集陣列[先後陣列[來源頭]].內底組[0]
            結果集物件.內底組[0].翻譯來源組物件.翻譯目標組物件 = 結果集物件.內底組[0]

    def _對齊索引轉陣列(self, 對齊索引陣列, 結果長度):
        結果陣列 = []
        來源陣列 = []
        頂一个結果 = 0
        for 對齊索引 in 對齊索引陣列:
            這个結果 = 對齊索引['tgt-start']
            結果陣列.append((頂一个結果, 這个結果))
            來源陣列.append((對齊索引['src-start'], 對齊索引['src-end'] + 1))
            頂一个結果 = 這个結果
        結果陣列.append((頂一个結果, 結果長度))
        return 結果陣列[1:], 來源陣列

    def _詞陣列照對齊轉句物件(self, 詞陣列, 對齊陣列):
        句物件 = 句()
        for 頭, 尾 in 對齊陣列:
            集物件 = 集()
            集物件.內底組.append(組(詞陣列[頭:尾]))
            if hasattr(詞陣列[頭], '屬性'):
                集物件.內底組[-1].屬性 = 詞陣列[頭].屬性
            句物件.內底集.append(集物件)
        return 句物件

    def _取得來源詞先後(self, 來源對齊陣列):
        先後陣列 = {}
        for 先後, (頭, _) in enumerate(來源對齊陣列):
            先後陣列[頭] = 先後
        return 先後陣列
