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
