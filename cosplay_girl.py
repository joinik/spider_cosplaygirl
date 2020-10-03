




#1 真实的url地址（静态\动态）， 系统分析网页性质
import os

import parsel as parsel
from pip._vendor import requests

def down_img():
	"""下载cosplay文件"""

	for page in range(1,6):

		print("------正在爬取第{}页数据------".format(page))
		url = "http://www.win4000.com/meinvtag26_{}.html".format(page)
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}

		#2 发送网路请求（html\css<网页层叠样式表>js\....)
		response = requests.get(url=url, headers=headers)
		html_data = response.text
		# print(html_data)

		# 3 解析数据
		# 3.1 转换数据类型 xpath
		selector = parsel.Selector(html_data)

		# getall() 匹配到的所有数据 ，返回的是一个列表，
		data_list = selector.xpath('//div[@class="Left_bar"]//ul/li/a/@href').getall()
		print(data_list)

		for data in data_list:
			resp = requests.get(url=data, headers=headers).text
			sele = parsel.Selector(resp)
			# 获取图片系列，名字
			img_file_name = sele.xpath('//div[@class="ptitle"]/h1/text()').get()
			# print(img_name)
			img_url_list = sele.xpath('//ul[@id="scroll"]//li/a/@href').getall()
			# print(img_url_list)

			try:
				# 创建系列文件
				os.mkdir ("img/" + img_file_name)
				print(img_file_name)
				for img_url in img_url_list:
					resp = requests.get (url=img_url, headers=headers).text
					sele = parsel.Selector (resp)
					img_url_1 = sele.xpath('//div[@class="pic-meinv"]/a/img/@data-original').get()
					# print(img_url)
					# # 这里请求的是，图片数据，即为二进制数据，（音频，视频，）都是二进制
					img_data = requests.get(url=img_url_1, headers=headers).content
					#
					file_name = img_url_1.split("/")
					# print(file_name)

					with open("img/"+ img_file_name +"/" + file_name[-1], "wb") as f:
						f.write(img_data)
						print("保存完成", file_name[-1])

			except Exception as e:
				print(e)






if __name__ == '__main__':
	down_img()





