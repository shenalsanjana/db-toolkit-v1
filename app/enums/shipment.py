from django.db import models


class ShipmentStatus(models.IntegerChoices):
    PENDING = 0, "Pending"
    SHIPPED = 1, "Shipped"
    DELIVERED = 2, "Delivered"
    RETURNED = 3, "Returned"
