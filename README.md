# BookCircle 📚

## Proje Açıklaması
Python ve Flask kullanılarak geliştirilmiş, kişisel kitap takibi ve dijital okuma kulübü altyapısı sunan modern bir web uygulaması.

## Özellikler
- Kullanıcı kaydı ve yetkilendirme (Flask-Login)
- Kitap ekleme, kapak resmi (URL) ve cilt/seri bilgisi desteği
- Okuma ilerlemesi takibi
- Güvenli form doğrulamaları (Validation)

## Kullanılan Teknolojiler
- Python
- Flask
- Flask-SQLAlchemy
- WTForms
- Bootstrap 5
- SQLite

## Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları sırasıyla terminal veya komut satırında (cmd/powershell) uygulayın:

1. **Projeyi Klonlayın:**
   ```bash
   git clone <proje-url>
   cd bookcircle
   ```

2. **Sanal Ortam (venv) Oluşturun ve Aktifleştirin:**
   ```bash
   python -m venv venv
   
   # Windows için:
   venv\Scripts\activate
   
   # macOS/Linux için:
   source venv/bin/activate
   ```

3. **Gerekli Kütüphaneleri Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Uygulamayı Başlatın:**
   ```bash
   python run.py
   ```

Tarayıcınızı açıp `http://127.0.0.1:5000` adresine giderek uygulamayı kullanmaya başlayabilirsiniz.
