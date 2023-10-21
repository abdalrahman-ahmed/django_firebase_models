from django.conf import settings
from firebase_admin import (
    credentials as fbc,
    firestore as fbs,
    auth as fba,
    initialize_app as fbi
)

credential = fbc.Certificate(settings.FIREBASE_CONFIG_FILE)

fbi(credential)

app = fbi(credential, name=settings.FIREBASE_APP_NAME)
firestore = fbs.client(app=app).collection
auth = fba.Client(app=app)
