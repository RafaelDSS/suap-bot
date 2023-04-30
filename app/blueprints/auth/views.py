from flask import Blueprint, render_template, flash, current_app, redirect
from sqlalchemy.exc import IntegrityError

from app.bot.suap_wrapper.main import SuapApi
from app.bot.handlers.helpers import get_payload_from_token
from app.extensions.database import db
from app.models.forms import LoginForm
from app.models.tables import TelegramUser

app_auth = Blueprint("auth", __name__)


@app_auth.route("/auth/<validation_token>", methods=["GET", "POST"])
def index(validation_token=None):
    form = LoginForm()
    try:
        payload = get_payload_from_token(
            validation_token, current_app.config["SECRET_KEY"]
        )
    except:
        flash("Token inválido.")

    if form.validate_on_submit():
        suap = SuapApi(registration=form.username.data, password=form.password.data)
        try:
            token = suap.get_token_user()
        except:
            flash("Por favor, entre com um usuário e senha corretos. Note que ambos os campos diferenciam maiúsculas e minúsculas.")
            return render_template("auth/login.html", form=form)

        user = TelegramUser.query.filter_by(telegram_chat_id=payload['chat_id']).first()
        if not user:
            new_user = TelegramUser(telegram_chat_id=payload['chat_id'], suap_token=token)
            db.session.add(new_user)
        else:
            user.suap_token = token
        db.session.commit()

        current_app.bot.edit_message_text(
            chat_id=payload['chat_id'],
            message_id=payload['message_id'],
            text="Login feito com sucesso."
        )
        return redirect("https://t.me/suapifba_bot")
    return render_template("auth/login.html", form=form)


def init_app(app):
    app.register_blueprint(app_auth)
