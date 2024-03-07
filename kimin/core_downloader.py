import os, datetime, time, socket
from bs4 import BeautifulSoup as bs
from .core_config import Configurate
from urllib import request, error

class Driver:
	def __init__(kimin, **parameter):
		kimin.method, kimin.url, kimin.stream, kimin.timeout, kimin.header = parameter.get('method', 'GET'), parameter['url'], parameter.get('stream', False), parameter.get('timeout', 5), parameter.get('header', {})
	
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
			hasil['data'] = 'Timeout' if isinstance(e.reason, socket.timeout) else str(e)
		except Exception as e:
			hasil['header'], hasil['data'] = dict(respon.getheaders()), str(e)
		return hasil
	
	def _stream_response(kimin, respon):
		buffer_size, hasil, start = 4096, b'', time.time()
		while True:
			if time.time() - start > kimin.timeout:
				break
			data = respon.read(buffer_size)
			if not data:
				break
			hasil += data
		return hasil.decode('utf-8')
		
class Downloader(Configurate):
	def __init__(kimin, **parameter):
		kimin.parameter = parameter
		super().__init__(path="./kimin/config.min")
	
	def Get_Time(kimin, format="%H:%M:%S"):
		return datetime.datetime.now().strftime(format)
	
	def Get_Domain(kimin, link):
		return link.split("//")[-1].split("/")[0]
	
	def Mode_Parse(kimin, link):
		link = kimin.Get_Domain(link)
		return [i for i in kimin.Mode_Selection() if not link.find(kimin.Mode_Selection()[i]['url']) == -1][0]
	
	def Parse(kimin, data):
		return bs(data, kimin.Parse_Method())
	
	def Generate_Link(kimin, **parameter):
		data, hasil = kimin.Link_Extractor(parameter['mode']), None
		if 'parse' in data:
			if data['parse']:
				hasil = kimin.Parse(parameter['respon']).find(data['elemen'], attrs=data['attribute'])[data['extract']]
			else:
				if 'redirect' in data:
					domain, id_file = kimin.Get_Domain(parameter['link']), parameter['link'].split('/')[data['redirect']['id_file']]
					hasil = f"https://{data['redirect']['endpoint'].replace('{domain}', domain).replace('{id_file}', id_file)}"
		return hasil
	
	def Extract_Data(kimin, **parameter):
		cfg, respon = kimin.Data_Extraction(parameter['mode']), Driver(url=parameter['url']).Execute(mode='pre')
		hasil = {
			i:respon['header'][cfg[i]['data']] if 'header' in cfg[i] and cfg[i]['header'] else None
			for i in cfg}
		
		if not hasil['nama'] is None and 'split_by' in cfg['nama']:
			hasil['nama'] = hasil['nama'].split(cfg['nama']['split_by'])[cfg['nama']['split_index']].replace('"',"")
		if not hasil['size'] is None:
			hasil['size'] = int(hasil['size'])
		return hasil
	
	def Stream_Proses(kimin, respon, **parameter):
		buffer_size = kimin.Get_Buffer()
		with open(parameter['nama'], 'ab') as dataku:
			while True:
				temp = respon.read(buffer_size)
				if not temp:
					break
				dataku.write(temp)
				dataku.flush()
				os.fsync(dataku.fileno())
				print(f"\r[*][{kimin.Get_Time()}] Download progress: {os.path.getsize(parameter['nama']) / parameter['size'] * 100:.2f}% ({os.path.getsize(parameter['nama']):,} MB / {parameter['size']:,} MB)", end="\r")
		return b''
	
	def Download(kimin, *argument):
		data = kimin.Extract_Data(mode=argument[1], url=argument[0])
		print(data)
		if not os.path.exists(data['nama']):
			open(data['nama'], 'ab').close()
		size = os.path.getsize(data['nama'])
		headers = {'Range': f'bytes={size}-'}
		print(f"="*75)
		print(f"[*] Download Link : {argument[0]}\n[*] Media Download : {argument[1].capitalize()}\n[*] Nama File : {data['nama']}\n[*] Ukuran File : {data['size']/1024/1024} MB\n[*] Terdownload : {size/1024/1024} MB")
		print(f"="*75)
		try:
			respon = Driver(url=argument[0], header=headers, stream=True).Execute(mode='download')
			with request.urlopen(respon, timeout=5) as respon:
				kimin.Stream_Proses(respon, nama=data['nama'], size=data['size'])
			return True, None
		except error.URLError as e:
			return False, 'Timeout' if isinstance(e.reason, socket.timeout) else str(e)
		except Exception as e:
			return False, str(e)
		return True
	
	def Generate(kimin):
		data, mode, allowed_code = Driver(url=kimin.parameter['link']).Execute(mode='pre'), kimin.Mode_Parse(kimin.parameter['link']), [200, 201]
		if data['status'] and data['status_code'] in allowed_code:
			link = kimin.Generate_Link(link=kimin.parameter['link'], mode=mode, respon=data['data'])
			return link, mode
		return False, None
