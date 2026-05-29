from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

class BookForm(FlaskForm):
    title = StringField('Kitap Adı', validators=[DataRequired()])
    author = StringField('Yazar', validators=[DataRequired()])
    total_pages = IntegerField('Toplam Sayfa', validators=[DataRequired(), NumberRange(min=1)])
    genre = StringField('Tür')
    series_name = StringField('Seri Adı (Varsa)', validators=[Optional(), Length(max=140)])
    volume_number = IntegerField('Cilt/Kitap Numarası (Varsa)', validators=[Optional(), NumberRange(min=1)])
    image_url = StringField('Kapak Görseli URL', validators=[Optional(), Length(max=255)])
    summary = TextAreaField('Kitabın Konusu / Özeti', validators=[Optional(), Length(max=2000)])
    submit = SubmitField('Kitap Ekle')

class UpdateProfileForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=2, max=64)])
    about_me = TextAreaField('Hakkımda', validators=[Optional(), Length(max=500)])
    avatar = FileField('Profil Fotoğrafı Güncelle', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Güncelle')

class CreateClubForm(FlaskForm):
    name = StringField('Kulüp Adı', validators=[DataRequired(), Length(min=3, max=140)])
    description = StringField('Açıklama', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Kulüp Oluştur')

class ClubMessageForm(FlaskForm):
    body = StringField('Mesajınız', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Gönder')

class ReviewForm(FlaskForm):
    rating = SelectField('Puanınız', choices=[(5, '5 Yıldız'), (4, '4 Yıldız'), (3, '3 Yıldız'), (2, '2 Yıldız'), (1, '1 Yıldız')], coerce=int, validators=[DataRequired()])
    body = TextAreaField('Yorumunuz', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Değerlendir')
