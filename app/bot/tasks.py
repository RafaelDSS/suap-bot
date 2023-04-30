from app.extensions.celery import celery_app
from app.bot.suap_wrapper.main import SuapApi
from app.extensions.database import db
from app.models.tables import TelegramUser


@celery_app.task
def update_suap_tokens():
    telegram_user = TelegramUser.query.all()

    for user in telegram_user:
        suap_api = SuapApi(token=user.suap_token)
        try:
            user.suap_token = suap_api.refresh_token()
        except Exception as e:
            print(e)
    db.session.commit()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls update_suap_tokens() every 79200 seconds.
    sender.add_periodic_task(79200, update_suap_tokens.s())
