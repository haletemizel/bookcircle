from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

class BookForm(FlaskForm):
    title = StringField('Kitap Adı', validators=[DataRequired()])
    author = StringField('Yazar', validators=[DataRequired()])
    total_pages = IntegerField('Toplam Sayfa', validators=[DataRequired(), NumberRange(min=1)])
    genre = StringField('Tür')
    series_name = StringField('Seri Adı (Opsiyonel)')
    volume_number = IntegerField('Cilt Numarası (Opsiyonel)', validators=[Optional(), NumberRange(min=1)])
    image_url = StringField('Kapak Resmi URL (Opsiyonel)')
    submit = SubmitField('Kitabı Ekle')

class UpdateProfileForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=2, max=64)])
    avatar = FileField('Profil Fotoğrafı Güncelle', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Güncelle')

class CreateClubForm(FlaskForm):
    name = StringField('Kulüp Adı', validators=[DataRequired(), Length(min=3, max=140)])
    description = StringField('Açıklama', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Kulüp Oluştur')

class ClubMessageForm(FlaskForm):
    body = StringField('Mesajınız', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Gönder')
