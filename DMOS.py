from kimin.core_downloader import Downloader

link = input("Masukkan Link : ")
sin = Downloader(link=link)
data = sin.Generate()
print(data)
if not data[0] is False:
	if sin.Download(data[0], data[1]):
		print("Download Berhasil")
	else:
		print("Download Gagal")


