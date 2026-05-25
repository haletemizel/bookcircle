# BookCircle - Yapay Zeka (AI) Geliştirme Günlüğü

## Oturum 1: Proje İskeletinin Kurulması
- **Hedef:** Flask 3.x sürümüne uygun, Application Factory pattern ve Blueprint yapısını kullanan temel klasör hiyerarşisinin kurulması.
- **AI ile Etkileşim ve Karar Süreci:** Ajan, `templates`, `static` ve `migrations` klasörlerinin birer Python paketi olmadığını belirterek içlerine `__init__.py` koymayı ilk planda reddetti. Ancak ödev kılavuzundaki "Her klasörde bir __init__.py olmalı" kısıtını ajana hatırlatarak zorladım. Ajan planı revize etti ve kurallara tam uyumlu bir iskelet oluşturuldu. Altyapıyı körü körü onaylamayıp kılavuza göre yönlendirmenin önemini kavradım.

## Oturum 2: Veritabanı Modellerinin Tasarlanması
- **Hedef:** User, Book ve ReadingProgress (ilişkisel ara tablo) modellerinin SQLAlchemy kullanarak modellenmesi.
- **AI ile Etkileşim ve Karar Süreci:** Yapay zeka ajanlarının eski tip SQLAlchemy (1.x) kod blokları yazma eğilimini bildiğim için, ajana kesin bir kısıt vererek modern SQLAlchemy 2.x sözdizimini (`Mapped` ve `mapped_column`) kullanmasını istedim. Ayrıca güvenlik riski yaratmamak adına `User` modelinde şifrelerin düz metin yerine `werkzeug.security` ile hash'lenerek saklanması mantığını kurgulattım.

## Oturum 3: Veritabanı Migrasyonlarının Çalıştırılması
- **Hedef:** Yazılan modellerin Flask-Migrate araçları yardımıyla fiziksel SQLite veritabanına (`app.db`) aktarılması.
- **AI ile Etkileşim ve Karar Süreci:** `flask db init` komutunun temiz bir dizin istemesi sebebiyle, 1. oturumda açtığımız `migrations/__init__.py` dosyasının çakışma yaratacağını ajan fark etti ve o klasörü temizleyerek süreci yönetti. Ayrıca ilk migrasyon üretiminde Flask'ın modelleri görebilmesi için `create_app` factory fonksiyonu içerisine modellerin import edilmesi gerektiğini ajan başarıyla tespit edip koda yansıttı. Komutlar "Request Review" modunda adım adım onaylanarak `flask db upgrade` ile veritabanı başarıyla kilitlendi.

## Oturum 4: Kimlik Doğrulama (Auth) Altyapısı ve Formlar
- Hedef: Kullanıcı kayıt (Register) ve giriş (Login) işlemlerini yönetecek güvenli bir auth yapısı kurmak.
- AI ile Etkileşim ve Karar Süreci: Flask-WTF kullanarak CSRF korumalı form yapıları kurgulandı. Kayıt esnasında veritabanında mükerrer (aynı) kullanıcı adı veya e-posta adresi oluşmasını engelleyen özel veritabanı validator fonksiyonları (`validate_username`, `validate_email`) backend'e entegre edildi. Güvenlik kısıtlarına tam uyularak şifre doğrulama mantığı modeldeki hash yapısı üzerinden bağlandı.

## Oturum 5: Kitap Yönetimi ve Okuma Takip Backend Mantığı
- Hedef: Kullanıcıların kütüphanelerine kitap ekleyebileceği ve okuma ilerlemelerini güncelleyebileceği backend altyapısını kurmak.
- AI ile Etkileşim ve Karar Süreci: Kitap verilerini toplamak için `BookForm` sınıfı oluşturuldu. `main` blueprint'i altında `@login_required` ile korunan rotalar yazıldı. `/update-progress` rotasında, kullanıcının girdiği güncel sayfa sayısı eğer kitabın toplam sayfa sayısına eşitse, okuma durumunun otomatik olarak 'Bitti' şeklinde güncellenmesini sağlayan akıllı bir backend lojiği kurgulandı.

## Oturum 6: Docker Konteynerizasyon Altyapısı
- Hedef: Projenin her ortamda bağımsız, izole ve güvenli bir şekilde çalışabilmesi için Docker konfigürasyonunu tamamlamak.
- AI ile Etkileşim ve Karar Süreci: Sadece tekil bir Dockerfile yerine, dağıtım standartlarına uygun olarak `docker-compose` yapısı kuruldu. Flask'in yerleşik geliştirme sunucusu yerine, production (üretim) ortamları için güvenli ve performanslı olan `gunicorn` WSGI sunucusu tercih edildi. İmajın hafif kalması için `python:3.12-slim` taban imajı kullanıldı.

## Oturum 7: UI/UX Geliştirmeleri ve Görsel Modernizasyon
- Hedef: Yalın Bootstrap arayüzünü daha kullanıcı dostu, estetik ve modern bir tasarıma dönüştürmek.
- AI ile Etkileşim ve Karar Süreci: Şablonlara soft-shadows (hafif gölgeler), yuvarlatılmış köşeler (rounded-3, rounded-4) ve estetik renk paletleri entegre edildi. Navbar ve kart tasarımları premium bir görünüm için güncellendi, Inter fontu yerine daha yuvarlak hatlara sahip Poppins fontuna geçildi.

## Oturum 8: Özel Hata Sayfalarının Entegrasyonu
- Hedef: Kullanıcıların hatalı URL girdiklerinde veya sunucu kaynaklı pürüzlerde sistemde kalmasını sağlayacak şık hata sayfaları tasarlamak.
- AI ile Etkileşim ve Karar Süreci: Flask errorhandler dekoratörleri kullanılarak 404 ve 500 hataları yakalandı. `app/templates/errors/` altında base.html ile uyumlu iki yeni şablon oluşturuldu.

## Oturum 9: Kitap Silme (Delete) Backend Mantığının Kurulması
- Hedef: Kullanıcıların kütüphanelerindeki kitapları kalıcı olarak silebilmesi için güvenli bir backend rotası oluşturmak.
- AI ile Etkileşim ve Karar Süreci: `main` blueprint'i altında `@login_required` ile korunan `/delete-book/<int:book_id>` POST rotası kurgulandı. Ajanın kitabı veritabanında bırakıp sadece ilerleme kaydını silme önerisi reddedildi. Cascade delete mantığıyla kitabın tamamen silinmesi sağlandı.

## Oturum 10: Kitap Silme Arayüz Entegrasyonu
- Hedef: Kullanıcının kitaplığım sayfasından doğrudan silme işlemini tetikleyebilmesini sağlamak.
- AI ile Etkileşim ve Karar Süreci: `app/templates/main/index.html` içinde her kitabın alt kısmına Bootstrap standartlarına uygun, kırmızı renkli (`btn-outline-danger`) ve onay mekanizması (`confirm()`) içeren bir silme formu yerleştirildi.
