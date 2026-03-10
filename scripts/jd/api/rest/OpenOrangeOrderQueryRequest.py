from jd.api.base import RestApi

class OpenOrangeOrderQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.request = None

		def getapiname(self):
			return 'jingdong.open.orange.order.query'

			
	

class Request(object):
		def __init__(self):
			"""
			"""
			self.pageIndex = None
			self.pageSize = None
			self.type = None
			self.startTime = None
			self.endTime = None





