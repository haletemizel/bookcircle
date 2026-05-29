import os
import secrets
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, request, current_app, jsonify, session
from flask_login import login_required, current_user
from sqlalchemy import select, func
from app import db
from app.main import main
from app.models import Book, ReadingProgress, User, BookClub, ClubMessage, Review
from app.main.forms import BookForm, UpdateProfileForm, CreateClubForm, ClubMessageForm, ReviewForm

@main.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['tr', 'en']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))

@main.app_context_processor
def inject_dict():
    translations = {
        'tr': {
            'explore': 'Keşfet',
            'my_library': 'Kitaplığım',
            'add_book': 'Kitap Ekle',
            'profile': 'Profilim',
            'logout': 'Çıkış Yap',
            'login': 'Giriş Yap',
            'register': 'Kayıt Ol',
            'search_placeholder': 'Kitap veya yazar ara...',
            'search_btn': 'Ara',
            'welcome': 'BookCircle\'a Hoş Geldiniz! 📚',
            'hero_desc': 'Kişisel kütüphanenizi dijitalleştirin, okuma hedeflerinizi takip edin ve yeni kitaplar keşfedin.',
            'hero_start': 'Hemen Başla',
            'hero_library': 'Kitaplığına Git',
            'my_books': 'Kitaplarım',
            'no_books': 'Kitaplığınızda henüz kitap yok.',
            'no_books_sub': 'Okuduğunuz veya okumak istediğiniz kitapları eklemeye başlayın.',
            'add_first_book': 'İlk Kitabı Ekle',
            'clubs': 'Kulüpler'
        },
        'en': {
            'explore': 'Explore',
            'my_library': 'My Library',
            'add_book': 'Add Book',
            'profile': 'My Profile',
            'logout': 'Log Out',
            'login': 'Log In',
            'register': 'Register',
            'search_placeholder': 'Search books or authors...',
            'search_btn': 'Search',
            'welcome': 'Welcome to BookCircle! 📚',
            'hero_desc': 'Digitize your personal library, track your reading goals, and discover new books.',
            'hero_start': 'Get Started',
            'hero_library': 'Go to Library',
            'my_books': 'My Books',
            'no_books': 'No books in your library yet.',
            'no_books_sub': 'Start adding books you have read or want to read.',
            'add_first_book': 'Add First Book',
            'clubs': 'Clubs'
        }
    }
    lang = session.get('lang', 'tr')
    return dict(t=translations.get(lang, translations['tr']), current_lang=lang)

@main.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    progresses = db.paginate(
        select(ReadingProgress).where(ReadingProgress.user_id == current_user.id),
        page=page,
        per_page=5,
        error_out=False
    )
    return render_template('main/index.html', progresses=progresses)

@main.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        # Kitap mevcut mu diye kontrol et
        book = db.session.scalar(
            select(Book).where(
                (Book.title == form.title.data) & (Book.author == form.author.data)
            )
        )
        if not book:
            book = Book(
                title=form.title.data, 
                author=form.author.data, 
                total_pages=form.total_pages.data, 
                genre=form.genre.data,
                series_name=form.series_name.data,
                volume_number=form.volume_number.data,
                image_url=form.image_url.data
            )
            db.session.add(book)
            db.session.commit()
            
        # Kullanıcının bu kitabı önceden ekleyip eklemediğini kontrol et
        progress = db.session.scalar(
            select(ReadingProgress).where(
                (ReadingProgress.user_id == current_user.id) & 
                (ReadingProgress.book_id == book.id)
            )
        )
        if not progress:
            new_progress = ReadingProgress(user_id=current_user.id, book_id=book.id, current_page=0, status="Okunuyor")
            db.session.add(new_progress)
            db.session.commit()
            flash('Kitap kütüphanenize başarıyla eklendi!', 'success')
        else:
            flash('Bu kitap zaten kütüphanenizde mevcut.', 'info')
            
        return redirect(url_for('main.index'))
    return render_template('main/add_book.html', form=form)

