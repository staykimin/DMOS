from urllib import request, error
from .core_config import Configurate
import time, socket

class Driver(Configurate):
	def __init__(kimin, **parameter):
		super().__init__(path="./kimin/config.min")
		kimin.method, kimin.url, kimin.stream, kimin.timeout, kimin.header = parameter.get('method', 'GET'), parameter['url'], parameter.get('stream', False), parameter.get('timeout', kimin.Cfg_Driver()['timeout']), parameter.get('header', {})
		
	
	def Execute(kimin, mode='pre'):
		hasil = {'status':False}
		try:
			respon = request.Request(kimin.url, headers=kimin.header, method=kimin.method)
			if mode == 'pre':
				with request.urlopen(respon, timeout=kimin.timeout) as respon:
					hasil['status'], hasil['data'], hasil['status_code'], hasil['header'] = True, kimin._stream_response(respon), respon.status, dict(respon.getheaders())
			else:
				return respon
		except error.URLError as e:
			hasil['data'], hasil['status_code'] = 'Timeout' if isinstance(e.reason, socket.timeout) else str(e), respon.status
		except Exception as e:
			hasil['header'], hasil['data'], hasil['status_code'] = dict(respon.getheaders()), str(e), respon.status
		return hasil
	
	def _stream_response(kimin, respon):
		buffer_size, hasil, start = kimin.Cfg_Driver()['buffer'], b'', time.time()
		while True:
			if time.time() - start > kimin.timeout:
				break
			data = respon.read(buffer_size)
			if not data:
				break
			hasil += data
		return hasil.decode('utf-8')