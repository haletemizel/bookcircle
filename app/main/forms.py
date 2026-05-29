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
