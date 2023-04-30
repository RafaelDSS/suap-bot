from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, ValidationError

from app.bot.suap_wrapper.main import SuapApi


class LoginForm(FlaskForm):
    username = StringField("Matrícula:", validators=[InputRequired()])
    password = PasswordField("Senha:", validators=[InputRequired()])
    submit = SubmitField("Acessar")

    # def validation_submit(form, field):
    #     suap = SuapApi(registration=form.username.data, password=form.password.data)

    #     try:
    #         token = suap.get_token_user()
    #     except:
    #         flash("Houve algum problema com a autenticação no SUAP.")
