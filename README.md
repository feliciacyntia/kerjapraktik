# Dashboard IPM vs P2 Jawa Barat (Streamlit)

IPM dan Indeks Keparahan Kemiskinan (P2) 27 kabupaten/kota Jawa Barat, 2020–2025 (sumber: BPS Jabar).

## Jalankan di komputer
```bash
pip install -r requirements.txt
streamlit run app.py
```
Buka http://localhost:8501

## Bagikan ke tim (gratis, Streamlit Community Cloud)
1. Unggah folder ini ke repo GitHub (boleh private): `app.py`, `requirements.txt`, `.streamlit/config.toml`, `data/master_ipm_p2_jabar_looker.csv`.
2. Masuk ke https://share.streamlit.io dengan akun GitHub → **Create app** → pilih repo, branch, file `app.py` → **Deploy**.
3. Di **Settings → Sharing**, pilih "Only specific people can view this app" lalu undang email rekan kerja, atau buat publik.

Edit: ubah `app.py` lalu push ke GitHub; aplikasi otomatis diperbarui.

## Ganti data
Timpa `data/master_ipm_p2_jabar_looker.csv` dengan file berstruktur kolom yang sama. Aplikasi memeriksa jumlah baris (162) dan 27 wilayah per tahun, dan menampilkan peringatan bila tidak sesuai.
