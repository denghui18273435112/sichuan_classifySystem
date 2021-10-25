import requests
from tools.logUtil import my_log


#重构requests库中的post方法、get方法  使用中
class RequestsUtil:

	def __init__(self):
		self.log = my_log("自定义封装")

	def request_api(self,url,headers=None,data=None,json=None,cookies=None,method="get"):
		"""
		:param url: 必传
		:param headers: 默认不传
		:param data: 默认不传
		:param json: 默认不传
		:param cookies: 默认不传
		:param method: 默认为get
		:return:  res字典由code和body组成
		#status_code获取状态码
		"""
		if method=="get":
			self.log.debug("发送get请求")
			r = requests.get(url=url,headers=headers,data=data,cookies=cookies)
		elif method=="post":
			self.log.debug("发送post请求")
			r = requests.post(url=url,headers=headers,data=data,json=json,cookies=cookies)
		try:
			body = r.json()
		except Exception as e:
			body = r.text
		res =dict()
		res["code"] = r.status_code
		res["body"] = body
		return res

	def get(self,url,**kwargs):
		"""
		:param url:  接口地址
		:param kwargs: 不定参数: *args和**kwargs 可以接受任意长度和格式的参数；两个参数不能同时传，一次只能传一个
		:return: 调用request_api方法,method默认为get,并且传入随意参数;request_api方法支持headers,data,json,cookies
		"""
		return self.request_api(url,method="get",**kwargs)

	def post(self,url,**kwargs):
		"""
		:param url:  接口地址
		:param kwargs: 不定参数: *args和**kwargs 可以接受任意长度和格式的参数；两个参数不能同时传，一次只能传一个
		:return: 调用request_api方法,method默认为post,并且传入随意参数;request_api方法支持headers,data,json,cookies
		"""
		return self.request_api(url,method="post",**kwargs)


	def run_api(self,url,method,params=None,header=None,cookie=None):
			"""
			发送请求api
			:return:
			"""
			if len(str(params).strip()) is not 0:
				params = json.loads(params)
			if str(method).lower() == "get":
				res = RequestsUtil.get(url, json=params, headers=header, cookies=cookie)
			elif str(method).lower() == "post":
				res = RequestsUtil.post(url, json=params, headers=header, cookies=cookie)
			else:
				my_log().error("错误请求method: %s" % method)
			return res



if __name__ == '__main__':
	# url = ConfigYaml().get_conf_url()+"/authorizations/"
	# data = {"username":"python","password":"12345678"}
	# print(Request().post(url=url,data=data))

	headers ={"Host":"<calculated when request is sent>",
			  "User-Agent":"PostmanRuntime/7.26.8",
			  "Accept":"*/*",
			  "Accept-Encoding":"gzip, deflate, br",
			  "Connection":"keep-alive",
			  "Cookie":"lang=zh-cn; device=desktop; theme=default; lastProject=1; lastProduct=1; lastTaskModule=0; preProductID=1; preBranch=0; bugModule=0; bugBranch=0; treeBranch=0; qaBugOrder=id_desc; zentaosid=7o6sngqg9mp01dmhmg38m3d6i1",
			  "Postman-Token":"<calculated when request is sent>"}
	url ="http://tp.sichuan.giiatop.com/manageapi/membertrainingtest/VerifyCodeImg"
	data = {"h":"40",
			"w":"128",
			"f":"20",
			"rnd":"0.46250044537312074"}
	r = requests.get(url=url,data=data,)
	new_dict = r.cookies.get_dict()
	print(new_dict["zzlvcode"])


