from ConviteDigital import database, app
from ConviteDigital.models import Usuario, Foto

with app.app_context():
    database.create_all()