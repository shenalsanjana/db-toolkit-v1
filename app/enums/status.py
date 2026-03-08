from django.db import models


class Status(models.IntegerChoices):
    INACTIVE = 0, "Inactive"
    ACTIVE = 1, "Active"
