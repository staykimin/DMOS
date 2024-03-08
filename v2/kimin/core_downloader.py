import os, datetime, time, socket
from urllib import request, error
from bs4 import BeautifulSoup as bs
from .core_config import Configurate
from .core_driver import Driver

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
		link = [i for i in kimin.Mode_Selection() if not link.find(kimin.Mode_Selection()[i]['url']) == -1]
		return link[0] if len(link) > 0 else None
	
	def Parse(kimin, data):
		return bs(data, kimin.Parse_Method())
	
	def Generate_Link(kimin, **parameter):
		data, hasil = kimin.Link_Extractor(parameter['mode']), None
		if data is None:
			return kimin.parameter['link']
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
		if not cfg is None:
			hasil = {
				i:respon['header'][cfg[i]['data']] if 'header' in cfg[i] and cfg[i]['header'] else None
				for i in cfg}
		else:
			hasil = {}
			hasil['size'], hasil['nama'] = [respon['header'][i] for i in respon['header'] if i.lower() == 'content-length'], [respon['header'][i] for i in respon['header'] if i.lower() == 'content-disposition']
			hasil['size'], hasil['nama'] = int(hasil['size'][0]) if len(hasil['size']) > 0 else 0, hasil['nama'][0].split('filename=')[-1].replace('"',"") if len(hasil['nama']) > 0 else ""
			return hasil
	
		if not hasil['nama'] is None and 'split_by' in cfg['nama']:
			hasil['nama'] = hasil['nama'].split(cfg['nama']['split_by'])[cfg['nama']['split_index']].replace('"',"")
		
		if not hasil['size'] is None:
			hasil['size'] = int(hasil['size'])
		return hasil
	
	def Stream_Proses(kimin, respon, **parameter):
		buffer_size = kimin.Cfg_Driver()['split_size']
		no, start= 0, time.time()
		with open(parameter['nama'], 'ab') as dataku:
			while True:
				temp = respon.read(buffer_size)
				if not temp:
					break
				dataku.write(temp)
				dataku.flush()
				os.fsync(dataku.fileno())
				data = {
					"link":parameter['link'],
					"nama":parameter['nama'],
					"size":f"{int(parameter['size']) / (1024 * 1024):.2f} MB",
					"downloaded":f"{int(os.path.getsize(parameter['nama'])) / (1024 * 1024):.2f} MB",
					"progress":f"{os.path.getsize(parameter['nama']) / parameter['size'] * 100:.2f}%"
					}
				if no == 0 or time.time() - start >= 5:
					kimin.Add_Data(status='data', data=data)
					start = time.time()
				no += 1
		
		data = {
			"link":parameter['link'],
			"nama":parameter['nama'],
			"size":f"{int(parameter['size']) / (1024 * 1024):.2f} MB",
			"downloaded":f"{int(os.path.getsize(parameter['nama'])) / (1024 * 1024):.2f} MB",
			"progress":f"{os.path.getsize(parameter['nama']) / parameter['size'] * 100:.2f}%"
		}
		kimin.Add_Data(status='data', data=data)
		# print(f"\r[*][{kimin.Get_Time()}] Download progress: {os.path.getsize(parameter['nama']) / parameter['size'] * 100:.2f}% ({os.path.getsize(parameter['nama']):,} MB / {parameter['size']:,} MB)", end="\r")
		return b''
	
	def Download(kimin, *argument):
		data = kimin.Extract_Data(mode=argument[1], url=argument[0])
		if not data['nama'] == "" and data['size'] > 0:
			if not os.path.exists(data['nama']):
				open(data['nama'], 'ab').close()
			size = os.path.getsize(data['nama'])
			headers = {'Range': f'bytes={size}-'}
			try:
				respon = Driver(url=argument[0], header=headers, stream=True).Execute(mode='download')
				with request.urlopen(respon, timeout=kimin.Cfg_Driver()['timeout']) as respon:
					kimin.Stream_Proses(respon, nama=data['nama'], size=data['size'], link=argument[0])
				return True, None
			except error.URLError as e:
				return False, 'Timeout' if isinstance(e.reason, socket.timeout) else str(e)
			except Exception as e:
				return False, str(e)
		else:
			return False, None
		return True, None
	
	def Generate(kimin):
		data, mode, allowed_code = Driver(url=kimin.parameter['link']).Execute(mode='pre'), kimin.Mode_Parse(kimin.parameter['link']), [200, 201]
		if data['status_code'] in allowed_code:
			link = kimin.Generate_Link(link=kimin.parameter['link'], mode=mode, respon=data['data'])
			return link, mode
		return False, data