from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import select
from app import db
from app.main import main
from app.main.forms import BookForm
from app.models import Book, ReadingProgress, User

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

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_password = request.form.get('password')
        
        updated = False
        
        if new_username and new_username != current_user.username:
            user = db.session.scalar(select(User).where(User.username == new_username))
            if user:
                flash('Bu kullanıcı adı zaten kullanılıyor. Lütfen başka bir tane seçin.', 'danger')
                return redirect(url_for('main.profile'))
            current_user.username = new_username
            updated = True
            
        if new_password:
            current_user.set_password(new_password)
            updated = True
            
        if updated:
            db.session.commit()
            flash('Profil bilgileriniz başarıyla güncellendi!', 'success')
            return redirect(url_for('main.profile'))
            
    return render_template('main/profile.html')

@main.route('/explore')
@login_required
def explore():
    books = db.session.scalars(select(Book)).all()
    return render_template('main/explore.html', books=books)

@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