@main.route('/update-progress/<int:progress_id>', methods=['POST'])
@login_required
def update_progress(progress_id):
    progress = db.session.get(ReadingProgress, progress_id)
    if progress and progress.user_id == current_user.id:
        current_page_data = request.form.get('current_page', type=int)
        if current_page_data is not None:
            progress.current_page = current_page_data
            # Okuma tamamlandıysa durumu güncelle
            if progress.current_page >= progress.book.total_pages:
                progress.current_page = progress.book.total_pages
                progress.status = "Bitti"
            db.session.commit()
            flash('Okuma ilerlemeniz güncellendi!', 'success')
        else:
            flash('Geçersiz sayfa numarası.', 'danger')
    else:
        flash('Böyle bir kayıt bulunamadı veya yetkiniz yok.', 'danger')
    return redirect(url_for('main.index'))

@main.route('/delete-book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = db.session.get(Book, book_id)
    if book:
        # O anki kullanıcının bu kitabı okuyup okumadığını kontrol et
        progress = db.session.scalar(
            select(ReadingProgress).where(
                (ReadingProgress.user_id == current_user.id) & 
                (ReadingProgress.book_id == book.id)
            )
        )
        if progress:
            # Cascade delete etkisini sağlamak için kitaba bağlı tüm progress kayıtlarını siliyoruz
            all_progresses = db.session.scalars(
                select(ReadingProgress).where(ReadingProgress.book_id == book.id)
            ).all()
            for p in all_progresses:
                db.session.delete(p)
            
            # Ana kitap nesnesini sil
            db.session.delete(book)
            db.session.commit()
            flash('Kitap başarıyla silindi!', 'success')
        else:
            flash('Bu kitabı silme yetkiniz yok.', 'danger')
    else:
        flash('Silinmek istenen kitap bulunamadı.', 'danger')
    return redirect(url_for('main.index'))

def save_avatar(form_avatar):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_avatar.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img/avatars', picture_fn)
    
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    form_avatar.save(picture_path)
    return picture_fn

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.username.data != current_user.username:
            user = db.session.scalar(select(User).where(User.username == form.username.data))
            if user:
                flash('Bu kullanıcı adı zaten kullanılıyor. Lütfen başka bir tane seçin.', 'danger')
                return redirect(url_for('main.profile'))
            current_user.username = form.username.data
            
        if form.avatar.data:
            avatar_file = save_avatar(form.avatar.data)
            current_user.avatar_file = avatar_file
            
        db.session.commit()
        flash('Profil bilgileriniz başarıyla güncellendi!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        
    image_file = url_for('static', filename='img/avatars/' + current_user.avatar_file)
    return render_template('main/profile.html', form=form, image_file=image_file)

@main.route('/search')
@login_required
def search():
    q = request.args.get('q', '')
    if not q:
        return redirect(url_for('main.index'))
    
    # Kitap Adı veya Yazar alanında büyük/küçük harf duyarsız arama
    books = db.session.scalars(
        select(Book).where(
            (Book.title.ilike(f'%{q}%')) | (Book.author.ilike(f'%{q}%'))
        )
    ).all()
    
    return render_template('main/search_results.html', books=books, query=q)

@main.route('/explore')
@login_required
def explore():
    books = db.session.scalars(select(Book)).all()
    
    # Haftanın Kitabı (En yüksek puanlı veya rastgele 1 kitap)
    featured_book = db.session.scalar(
        select(Book)
        .outerjoin(Review)
        .group_by(Book.id)
        .order_by(func.avg(Review.rating).desc())
        .limit(1)
    )
    if not featured_book:
        featured_book = db.session.scalar(select(Book).order_by(func.random()).limit(1))
        
    return render_template('main/explore.html', books=books, featured_book=featured_book)

@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@main.route('/api/v1/books', methods=['GET'])
def api_get_books():
    books = db.session.scalars(select(Book)).all()
    books_list = []
    for book in books:
        books_list.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'total_pages': book.total_pages,
            'genre': book.genre,
            'series_name': book.series_name,
            'volume_number': book.volume_number,
            'image_url': book.image_url
        })
    return jsonify({'books': books_list, 'count': len(books_list)})

