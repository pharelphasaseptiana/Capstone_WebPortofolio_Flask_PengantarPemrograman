# Portofolio Flask — Capstone Project

Aplikasi portofolio pribadi berbasis Flask dengan dashboard admin untuk
mengelola proyek, profil, dan pesan masuk dari pengunjung.

## Fitur

- Halaman publik: Beranda, Tentang (dengan pendidikan & skill), Portofolio,
  Detail Proyek, Kontak (email, GitHub, LinkedIn)
- Dashboard admin (login diperlukan):
  - CRUD Proyek (tambah, edit, hapus) dengan upload gambar dan link GitHub/Live
  - Edit Profil (nama, headline, about, pendidikan, email, GitHub, LinkedIn) & daftar Skill
  - Kotak Masuk pesan (tandai dibaca, hapus)
- Autentikasi session dengan hashing password (Werkzeug)
- Validasi upload file: ekstensi gambar saja, maksimal 5 MB

## Struktur Proyek

```
app.py              # Entry point, routing, dan konfigurasi Flask
config.py           # Konfigurasi (SECRET_KEY, database, upload)
models.py           # Model SQLAlchemy: User, Profile, Skill, Project, Message
portfolio.db         # Database SQLite
requirements.txt     # Dependensi Python
templates/           # Template Jinja2 (halaman publik + dashboard)
static/              # CSS, JS, dan file upload gambar
```

## Instalasi & Menjalankan

```bash
pip install -r requirements.txt
python app.py
```

Buka browser di `http://localhost:5000`.

> **Penting:** jika sebelumnya sudah pernah menjalankan versi lama project ini,
> hapus dulu file `portfolio.db` yang lama sebelum menjalankan versi ini, karena
> ada kolom baru (`education` pada tabel Profile) yang tidak akan otomatis
> ditambahkan oleh `db.create_all()` ke database lama.

**Akun admin default:**
- Username: `admin`
- Password: `admin123`

> Ganti password default dan `SECRET_KEY` sebelum digunakan di produksi.

## Teknologi

- Flask 3.0
- Flask-SQLAlchemy 3.1
- Werkzeug 3.0 (hashing password & keamanan upload file)
- SQLite
