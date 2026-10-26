<div align="center">

# 📊 IPM vs Kemiskinan Jawa Barat

**Dashboard interaktif Indeks Pembangunan Manusia (IPM) dan Indeks Keparahan Kemiskinan (P2)**
**27 kabupaten/kota Jawa Barat · 2020–2025**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.24%2B-3F4F75?logo=plotly&logoColor=white)
![Data](https://img.shields.io/badge/Data-BPS%20Jawa%20Barat-0F766E)

*Apakah IPM yang tinggi berarti kemiskinan yang lebih ringan? Wilayah mana yang tertinggal?*

[Fitur](#-fitur) · [Mulai cepat](#-mulai-cepat) · [Deploy & bagikan](#-deploy--bagikan-ke-tim) · [Data](#-data) · [Metodologi](#-metodologi) · [Kustomisasi](#-kustomisasi) · [FAQ](#-pemecahan-masalah)

</div>

---

## 🎯 Tentang

Dashboard ini menjawab tiga pertanyaan:

1. **Bagaimana kondisi dan tren** IPM dan P2 di setiap kabupaten/kota sejak 2020?
2. **Wilayah mana yang tertinggal**, yaitu yang IPM-nya di bawah rata-rata *sekaligus* P2-nya di atas rata-rata?
3. **Apakah IPM tinggi berhubungan dengan P2 rendah?** Jawabannya dilihat lewat korelasi yang dihitung langsung dari data.

> **Cara membaca indikator**
> 📈 **IPM**: makin **tinggi** makin baik (kesehatan, pendidikan, daya beli).
> 📉 **P2**: makin **rendah** makin baik (ketimpangan pengeluaran di antara penduduk miskin).
> Karena arahnya berlawanan, warna penanda perubahan P2 **dibalik**: P2 turun berwarna 🟢, P2 naik berwarna 🔴.

### Temuan utama dari data

| Tahun | Rata-rata IPM* | Rata-rata P2* | Korelasi IPM–P2 (r) | Wilayah tertinggal ganda |
|:-----:|:--------------:|:-------------:|:-------------------:|:------------------------:|
| 2020 | 72.51 | 0.24 | −0.26 | 9 |
| 2021 | 72.81 | 0.37 | −0.39 | 7 |
| 2022 | 73.48 | 0.34 | −0.41 | 9 |
| 2023 | 74.11 | 0.28 | −0.58 | 9 |
| 2024 | 74.68 | 0.28 | −0.53 | 10 |
| 2025 | 75.50 | 0.24 | −0.65 | 10 |

<sub>*Rata-rata sederhana 27 kab/kota, <b>bukan angka resmi</b> Provinsi Jawa Barat.</sub>

Hubungan IPM–P2 **selalu negatif dan cenderung menguat**: wilayah ber-IPM tinggi umumnya punya kemiskinan yang lebih ringan. Hubungan ini tidak berlaku untuk semua wilayah, dan **korelasi bukan sebab-akibat**.

---

## ✨ Fitur

| | Komponen | Pertanyaan yang dijawab |
|---|---|---|
| 🧭 | **Ringkasan otomatis** | Kalimat kesimpulan yang ikut berubah sesuai tahun yang dipilih |
| 🎛️ | **Filter tahun & kab/kota** | Tahun default **2025**; memilih wilayah akan menyorotnya di semua grafik |
| 🔢 | **4 kartu KPI** | IPM, P2 (dengan perubahan tahunan), korelasi r, dan jumlah/status wilayah tertinggal |
| 🗺️ | **Peta interaktif** | *Di mana wilayah yang tertinggal?* Warna bisa diganti: Status / IPM / P2 |
| 🔵 | **Diagram sebar + garis tren** | *Apakah IPM tinggi beriringan dengan P2 rendah?* Ada kuadran dan rata-rata Jabar |
| ▶️ | **Animasi 2020–2025** | Lihat pergerakan tiap wilayah dari tahun ke tahun |
| 📊 | **Korelasi per tahun** | *Apakah hubungannya makin kuat dari tahun ke tahun?* |
| 📈 | **Tren IPM & P2** | *Apakah semua wilayah membaik?* Selalu menampilkan **semua tahun** |
| 📋 | **Tabel peringkat** | Bisa diurutkan dan dicari, dengan bar, Δ berwarna, dan status |
| ⬇️ | **Unduh CSV** | Data tahun yang sedang dipilih |
| ✅ | **Cek data otomatis** | Peringatan jika jumlah baris ≠ 162 atau wilayah per tahun ≠ 27 |

**Interaksi:** klik titik di peta, diagram sebar, atau garis tren untuk menyorot wilayah. Klik sekali lagi untuk membatalkan.

<!-- Tambahkan tangkapan layar setelah aplikasi berjalan:
![Tampilan dashboard](docs/screenshot.png)
-->

---

## 🚀 Mulai cepat

**Prasyarat:** Python 3.10 atau lebih baru.

```bash
# 1. Masuk ke folder proyek
cd streamlit_ipm_p2

# 2. (Disarankan) buat virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Pasang dependensi
pip install -r requirements.txt

# 4. Jalankan
streamlit run app.py
```

Aplikasi akan terbuka di **http://localhost:8501**.

---

## ☁️ Deploy & bagikan ke tim

### Opsi A: Streamlit Community Cloud (gratis, disarankan)

1. **Unggah ke GitHub.** Buat repo baru (boleh *private*) lalu push seluruh isi folder ini:
   ```bash
   git init
   git add .
   git commit -m "Dashboard IPM vs P2 Jabar"
   git branch -M main
   git remote add origin https://github.com/<akun-anda>/<nama-repo>.git
   git push -u origin main
   ```
2. **Deploy.** Buka [share.streamlit.io](https://share.streamlit.io), masuk dengan GitHub, pilih **Create app**, lalu pilih repo, branch `main`, dan file `app.py`. Klik **Deploy**.
3. **Bagikan.** Di **Settings → Sharing**:
   - 🔒 *Only specific people can view this app*: undang email rekan kerja satu per satu, atau
   - 🌐 *Public*: siapa pun yang punya link bisa melihat.

### Opsi B: Server internal kantor

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Setelah itu aplikasi bisa diakses dari jaringan kantor di `http://<ip-server>:8501`.

### Mengedit setelah dibagikan

Edit `app.py` atau ganti file data, lalu `git push`. Aplikasi di Community Cloud akan **memperbarui dirinya sendiri** dalam beberapa detik.

---

## 📁 Struktur proyek

```
streamlit_ipm_p2/
├── app.py                              # Seluruh aplikasi (data, perhitungan, tampilan)
├── requirements.txt                    # Dependensi Python
├── README.md                           # Dokumen ini
├── .streamlit/
│   └── config.toml                     # Tema (warna, latar, font)
└── data/
    └── master_ipm_p2_jabar_looker.csv  # Data sumber (162 baris)
```

---

## 🗂️ Data

**Sumber:** BPS Provinsi Jawa Barat, IPM dan Indeks Keparahan Kemiskinan (P2) menurut kabupaten/kota.
**Cakupan:** 27 kabupaten/kota × 6 tahun (2020–2025) = **162 baris**.

<details>
<summary><b>Kamus kolom</b> (klik untuk membuka)</summary>

| Kolom | Keterangan |
|---|---|
| `kode_kabupaten_kota` | Kode wilayah BPS (mis. `3201`) |
| `nama_label` | Nama wilayah (mis. `Kab. Bogor`, `Kota Bandung`) |
| `tipe` | `Kabupaten` / `Kota` |
| `tahun`, `tanggal` | Tahun data dan tanggal (`YYYYMMDD`) |
| `ipm` | Indeks Pembangunan Manusia |
| `p2` | Indeks Keparahan Kemiskinan |
| `kategori_ipm` | Rendah / Sedang / Tinggi / Sangat Tinggi |
| `ipm_yoy`, `p2_yoy` | Perubahan dari tahun sebelumnya (**kosong di 2020**, tampil sebagai `n/a`) |
| `rank_ipm` | Peringkat IPM (1 = tertinggi) |
| `rank_p2` | Peringkat P2 (1 = paling parah) |
| `ipm_rata2_jabar`, `p2_rata2_jabar` | Rata-rata sederhana 27 kab/kota pada tahun itu |
| `ipm_jabar_yoy`, `p2_jabar_yoy` | Perubahan rata-rata Jabar dari tahun sebelumnya |
| `koordinat` | `"lat,lon"` dalam satu teks; dipisah otomatis oleh aplikasi |

</details>

### Memperbarui data

Timpa `data/master_ipm_p2_jabar_looker.csv` dengan file baru yang **nama kolomnya sama**. Tahun baru akan muncul otomatis di filter. Jika file tidak ditemukan, aplikasi menampilkan tombol unggah CSV.

> ℹ️ Pemeriksaan otomatis mengharapkan 162 baris dan 27 wilayah per tahun. Jika Anda menambah tahun, ubah angka 162 di fungsi `validate()` di `app.py`.

---

## 🧮 Metodologi

| Ukuran | Cara hitung |
|---|---|
| **Rata-rata Jabar** | Diambil dari kolom file: rata-rata **sederhana** 27 kab/kota, tidak dibobot jumlah penduduk. **Bukan angka resmi BPS** untuk Provinsi Jawa Barat. |
| **Korelasi (r)** | Korelasi Pearson antara IPM dan P2 dari 27 wilayah, dihitung **per tahun** |
| **Garis tren** | Regresi linear P2 terhadap IPM per tahun (`numpy.polyfit`) |
| **Kekuatan korelasi** | \|r\| < 0.2 sangat lemah · < 0.4 lemah · < 0.6 sedang · < 0.8 kuat · ≥ 0.8 sangat kuat |

**Status wilayah** (dibanding rata-rata Jabar pada tahun yang sama):

| Status | Kriteria | Warna |
|---|---|:---:|
| **Unggul** | IPM ≥ rata-rata **dan** P2 ≤ rata-rata | 🟢 |
| **Waspada kemiskinan** | IPM ≥ rata-rata **dan** P2 > rata-rata | 🟠 |
| **Kejar IPM** | IPM < rata-rata **dan** P2 ≤ rata-rata | 🔵 |
| **Tertinggal ganda** | IPM < rata-rata **dan** P2 > rata-rata | 🔴 |

> ⚠️ **Korelasi bukan sebab-akibat.** IPM dan P2 bisa sama-sama dipengaruhi faktor lain seperti urbanisasi, struktur ekonomi, atau akses layanan. Dengan hanya 27 wilayah, satu-dua wilayah ekstrem dapat menggeser nilai r.

> 📍 Titik pada peta adalah **koordinat pusat perkiraan** tiap wilayah, bukan batas administratif.

---

## 🎨 Kustomisasi

Semua pengaturan utama ada di bagian atas `app.py`:

```python
DEFAULT_YEAR = 2025          # tahun yang dipilih saat aplikasi dibuka
IPM_C = "#2563EB"            # warna IPM (biru)
P2_C  = "#DC2626"            # warna P2 (merah)
STATUS_COLORS = { ... }      # warna tiap status wilayah
```

| Ingin mengubah… | Lokasi |
|---|---|
| Warna tema & latar | `.streamlit/config.toml` |
| Gaya kartu, hero, font | blok `<style>` di awal `app.py` |
| Batas status wilayah | fungsi `load_data()` (`np.select`) |
| Batas kekuatan korelasi | fungsi `strength()` |
| Gaya peta dasar | `map=dict(style="carto-positron", ...)`; bisa diganti `"carto-darkmatter"` atau `"open-street-map"` |

---

## 🛠️ Pemecahan masalah

<details>
<summary><b><code>AttributeError: module 'streamlit' has no attribute 'segmented_control'</code></b></summary>

Versi Streamlit terlalu lama. Perbarui dengan `pip install -U "streamlit>=1.40"`.
</details>

<details>
<summary><b><code>AttributeError: ... 'Scattermap'</code></b> atau peta kosong</summary>

Versi Plotly terlalu lama. Perbarui dengan `pip install -U "plotly>=5.24"`. Peta dasar juga butuh koneksi internet.
</details>

<details>
<summary><b><code>AttributeError: 'Styler' object has no attribute 'map'</code></b></summary>

Versi pandas di bawah 2.1. Perbarui dengan `pip install -U "pandas>=2.1"`.
</details>

<details>
<summary><b>Muncul peringatan "Cek data: …"</b></summary>

Jumlah baris atau jumlah wilayah per tahun di CSV tidak sesuai harapan. Periksa apakah ada baris yang hilang atau ganda untuk kombinasi wilayah–tahun yang sama.
</details>

<details>
<summary><b>Klik titik di grafik tidak menyorot wilayah</b></summary>

Fitur ini butuh Streamlit 1.35 atau lebih baru. Jika tetap tidak berfungsi, gunakan menu **Kabupaten/kota** di bagian atas.
</details>

---

## 📄 Sumber & catatan

- **Data:** [BPS Provinsi Jawa Barat](https://jabar.bps.go.id), diolah dari `master_ipm_p2_jabar_looker.csv`.
- Rata-rata Jabar dalam dashboard ini adalah **rata-rata sederhana 27 kab/kota**, bukan angka resmi BPS.
- Dibuat dengan [Streamlit](https://streamlit.io) dan [Plotly](https://plotly.com/python/).
