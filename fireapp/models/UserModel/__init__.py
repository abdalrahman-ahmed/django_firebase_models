import threading
from datetime import datetime, timezone

from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator
from django.db import models
from google.cloud.firestore_v1 import FieldFilter

from fireapp.core.firebase import firestore, auth


class UserModel(models.Model):
    Model = firestore('users')

    name = models.CharField(max_length=50, validators=[MinLengthValidator(3), MaxLengthValidator(50)])
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone = models.CharField(unique=True, max_length=31, validators=[MinLengthValidator(4), MaxLengthValidator(31)])
    password = models.CharField(max_length=128, validators=[MaxLengthValidator(128)])

    @classmethod
    def login(cls, email: str, password: str):
        user = cls.Model.where(filter=FieldFilter('email', '==', email)).get()
        if len(user) == 0:
            return False
        else:
            user = user[0].to_dict()
            if not check_password(password, user['password']):
                return False
            user.pop('password', None)
            custom_token = auth.create_custom_token(str(user['id']))
            return {'success': True, 'custom_token': custom_token}

    @classmethod
    def register(cls, data: dict):
        email = data['email']
        phone = data['phone']
        password = data['password']
        users = cls.Model.where(filter=FieldFilter('email', '==', email)).where(filter=FieldFilter('phone', '==', phone)).get()
        if len(users) == 0:
            count = cls.Model.count().get()[0][0].value
            document_id = int(count + 1)
            password = make_password(password)
            data.update({'id': document_id, 'password': password, 'created': datetime.now(tz=timezone.utc)})
            cls.Model.document(str(document_id)).set(data)
            custom_token = auth.create_custom_token(str(document_id))
            return {'success': True, 'custom_token': custom_token}
        else:
            return False

    @classmethod
    def document(cls, document_id: str):
        return cls.Model.document(document_id)

    @classmethod
    def watch(cls, callback: callable = None):
        # Create an Event for notifying main thread.
        callback_done = threading.Event()
        if callback is None:
            # Create a callback on_snapshot function to capture changes
            def callback(col_snapshot, changes, read_time):
                print("Callback received query snapshot.")
                for change in changes:
                    uid = change.document.id
                    document = change.document.to_dict()
                    status = change.type.name
                    print(f"{status} User: {uid} {'email' in document and document['email'] or ''}")
                callback_done.set()

        # Watch the collection query
        cls.Model.on_snapshot(callback)

    @classmethod
    def unwatch(cls):
        cls.Model.on_snapshot(None)
