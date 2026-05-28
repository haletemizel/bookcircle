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

## Oturum 11: Kitap Listesi İçin Pagination (Sayfalama) Entegrasyonu
- Hedef: Ana sayfada biriken kitapların performansı olumsuz etkilemesini önlemek amacıyla sayfa başına limit getirmek.
- AI ile Etkileşim ve Karar Süreci: Flask-SQLAlchemy'nin `.paginate()` fonksiyonu kullanılarak ana sayfa rotası güncellendi. Sayfa başına maksimum 5 kitap gösterilecek şekilde yapılandırma sağlandı.

## Oturum 12: Pagination (Sayfalama) Arayüz Elementlerinin Entegrasyonu
- Hedef: Kullanıcının ana sayfadaki kitap listesinde sayfalar arasında (Önceki/Sonraki) geçiş yapabilmesini sağlamak.
- AI ile Etkileşim ve Karar Süreci: app/templates/main/index.html şablonuna Bootstrap 5 standartlarına uygun, dinamik aktiflik durumuna sahip (disabled/active) sayfalama butonları entegre edildi.

## Oturum 13: Kullanıcı Profil Sayfası Backend Altyapısının Kurulması
- Hedef: Kullanıcının kendi profil bilgilerini görebileceği ve şifre/bilgi güncellemesi yapabileceği bir alan oluşturmak.
- AI ile Etkileşim ve Karar Süreci: app/main/routes.py dosyasına '@main.route("/profile", methods=["GET", "POST"])' rotası eklendi. Giriş yapmış kullanıcının bilgileri güvenli bir şekilde çekildi.

## Oturum 14: Profil Sayfası Tasarımı ve Üyelik Tarihi Rozetinin Eklenmesi
- Hedef: Kullanıcının profil bilgilerini görebileceği şık bir arayüz tasarlamak ve ek puan kriterlerine uygun olarak kayıt tarihini sergilemek.
- AI ile Etkileşim ve Karar Süreci: app/templates/main/profile.html şablonu oluşturuldu. Bootstrap 5 kart (Card) yapısı kullanılarak kullanıcı adı ve hakkında bilgileri listelendi; kullanıcının kayıt tarihini 'Member since...' formatında gösteren şık bir rozet (badge) entegre edildi.

## Oturum 15: Kitap Serileri İçin Veritabanı Güncellemesi
- Hedef: Kullanıcıların serilere ait kitapları (Örn: Yüzüklerin Efendisi - 1. Cilt) takip edebilmesi için veritabanı altyapısını kurmak.
- AI ile Etkileşim ve Karar Süreci: app/models.py dosyasındaki kitap veritabanı modeline 'series_name' (String) ve 'volume_number' (Integer) alanları eklendi. Değişiklikleri veritabanına yansıtmak için migration (göç) işlemi yapıldı.

## Oturum 16: Kitap Kapak Resmi (Image URL) Desteğinin Eklenmesi
- Hedef: Kullanıcıların kitaplara kapak resmi ekleyebilmesi için veritabanı ve form altyapısını güncellemek.
- AI ile Etkileşim ve Karar Süreci: app/models.py dosyasındaki Book modeline 'image_url' (String) kolonu eklendi. app/main/forms.py dosyasındaki kitap ekleme formuna bu alan dahil edildi. Değişiklikler Flask-Migrate ile veritabanına yansıtıldı.

## Oturum 17: Kitap Listesi Arayüzünün Modernize Edilmesi
- Hedef: Ana sayfadaki standart kitap listesini, kapak resimlerini ve seri bilgilerini içeren modern Bootstrap 5 kartlarına dönüştürmek.
- AI ile Etkileşim ve Karar Süreci: app/templates/main/index.html şablonu güncellendi. Kitaplar artık kapak resmi (image_url), seri adı/cilt numarası ve okuma ilerlemesini gösteren Bootstrap progress bar içeren şık bir Grid/Card yapısında listeleniyor.

## Oturum 18: Kitap Ekleme Formunun Güncellenmesi
- Hedef: Veritabanına eklenen 'Kapak Resmi' ve 'Kitap Serileri' özelliklerinin kullanıcı tarafından arayüz üzerinden girilebilmesini sağlamak.
- AI ile Etkileşim ve Karar Süreci: app/main/forms.py ve app/templates/main/add_book.html güncellenerek series_name, volume_number ve image_url alanları forma dahil edildi. app/main/routes.py dosyasındaki kayıt fonksiyonu bu verileri veritabanına aktaracak şekilde düzenlendi.

## Oturum 19: Form Veri Doğrulamalarının (Validation) Eklenmesi
- Hedef: Kullanıcıların sayfa sayılarına eksi (-) değer girmesini engellemek.
- Karar Süreci: app/main/forms.py dosyasındaki sayısal giriş alanlarına (Integer) WTForms'un NumberRange(min=0) doğrulayıcısı eklendi.

## Oturum 20: Birim Testlerinin (Unit Tests) Eklenmesi
- Hedef: Veritabanı modellerinin (User ve Book) doğru çalıştığını kanıtlayan otomatik testler yazmak.
- AI ile Etkileşim ve Karar Süreci: Proje kök dizininde 'tests' klasörü ve içine 'test_models.py' dosyası oluşturuldu. Kullanıcı şifreleme (password hashing) ve kitap ekleme senaryoları için unittest modülü kullanılarak temel test senaryoları yazıldı.
