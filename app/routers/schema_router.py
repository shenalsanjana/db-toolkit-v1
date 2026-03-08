from app.persistence.models import (Customer, Category, Product, ProductVariant, Address, ProductImage, ProductColor,
                                    ProductSize, Inventory,
                                    Cart,
                                    CartItem,
                                    Order,
                                    OrderItem,
                                    Payment,
                                    Shipment,
                                    Wishlist,
                                    WishlistItem,
                                    Banner,
                                    Coupon,
                                    Review,
                                    ProductTag,
                                    ProductTagMap,
                                    HomepageSection,
                                    HomepageSectionProduct,
                                    Setting,
                                    )

ROUTE_MODELS = [
    Customer,
    Category,
    Product,
    ProductVariant,
    Address,
    ProductImage,
    ProductColor,
    ProductSize,
    Inventory,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Payment,
    Shipment,
    Wishlist,
    WishlistItem,
    Banner,
    Coupon,
    Review,
    ProductTag,
    ProductTagMap,
    HomepageSection,
    HomepageSectionProduct,
    Setting,
]

SCHEMA_NAME = 'db_database'


class SchemaRouter:

    def db_for_read(self, model, **hints):
        if model in ROUTE_MODELS:
            return SCHEMA_NAME
        return None

    def db_for_write(self, model, **hints):
        if model in ROUTE_MODELS:
            return SCHEMA_NAME
        return None
