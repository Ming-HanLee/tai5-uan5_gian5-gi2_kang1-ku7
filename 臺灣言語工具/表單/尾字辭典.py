# -*- coding: utf-8 -*-
"""
著作權所有 (C) 民國103年 意傳文化科技
開發者：薛丞宏
網址：http://意傳.台灣
語料來源：請看各資料庫內說明

本程式乃自由軟體，您必須遵照SocialCalc設計的通用公共授權（Common Public Attribution License, CPAL)來修改和重新發佈這一程式，詳情請參閱條文。授權大略如下，若有歧異，以授權原文為主：
	１．得使用、修改、複製並發佈此程式碼，且必須以通用公共授權發行；
	２．任何以程式碼衍生的執行檔或網路服務，必須公開該程式碼；
	３．將此程式的原始碼當函式庫引用入商業軟體，且不需公開非關此函式庫的任何程式碼

此開放原始碼、共享軟體或說明文件之使用或散佈不負擔保責任，並拒絕負擔因使用上述軟體或說明文件所致任何及一切賠償責任或損害。

臺灣言語工具緣起於本土文化推廣與傳承，非常歡迎各界用於商業軟體，但希望在使用之餘，能夠提供建議、錯誤回報或修補，回饋給這塊土地。

感謝您的使用與推廣～～勞力！承蒙！
"""
from 臺灣言語工具.基本元素.詞 import 詞

def _詞物件反過來(詞物件):
	反過來詞物件 = 詞()
	反過來詞物件.內底字 = 詞物件.內底字[::-1]
	if hasattr(詞物件, '屬性'):
		反過來詞物件.屬性 = 詞物件.屬性
	return 反過來詞物件

def _加詞(self, 詞物件):
	return super(self.__class__, self).加詞(_詞物件反過來(詞物件))
	
def _頭字查詞(self, 詞物件):
	return super(self.__class__, self).查詞(詞物件)

def _詞組合反過來(結果陣列):
	反過來結果陣列 = []
	for 結果 in 結果陣列:
		反過來結果 = set()
		for 一个詞 in 結果:
			反過來結果.add(_詞物件反過來(一个詞))
		反過來結果陣列.append(反過來結果)
	return 反過來結果陣列

def _尾字查詞(self, 詞物件):
	結果陣列 = self.頭字查詞(_詞物件反過來(詞物件))
	return _詞組合反過來(結果陣列)

def _揣詞查詞(self, 詞物件):
	結果陣列 = self.頭字查詞(詞物件)
	return _詞組合反過來(結果陣列)
	
def 尾字辭典(辭典類):
	return type('尾字{0}'.format(辭典類.__class__),
		(辭典類,), {'加詞':_加詞, '查詞':_尾字查詞,
			'頭字查詞':_頭字查詞, '尾字查詞':_尾字查詞, '揣詞查詞':_揣詞查詞})
