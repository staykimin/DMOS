import json, os
def Get_Conf(path):
	if not os.path.exists(path):
		print(f"{Fore.RED}Config Tidak Ditemukan atau Kosong{Style.RESET_ALL}")
		return False
	else:
		with open(path, 'r', encoding='UTF-8') as dataku:
			data = json.loads(dataku.read())
		return data