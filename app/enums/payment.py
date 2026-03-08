from django.db import models


class PaymentProvider(models.IntegerChoices):
    STRIPE = 0, "Stripe"
    COD = 1, "Cash on Delivery"
    CARD = 2, "Card"
    MINTPAY = 3, "MintPay"
    KOKO = 4, "Koko"
    PAYEASY = 5, "Payeasy"


class PaymentStatus(models.IntegerChoices):
    PENDING = 0, "Pending"
    SUCCEEDED = 1, "Succeeded"
    FAILED = 2, "Failed"
    REFUNDED = 3, "Refunded"
