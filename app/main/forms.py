from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class BookForm(FlaskForm):
    title = StringField('Kitap Adı', validators=[DataRequired()])
    author = StringField('Yazar', validators=[DataRequired()])
    total_pages = IntegerField('Toplam Sayfa', validators=[DataRequired(), NumberRange(min=1)])
    genre = StringField('Tür')
    series_name = StringField('Seri Adı (Opsiyonel)')
    volume_number = IntegerField('Cilt Numarası (Opsiyonel)', validators=[Optional(), NumberRange(min=1)])
    image_url = StringField('Kapak Resmi URL (Opsiyonel)')
    submit = SubmitField('Kitabı Ekle')
