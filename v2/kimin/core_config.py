import json, os
class Configurate:
	def __init__(kimin, **parameter):
		kimin.config = kimin.Get_Config(parameter['path'])
	
	def Get_Config(kimin, path):
		with open(path, 'r', encoding='UTF-8') as dataku:
			config = json.loads(dataku.read())
		return config
	
	def Data_Extraction(kimin, mode):
		return kimin.config['extract_data'].get(mode, None)
	
	def Get_Header(kimin, mode):
		return kimin.config['mode_selection'][mode].get('header', {})
	
	def Mode_Selection(kimin):
		return kimin.config['mode_selection']
	
	def Cfg_Driver(kimin):
		return kimin.config['driver']
	
	def Parse_Method(kimin):
		return kimin.config['parse_mode']
	
	def Add_Data(kimin, data, status, path="./tmp/api.min"):
		with open(path, 'r', encoding='UTF-8') as dataku:
			cfg = json.loads(dataku.read())
		tmp = [i['link'] for i in cfg['data']]
		if status == 'data':
			if data['link'] in tmp:
				cfg['data'][tmp.index(data['link'])] = data
			else:
				cfg['data'].append(data)
			
			if data['link'] in cfg['pending']:
				cfg['pending'] = [i for i in cfg['pending'] if not i == data['link']]
			
			if data['link'] in cfg['failed']:
				cfg['failed'] = [i for i in cfg['failed'] if not i == data['link']]
		
		else:
			cfg[status].append(data)
			if status == 'pending' or status == 'failed':
				if not data in tmp:
					cfg['data'].append({"link":data, "size":0, "downloaded":0, "progress":"0.00%", "nama":""})
			
		with open(path, 'w', encoding='UTF-8') as dataku:
			json.dump(cfg, dataku, indent=4)
	
	def Link_Extractor(kimin, mode):
		return kimin.config['link_extractor'][mode] if mode in kimin.config['link_extractor'] else None