@main.route('/clubs', methods=['GET', 'POST'])
@login_required
def clubs():
    form = CreateClubForm()
    if form.validate_on_submit():
        club = BookClub(name=form.name.data, description=form.description.data, creator_id=current_user.id)
        club.members.append(current_user)
        db.session.add(club)
        try:
            db.session.commit()
            flash('Yeni kitap kulübü başarıyla oluşturuldu!', 'success')
            return redirect(url_for('main.clubs'))
        except Exception:
            db.session.rollback()
            flash('Bu kulüp adı zaten kullanılıyor olabilir.', 'danger')
    
    all_clubs = db.session.scalars(select(BookClub).order_by(BookClub.created_at.desc())).all()
    popular_clubs = sorted(all_clubs, key=lambda c: len(c.members), reverse=True)[:3]
    return render_template('main/clubs.html', clubs=all_clubs, popular_clubs=popular_clubs, form=form)

@main.route('/join_club/<int:club_id>', methods=['POST'])
@login_required
def join_club(club_id):
    club = db.session.get(BookClub, club_id)
    if not club:
        flash('Kulüp bulunamadı.', 'danger')
        return redirect(url_for('main.clubs'))
    
    if current_user not in club.members:
        club.members.append(current_user)
        db.session.commit()
        flash(f'{club.name} kulübüne katıldınız!', 'success')
    return redirect(url_for('main.club_room', club_id=club.id))

@main.route('/club/<int:club_id>', methods=['GET', 'POST'])
@login_required
def club_room(club_id):
    club = db.session.get(BookClub, club_id)
    if not club:
        flash('Kulüp bulunamadı.', 'danger')
        return redirect(url_for('main.clubs'))
        
    if current_user not in club.members:
        flash('Bu kulübün odasına girmek için önce katılmalısınız.', 'warning')
        return redirect(url_for('main.clubs'))

    form = ClubMessageForm()
    if form.validate_on_submit():
        msg = ClubMessage(body=form.body.data, user_id=current_user.id, club_id=club.id)
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for('main.club_room', club_id=club.id))
        
    messages = db.session.scalars(
        select(ClubMessage).where(ClubMessage.club_id == club.id).order_by(ClubMessage.timestamp)
    ).all()
    
    return render_template('main/club_room.html', club=club, messages=messages, form=form)

@main.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_detail(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        flash('Kitap bulunamadı.', 'danger')
        return redirect(url_for('main.explore'))
        
    form = ReviewForm()
    if form.validate_on_submit():
        existing = db.session.scalar(select(Review).where((Review.book_id == book.id) & (Review.user_id == current_user.id)))
        if existing:
            existing.rating = form.rating.data
            existing.body = form.body.data
            flash('Yorumunuz başarıyla güncellendi.', 'success')
        else:
            review = Review(rating=form.rating.data, body=form.body.data, user_id=current_user.id, book_id=book.id)
            db.session.add(review)
            flash('Değerlendirmeniz başarıyla eklendi.', 'success')
        db.session.commit()
        return redirect(url_for('main.book_detail', book_id=book.id))
        
    reviews = db.session.scalars(select(Review).where(Review.book_id == book.id).order_by(Review.timestamp.desc())).all()
    avg_rating = db.session.scalar(select(func.avg(Review.rating)).where(Review.book_id == book.id))
    avg_rating = round(avg_rating, 1) if avg_rating else None
    
    return render_template('main/book_detail.html', book=book, reviews=reviews, avg_rating=avg_rating, form=form)
