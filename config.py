import os

class Config:
    # Kunci rahasia untuk session dan CSRF (Ganti dengan string acak yang kuat di produksi)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-capstone-2024'
    
    # Konfigurasi Database SQLite
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASE_DIR, 'portfolio.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Konfigurasi Upload File
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # Maksimal 5 MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
