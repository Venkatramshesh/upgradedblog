from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField, CKEditor



##WTForm
class CreatecommentForm(FlaskForm):
    body = CKEditorField('Please leave any blog comments below. Thank you')
    name = StringField(label='FullName')
    submit = SubmitField(label='Submit Comment')
