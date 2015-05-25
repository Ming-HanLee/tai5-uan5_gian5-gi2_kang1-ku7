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
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
import re

class 用戶端連線:
	檢查結果 = re.compile('<result>(.*)</result>')
	檢查空結果 = re.compile('<result/>')
	分句 = re.compile('<sentence>(.*?)</sentence>')
	回傳狀況 = re.compile('<processstatus code="\d">(.*?)</processstatus>')
	傳去格式 = '''
<?xml version="1.0" ?>
<wordsegmentation version="0.1" charsetcode='{}' >
<option showcategory="1" />
<authentication username="{}" password="{}" />
<text>{}</text>
</wordsegmentation>
'''
	def 連線(self, 語句, 編碼, 等待, 主機, 連接埠, 帳號, 密碼):
		連線 = socket(
			AF_INET, SOCK_STREAM)
		連線.settimeout(等待)
		try:
			連線.connect((主機, 連接埠))
		except:
			raise RuntimeError("連線逾時")
		資料 = self.傳去格式.format(編碼, 帳號, 密碼, 語句).encode(編碼)
# 		print('送出', 資料)
		已經送出去 = 0
		while 已經送出去 < len(資料):
			這擺送出去 = 連線.send(資料[已經送出去:])
			if 這擺送出去 == 0:
				raise RuntimeError("連線出問題")
			已經送出去 += 這擺送出去
		全部收著資料 = b''
		走 = True
		while 走:
			這擺收著資料 = 連線.recv(1024)
			if 這擺收著資料 == b'':
				raise RuntimeError("連線出問題")
			全部收著資料 = 全部收著資料 + 這擺收著資料
			if b'</wordsegmentation>' in 全部收著資料:
				走 = False
		連線.close()
		全部收著字串 = 全部收著資料.decode(編碼)
# 		print('收著', 全部收著字串)
		收著結果 = self.檢查結果.search(全部收著字串)
		if 收著結果 != None:
			逐逝 = self.分句.split(收著結果.group(1))[1::2]
			return 逐逝
		if self.檢查空結果.search(全部收著字串) != None:
			return []
		狀況 = self.回傳狀況.split(全部收著字串)
		if 狀況 != None:
# 			<processstatus code="1">Service internal error</processstatus>
# 			<processstatus code="2">XML format error</processstatus>
# 			<processstatus code="3">Authentication failed</processstatus>
			raise RuntimeError(狀況[1])
		raise RuntimeError('回傳的資料有問題！！')
