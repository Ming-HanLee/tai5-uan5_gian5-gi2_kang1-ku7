# -*- coding: utf-8 -*-
"""
著作權所有 (C) 民國102年 意傳文化科技
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
import unittest
from 臺灣言語工具.語音合成.句物件轉合成標仔 import 句物件轉合成標仔
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.音標系統.客話.臺灣客家話拼音 import 臺灣客家話拼音
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私

class 句物件轉合成標仔試驗(unittest.TestCase):
	def setUp(self):
		self.合成標籤工具 = 句物件轉合成標仔()
		self.分析器 = 拆文分析器()
		self.家私 = 轉物件音家私()
	def tearDown(self):
		pass

	def test_臺灣閩南語羅馬字拼音(self):
		# [我 gua2, 愛 ai3, 蔡 tsʰua3, 文 bun5, 莉 ni7, , ,]
		句物件 = self.分析器.產生對齊句('gua2 ai3 tshua3-bun5-le7', 'gua1 ai2 tshua2-bun7-le7',)
		音值句物件 = self.家私.轉音(臺灣閩南語羅馬字拼音, 句物件, 函式='音值')
		完整標仔 = self.合成標籤工具.句物件轉標仔(音值句物件)
		self.檢驗標仔有對無(完整標仔,
			['x-sil+x/調:x<x>x/詞:x!x@x/句:x^x_x/驗:',
			'sil-g+ua/調:x<1>2/詞:0!1@1/句:0^3_3/驗:',
			'g-ua+ʔ/調:x<1>2/詞:0!1@1/句:0^3_3/驗:',
			'ua-ʔ+ai/調:1<2>2/詞:0!1@1/句:1^2_3/驗:',
			'ʔ-ai+tsʰ/調:1<2>2/詞:0!1@1/句:1^2_3/驗:',
			'ai-tsʰ+ua/調:2<2>7/詞:0!3@3/句:2^1_3/驗:',
			'tsʰ-ua+b/調:2<2>7/詞:0!3@3/句:2^1_3/驗:',
			'ua-b+un/調:2<7>7/詞:1!2@3/句:2^1_3/驗:',
			'b-un+l/調:2<7>7/詞:1!2@3/句:2^1_3/驗:',
			'un-l+e/調:7<7>x/詞:2!1@3/句:2^1_3/驗:',
			'l-e+sil/調:7<7>x/詞:2!1@3/句:2^1_3/驗:',
			'x-sil+x/調:x<x>x/詞:x!x@x/句:x^x_x/驗:', ]
			)
		音值標仔 = self.合成標籤工具.提出標仔主要音值(完整標仔)
		self.檢驗標仔有對無(音值標仔,
			['sil/驗:',
			'g/驗:',
			'ua/驗:',
			'ʔ/驗:',
			'ai/驗:',
			'tsʰ/驗:',
			'ua/驗:',
			'b/驗:',
			'un/驗:',
			'l/驗:',
			'e/驗:',
			'sil/驗:', ]
			)

	def test_臺灣客家話拼音(self):
		句物件 = self.分析器.產生對齊句('tienˊ-dangˋ labˋ-suiˋ', 'tienˊ-dangˋ labˋ-suiˋ')
		音值句物件 = self.家私.轉音(臺灣客家話拼音, 句物件, 函式='音值')
		完整標仔 = self.合成標籤工具.句物件轉標仔(音值句物件)
		self.檢驗標仔有對無(完整標仔,
			['x-sil+x/調:x<x>x/詞:x!x@x/句:x^x_x/驗:',
			'sil-t+ien/調:x<ˊ>ˋ/詞:0!2@2/句:0^2_2/驗:',
			't-ien+d/調:x<ˊ>ˋ/詞:0!2@2/句:0^2_2/驗:',
			'ien-d+ang/調:ˊ<ˋ>ˋ/詞:1!1@2/句:0^2_2/驗:',
			'd-ang+l/調:ˊ<ˋ>ˋ/詞:1!1@2/句:0^2_2/驗:',
			'ang-l+ab/調:ˋ<ˋ>ˋ/詞:0!2@2/句:1^1_2/驗:',
			'l-ab+s/調:ˋ<ˋ>ˋ/詞:0!2@2/句:1^1_2/驗:',
			'ab-s+ui/調:ˋ<ˋ>x/詞:1!1@2/句:1^1_2/驗:',
			's-ui+sil/調:ˋ<ˋ>x/詞:1!1@2/句:1^1_2/驗:',
			'x-sil+x/調:x<x>x/詞:x!x@x/句:x^x_x/驗:', ]
			)
		音值標仔 = self.合成標籤工具.提出標仔主要音值(完整標仔)
		self.檢驗標仔有對無(音值標仔,
			['sil/驗:',
			't/驗:',
			'ien/驗:',
			'd/驗:',
			'ang/驗:',
			'l/驗:',
			'ab/驗:',
			's/驗:',
			'ui/驗:',
			'sil/驗:', ]
			)
	def 檢驗標仔有對無(self, 結果, 答案):
		for 結, 答 in zip(結果, 答案):
			self.assertEqual(結[:len(答)], 答, (結, 答))
		
