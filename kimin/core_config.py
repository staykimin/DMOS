import json, os
class Configurate:
	def __init__(kimin, **parameter):
		kimin.config = kimin.Get_Config(parameter['path'])
	
	def Get_Config(kimin, path):
		with open(path, 'r', encoding='UTF-8') as dataku:
			config = json.loads(dataku.read())
		return config
	
	def Data_Extraction(kimin, mode):
		return kimin.config['extract_data'][mode]
	
	def Mode_Selection(kimin):
		return kimin.config['mode_selection']
	
	def Get_Buffer(kimin):
		return kimin.config['split_size']
	
	def Parse_Method(kimin):
		return kimin.config['parse_mode']
	
	def Link_Extractor(kimin, mode):
		return kimin.config['link_extractor'][mode]