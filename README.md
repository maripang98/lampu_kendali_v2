# 🚦 Lampu Kendali

Game pengendalian diri berbasis lampu merah-kuning-hijau untuk kegiatan kTB.

## Cara Deploy ke Streamlit Cloud (gratis)

1. **Upload ke GitHub**
   - Buat repo baru di github.com
   - Upload `app.py` dan `requirements.txt`

2. **Deploy di Streamlit Cloud**
   - Buka [share.streamlit.io](https://share.streamlit.io)
   - Login dengan GitHub
   - Klik **"New app"** → pilih repo kamu → pilih `app.py`
   - Klik **Deploy**
   - Kamu dapat link seperti: `https://nama-app.streamlit.app`

3. **Share linknya ke peserta** — selesai! 🎉

---

## Cara Jalankan Lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Kustomisasi

Edit di `app.py`:
- `SITUASI` — daftar situasi yang muncul (tambah/ubah bebas)
- `TIMER = 3` — durasi timer dalam detik
