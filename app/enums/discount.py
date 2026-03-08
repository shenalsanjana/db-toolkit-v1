from django.db import models


class DiscountType(models.IntegerChoices):
    NONE = 0, "None"
    PERCENTAGE = 1, "Percentage"
    FIXED = 2, "Fixed"
