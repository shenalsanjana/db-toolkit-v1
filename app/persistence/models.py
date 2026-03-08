from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError

from app.enums.order_status import OrderStatus
from app.enums.payment import PaymentProvider, PaymentStatus
from app.enums.shipment import ShipmentStatus
from app.enums.discount import DiscountType
from app.persistence.base import BaseModel


class Customer(BaseModel):
    name = models.CharField(max_length=150)
    mobile_no = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'customers'


class Category(BaseModel):
    parent = models.ForeignKey('Category', null=True, blank=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'category'


class Product(BaseModel):
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'product'


class ProductVariant(BaseModel):
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    sku = models.CharField(max_length=80, unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'product_variant'


class Address(BaseModel):
    user = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)
    address = models.TextField()
    is_default_shipping = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'address'


class ProductImage(BaseModel):
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    file = models.TextField()
    extension = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'product_image'


class ProductColor(BaseModel):
    variant = models.ForeignKey('ProductVariant', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'product_color'


class ProductSize(BaseModel):
    color = models.ForeignKey('ProductColor', on_delete=models.DO_NOTHING)
    size = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'product_size'


class Inventory(BaseModel):
    variant = models.OneToOneField('ProductVariant', on_delete=models.DO_NOTHING)
    qty = models.IntegerField(default=0)
    qty_reserved = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'inventory'

    def clean(self):
        if self.qty < 0:
            raise ValidationError("Quantity cannot be negative")
        if self.qty_reserved < 0:
            raise ValidationError("Reserved quantity cannot be negative")


class Cart(BaseModel):
    user = models.ForeignKey('Customer', null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cart'


class CartItem(BaseModel):
    cart = models.ForeignKey('Cart', on_delete=models.DO_NOTHING)
    variant = models.ForeignKey('ProductVariant', on_delete=models.DO_NOTHING)
    qty = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cart_item'
        unique_together = ("cart", "variant")

    def clean(self):
        if self.qty <= 0:
            raise ValidationError("Quantity must be greater than 0")


class Order(BaseModel):
    user = models.ForeignKey('Customer', null=True, blank=True, on_delete=models.DO_NOTHING)

    name = models.CharField(max_length=150)
    mobile_no = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField()

    order_status = models.SmallIntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    currency = models.CharField(max_length=3, default="LKR")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    discount_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    shipping_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        managed = False
        db_table = 'order'

    def clean(self):
        if not self.user and not self.email and not self.mobile_no:
            raise ValidationError("Order must have registered user or guest email/mobile")


class OrderItem(BaseModel):
    order = models.ForeignKey('Order', on_delete=models.DO_NOTHING)
    variant = models.ForeignKey('ProductVariant', on_delete=models.DO_NOTHING)
    qty = models.IntegerField()
    sku_snapshot = models.CharField(max_length=80, null=True, blank=True)
    product_name_snapshot = models.CharField(max_length=200, null=True, blank=True)
    unit_price_snapshot = models.DecimalField(max_digits=12, decimal_places=2)

    discount_type = models.SmallIntegerField(
        choices=DiscountType.choices,
        default=DiscountType.NONE
    )
    discount_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        managed = False
        db_table = 'order_item'

    def clean(self):
        if self.qty <= 0:
            raise ValidationError("Quantity must be greater than 0")
        if self.unit_price_snapshot < 0:
            raise ValidationError("Unit price cannot be negative")
        if self.discount_amount < 0:
            raise ValidationError("Discount cannot be negative")
        if self.line_total < 0:
            raise ValidationError("Line total cannot be negative")


class Payment(BaseModel):
    order = models.ForeignKey('Order', on_delete=models.DO_NOTHING)
    provider = models.SmallIntegerField(
        choices=PaymentProvider.choices,
        default=PaymentProvider.COD
    )
    payment_status = models.SmallIntegerField(
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'payment'


class Shipment(BaseModel):
    order = models.ForeignKey('Order', on_delete=models.DO_NOTHING)
    courier = models.TextField(null=True, blank=True)
    tracking_number = models.CharField(max_length=120, null=True, blank=True)
    shipping_status = models.SmallIntegerField(
        choices=ShipmentStatus.choices,
        default=ShipmentStatus.PENDING
    )
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'shipment'


class Wishlist(BaseModel):
    user = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wishlist'


class WishlistItem(BaseModel):
    wishlist = models.ForeignKey('Wishlist', on_delete=models.DO_NOTHING)
    variant = models.ForeignKey('ProductVariant', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wishlist_item'
        unique_together = ('wishlist', 'variant')


class Banner(BaseModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    image = models.TextField()
    link = models.CharField(max_length=500, null=True, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'banner'


class Coupon(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.SmallIntegerField(
        choices=DiscountType.choices,
        default=DiscountType.PERCENTAGE
    )
    value = models.DecimalField(max_digits=12, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_discount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    usage_limit = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'coupon'

    def clean(self):
        if self.value < 0:
            raise ValidationError("Coupon value cannot be negative")


class Review(BaseModel):
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'review'

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Rating must be between 1 and 5")


class ProductTag(BaseModel):
    name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'product_tag'


class ProductTagMap(BaseModel):
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    tag = models.ForeignKey('ProductTag', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'product_tag_map'
        unique_together = ('product', 'tag')


class HomepageSection(BaseModel):
    title = models.CharField(max_length=255)
    section_type = models.CharField(max_length=50)
    sort_order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'homepage_section'


class HomepageSectionProduct(BaseModel):
    section = models.ForeignKey('HomepageSection', on_delete=models.DO_NOTHING)
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'homepage_section_product'
        unique_together = ('section', 'product')


class Setting(BaseModel):
    key = models.CharField(max_length=150, unique=True)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'setting'
