from django.db import models


class OrderStatus(models.IntegerChoices):
    PENDING = 0, "Pending"
    PAID = 1, "Paid"
    PROCESSING = 2, "Processing"
    SHIPPED = 3, "Shipped"
    DELIVERED = 4, "Delivered"
    CANCELLED = 5, "Cancelled"
    REFUNDED = 6, "Refunded"
