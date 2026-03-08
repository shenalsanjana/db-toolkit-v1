from django.db import models


class Flag(models.IntegerChoices):
    NONE = 0, "None"
    DELETED = 1, "Deleted"
