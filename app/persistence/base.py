import uuid
from django.db import models

from app.enums.flag import Flag
from app.enums.status import Status


class IDModel(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    uid = models.UUIDField("UUID", unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TrackableDateModel(models.Model):
    added_at = models.DateTimeField("Created At", auto_now_add=True)
    modified_at = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-modified_at",)


class CommonFieldModel(models.Model):
    status = models.SmallIntegerField(choices=Status.choices, default=Status.ACTIVE)
    flag = models.SmallIntegerField(choices=Flag.choices, default=Flag.NONE)

    class Meta:
        abstract = True


class BaseModel(IDModel, UUIDModel, TrackableDateModel, CommonFieldModel):
    class Meta:
        abstract = True
