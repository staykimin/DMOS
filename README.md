
# DMOS

<p align="center">
  <img width="25%" src="logo.png"/>
</p>
Download Manager Open Source Adalah Program Komputer Yang Dibuat Berdasarkan Prinsip Dasar Software IDM (Internet Download Manager) Yang Bisa Meresume / Melanjutkan Proses Download File Tanpa Harus Mengulangi Lagi Dari Awal.

## Support Download

- Mediafire
- Pixeldrain (Beta)


## Cara Penggunaan

Install Library Yang Dibutukan Dengan Cara :

**Windows**
```python
  pip install -r modul.min
```

**Linux**
```python
  pip3 install -r modul.min
```

Jalakan File **DMOS.py** dengan cara :


**Windows**
```python
   python DMOS.py
```

**Linux**
```python
   python3 DMOS.py
```
# Development & Costumize
Dalam DMOS Ini Mendukung Beberapa Fitur Kostumisasi Program Dengan Cara Mengedit Configurasi Pada File **/kimin/config.min**

## Config.min


Mengganti Teknik Parse Pada Halaman Download


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `parse_mode` | `string` | **Required**. Teknik Parsing Elemen Menggunakan bs4. Seperti : "html.parser" atau "xml"|

Mengubah Ukuran Split / Pembagian File Yang Akan Didownload


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `split_size`      | `integer` | **Required**. Pembagian File Akan Dibagi Menjadi Per Berapa Bytes |

#### Note : 1024 = 1 KB 


Menambahkan / Mengedit Beberapa Situs Yang Bisa Didownload

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `mode_selection` | `dict` | **Required**. Berisi *Key* Yang Berupa Nama Dari Situs  |
| `url` | `dict` | **Required**. Url Dari Situs Tanpa *https://* dan subdomain  |

#### Example : 
```json
    "mediafire":
	{
		"url":"mediafire.com"
	}
```

Mengubah Cara Extract Link Download Dari Tiap-Tiap Situs

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `link_extractor` | `dict` | **Required**. Berisi *Key* Yang Berupa Nama Dari Situs |
| `parse` | `boolean` | **Required**. Menetukan Apakah Perlu Dilakukan Parsing Atau Tidak |
| `elemen` | `boolean` | Menetukan Nama Elemen Apakah Yang Memuat Link Download Dari Situs |
| `attribute` | `dict` | Menetukan Attribute Apakah Yang Memuat Link Download Dari Sebuah Eleme. Menjadi **Required** jika *parse* = True |
| `extract` | `string` | Menetukan Attribute Apakah Yang Akan Kita Ambil. Mislanya *href*. Menjadi **Required** jika *parse* = True |
| `redirect` | `dict` | Menetukan Teknik Kombinasi Url Supaya Bisa Mendapatkan Link Download. Mislanya *domain+?id_file*. Menjadi **Required** jika *parse* = False |
| `id_file` | `integer` | Menetukan No Index ID File Dari Url. Menjadi **Required** jika *parse* = False |
| `endpoint` | `string` | Menetukan Url Akhir Ketika Sudah Mendapatkan *id_file*. Menjadi **Required** jika *parse* = False |

#### Example
```json
    "mediafire":
	{
		"parse":true,
		"elemen":"a",
		"attribute":{"id":"downloadButton"},
		"extract":"href"
	},
```

Mengubah Cara Extract Data Dari Tiap-Tiap Situs
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `extract_data` | `dict` | **Required**. Berisi *Key* Yang Berupa Nama Dari Situs |
| `size` | `dict` | **Required**. Untuk Mengambil Ukuran File |
| `header` | `boolean` | **Required**. Bernilai True Jika Data Yang Akan Dimabil Berada Di Header. Misalnya Ukuran File |
| `data` | `string` | **Required**. *Key* Dari Header Yang Di Extract |
| `split_by` | `string` | Berisi String Untuk Sebagai Pemisah Antar Data String |
| `split_index` | `integer` | Berisi Nomor Index Dari Data String Yang Sudah Di Pisah Dengan *split_by* |
| `nama` | `dict` | **Required**. Untuk Mengambil Nama File |
| `file_type` | `dict` | **Required**. Untuk Mengambil Type File |

#### Example
```json
    "mediafire":
	{
		"size":
			{
				"header":true,
				"data":"content-length"
			},
		"nama":
			{
				"header":true,
				"data":"content-disposition",
				"split_by":"filename=",
				"split_index":-1
			},
		"file_type":
			{
				"header":true,
				"data":"content-type"
			}
	},
```


## List Function

- Generate (Untuk Generate Link Download)
- Download (Untuk Download File)
- Stream_Proses (Untuk Membagi Split Download)
- Extract_Data (Untuk Extract Data Pada Link Download)
- Generate_Link (Untuk Mengextract Link Download Menggunakan Beberapa Teknik Sesuai Configurasi)
- Parse (Untuk Melakukan Parsing Data Menggunakan Beberapa Teknik Sesuai Configurasi)

## Authors

- [@staykimin](https://github.com/staykimin)

