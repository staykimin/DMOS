from flask import render_template, request, session, jsonify, url_for, redirect, session, abort, send_from_directory
from kimin.core_downloader import Downloader
from kimin.core_config import Configurate
import threading, queue, json, os

num_threads = int(input("Jumlah Thread : "))
download_queue = queue.Queue()
download_threads = []

def start_download():
	while True:
		link = download_queue.get()
		if link:
			print("Downloading:", link)
			sin = Downloader(link=link)
			data = sin.Generate()
			c =sin.Download(data[0], data[1])
			print(c)
			if c[0]:
				Configurate(path="./kimin/config.min").Add_Data(status='complete', data=link)
				print("Download Selesai Untuk : ", link)
			else:
				Configurate(path="./kimin/config.min").Add_Data(status='failed', data=link)
				print("Download Gagal Untuk : ", link)
		download_queue.task_done()

def start_download_threads(num_threads):
	global download_threads
	for _ in range(num_threads):
		thread = threading.Thread(target=start_download)
		thread.start()
		download_threads.append(thread)

def API():
	if request.method == "POST":
		download_queue.put(request.form['link'])
		if len(download_threads) < num_threads:
			start_download_threads(num_threads - len(download_threads))
		else:
			Configurate(path="./kimin/config.min").Add_Data(status='pending', data=request.form['link'])
			print("Download Pending Untuk : ", request.form['link'])
		return jsonify({'status': 'Proses Download Dimulai'}), 200
	
	elif request.method == "GET":
		with open("./tmp/api.min", "r", encoding="UTF-8") as dataku:
			data = json.loads(dataku.read())
		return data

def Proses():
	return render_template("hasil.html")