from django.core.validators import MinLengthValidator
from django.db import models
from fireapp.core.firebase import firestore
from google.cloud.firestore_v1 import Query


class ChatModel(models.Model):
    Model = firestore('chat')

    receiver_id = models.TextField(null=False, blank=False, validators=[MinLengthValidator(1)])
    message = models.TextField(null=False, blank=False, validators=[MinLengthValidator(1)])

    @classmethod
    def get_all(cls) -> list:
        items = cls.Model.order_by('id', direction=Query.DESCENDING).get()
        return [item.to_dict() for item in items]

    @classmethod
    def create(cls, data) -> dict:
        if (data['receiver_id'] and data['message']) and (data['receiver_id'] != '' and data['message'] != ''):
            data['receiver_id'] = int(data['receiver_id'])
            count = cls.Model.count().get()[0][0].value
            document_id = int(count + 1)
            data.update({'id': document_id})
            return cls.Model.document().set(data)

    @property
    def collection(self):
        return self.Model
