
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    Promotion,
    Collection,
    Product,
    ProductImage,
    Customer,
    Order,
    OrderItem,
    Address,
    Review,
    Cart,
    CartItem,
)


# ============================================================
# ADMIN SITE
# ============================================================

admin.site.site_header = "🛍️ Store Administration"
admin.site.site_title = "Store Admin"
admin.site.index_title = "Store Management Dashboard"


# ============================================================
# HELPER
# ============================================================

def money(value):
    if value is None:
        value = 0

    return f"${value:,.2f}"


# ============================================================
# PROMOTION
# ============================================================

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):

    list_display = (
        "description",
        "discount_badge",
        "product_count",
    )

    search_fields = (
        "description",
    )

    ordering = (
        "-discount",
    )

    @admin.display(description="Discount")
    def discount_badge(self, obj):

        return format_html(
            '<span style="'
            'background:#dcfce7;'
            'color:#166534;'
            'padding:5px 10px;'
            'border-radius:999px;'
            'font-weight:600;'
            '">{}%</span>',
            obj.discount,
        )

    @admin.display(description="Products")
    def product_count(self, obj):
        return obj.products.count()


# ============================================================
# PRODUCT IMAGE INLINE
# ============================================================

class ProductImageInline(admin.TabularInline):

    model = ProductImage

    extra = 1

    fields = (
        "image",
        "image_preview",
    )

    readonly_fields = (
        "image_preview",
    )

    @admin.display(description="Preview")
    def image_preview(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" '
                'width="90" '
                'height="90" '
                'style="object-fit:cover;'
                'border-radius:10px;'
                'border:1px solid #ddd;" />',
                obj.image.url,
            )

        return mark_safe(
            '<span style="color:#999;">No image</span>'
        )


# ============================================================
# PRODUCT
# ============================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "product_thumbnail",
        "title",
        "collection",
        "price_display",
        "inventory_badge",
        "promotion_count",
        "last_update",
    )

    list_display_links = (
        "title",
    )

    list_filter = (
        "collection",
        "promotions",
        "last_update",
    )

    search_fields = (
        "title",
        "description",
        "collection__title",
    )

    autocomplete_fields = (
        "collection",
        "promotions",
    )

    readonly_fields = (
        "last_update",
    )

    inlines = (
        ProductImageInline,
    )

    ordering = (
        "-last_update",
    )

    list_per_page = 25

    fieldsets = (
        (
            "📦 Product Information",
            {
                "fields": (
                    "title",
                    "description",
                    "collection",
                )
            },
        ),

        (
            "💰 Pricing & Inventory",
            {
                "fields": (
                    "price",
                    "inventory",
                )
            },
        ),

        (
            "🎯 Marketing",
            {
                "fields": (
                    "promotions",
                )
            },
        ),

        (
            "⚙️ System Information",
            {
                "fields": (
                    "last_update",
                )
            },
        ),
    )

    @admin.display(description="Product")
    def product_thumbnail(self, obj):

        image = obj.images.first()

        if image and image.image:

            return format_html(
                '<img src="{}" '
                'width="55" '
                'height="55" '
                'style="object-fit:cover;'
                'border-radius:8px;'
                'border:1px solid #ddd;" />',
                image.image.url,
            )

        return mark_safe(
            '<div style="'
            'width:55px;'
            'height:55px;'
            'background:#f3f4f6;'
            'border-radius:8px;'
            'display:flex;'
            'align-items:center;'
            'justify-content:center;'
            'color:#9ca3af;'
            'font-size:10px;'
            '">No image</div>'
        )

    @admin.display(description="Price")
    def price_display(self, obj):

        return format_html(
            "<strong>{}</strong>",
            money(obj.price),
        )

    @admin.display(description="Inventory")
    def inventory_badge(self, obj):

        if obj.inventory == 0:

            return mark_safe(
                '<span style="'
                'background:#fee2e2;'
                'color:#991b1b;'
                'padding:5px 10px;'
                'border-radius:999px;'
                'font-weight:600;'
                '">🔴 Out of stock</span>'
            )

        if obj.inventory <= 5:

            return format_html(
                '<span style="'
                'background:#fef3c7;'
                'color:#92400e;'
                'padding:5px 10px;'
                'border-radius:999px;'
                'font-weight:600;'
                '">⚠️ {} left</span>',
                obj.inventory,
            )

        return format_html(
            '<span style="'
            'background:#dcfce7;'
            'color:#166534;'
            'padding:5px 10px;'
            'border-radius:999px;'
            'font-weight:600;'
            '">🟢 {} in stock</span>',
            obj.inventory,
        )

    @admin.display(description="Promotions")
    def promotion_count(self, obj):
        return obj.promotions.count()


# ============================================================
# COLLECTION
# ============================================================

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "product_count",
        "featured_product",
    )

    search_fields = (
        "title",
    )

    autocomplete_fields = (
        "featured_product",
    )

    @admin.display(description="Products")
    def product_count(self, obj):
        return obj.products.count()


# ============================================================
# PRODUCT IMAGE
# ============================================================

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "product",
    )

    search_fields = (
        "product__title",
    )

    autocomplete_fields = (
        "product",
    )

    @admin.display(description="Image")
    def image_preview(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" '
                'width="100" '
                'height="100" '
                'style="object-fit:cover;'
                'border-radius:10px;" />',
                obj.image.url,
            )

        return mark_safe(
            '<span style="color:#999;">No image</span>'
        )


# ============================================================
# CUSTOMER
# ============================================================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "customer_name",
        "email",
        "phone",
        "membership_badge",
        "order_count",
    )

    list_filter = (
        "membership",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "phone",
    )

    autocomplete_fields = (
        "user",
    )

    list_per_page = 25

    @admin.display(description="Customer")
    def customer_name(self, obj):

        name = (
            f"{obj.user.first_name} "
            f"{obj.user.last_name}"
        ).strip()

        return name or obj.user.username

    @admin.display(description="Email")
    def email(self, obj):
        return obj.user.email

    @admin.display(description="Membership")
    def membership_badge(self, obj):

        styles = {
            "B": ("#f3f4f6", "#374151"),
            "S": ("#e5e7eb", "#1f2937"),
            "G": ("#fef3c7", "#92400e"),
        }

        background, color = styles.get(
            obj.membership,
            ("#f3f4f6", "#374151"),
        )

        return format_html(
            '<span style="'
            'background:{};'
            'color:{};'
            'padding:5px 10px;'
            'border-radius:999px;'
            'font-weight:600;'
            '">{}</span>',
            background,
            color,
            obj.get_membership_display(),
        )

    @admin.display(description="Orders")
    def order_count(self, obj):
        return obj.orders.count()


# ============================================================
# ORDER ITEM INLINE
# ============================================================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    fields = (
        "product",
        "quantity",
        "unit_price",
        "item_total",
    )

    readonly_fields = (
        "item_total",
    )

    autocomplete_fields = (
        "product",
    )

    @admin.display(description="Total")
    def item_total(self, obj):

        if not obj.pk:
            return money(0)

        return money(
            obj.quantity * obj.unit_price
        )


# ============================================================
# ORDER
# ============================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "customer_name",
        "payment_status_badge",
        "item_count",
        "order_total",
        "placed_at",
    )

    list_filter = (
        "payment_status",
        "placed_at",
    )

    search_fields = (
        "id",
        "customer__user__first_name",
        "customer__user__last_name",
        "customer__user__email",
    )

    autocomplete_fields = (
        "customer",
    )

    readonly_fields = (
        "placed_at",
        "order_total",
    )

    inlines = (
        OrderItemInline,
    )

    ordering = (
        "-placed_at",
    )

    list_per_page = 25

    fieldsets = (
        (
            "🧾 Order Information",
            {
                "fields": (
                    "customer",
                    "payment_status",
                )
            },
        ),

        (
            "💰 Order Summary",
            {
                "fields": (
                    "order_total",
                )
            },
        ),

        (
            "🕒 Timeline",
            {
                "fields": (
                    "placed_at",
                )
            },
        ),
    )

    @admin.display(description="Order")
    def order_number(self, obj):

        return format_html(
            "<strong>#{}</strong>",
            obj.id,
        )

    @admin.display(description="Customer")
    def customer_name(self, obj):

        name = (
            f"{obj.customer.user.first_name} "
            f"{obj.customer.user.last_name}"
        ).strip()

        return name or obj.customer.user.username

    @admin.display(description="Payment")
    def payment_status_badge(self, obj):

        styles = {
            "P": (
                "#fef3c7",
                "#92400e",
                "🟠 Pending",
            ),
            "C": (
                "#dcfce7",
                "#166534",
                "🟢 Complete",
            ),
            "F": (
                "#fee2e2",
                "#991b1b",
                "🔴 Failed",
            ),
        }

        background, color, label = styles.get(
            obj.payment_status,
            ("#f3f4f6", "#374151", "Unknown"),
        )

        return format_html(
            '<span style="'
            'background:{};'
            'color:{};'
            'padding:5px 10px;'
            'border-radius:999px;'
            'font-weight:600;'
            '">{}</span>',
            background,
            color,
            label,
        )

    @admin.display(description="Items")
    def item_count(self, obj):
        return obj.items.count()

    @admin.display(description="Total")
    def order_total(self, obj):

        total = sum(
            item.quantity * item.unit_price
            for item in obj.items.all()
        )

        return format_html(
            '<strong style="font-size:14px;">{}</strong>',
            money(total),
        )


# ============================================================
# ADDRESS
# ============================================================

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (
        "customer",
        "street",
        "city",
    )

    list_filter = (
        "city",
    )

    search_fields = (
        "street",
        "city",
        "customer__user__first_name",
        "customer__user__last_name",
        "customer__user__email",
    )

    autocomplete_fields = (
        "customer",
    )


# ============================================================
# REVIEW
# ============================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "customer",
        "product",
        "review_preview",
        "created_at",
    )

    list_filter = (
        "created_at",
        "product",
    )

    search_fields = (
        "description",
        "customer__user__first_name",
        "customer__user__last_name",
        "customer__user__email",
        "product__title",
    )

    autocomplete_fields = (
        "customer",
        "product",
    )

    readonly_fields = (
        "created_at",
    )

    @admin.display(description="Review")
    def review_preview(self, obj):

        text = obj.description

        if len(text) > 70:
            text = f"{text[:70]}..."

        return text


# ============================================================
# CART ITEM INLINE
# ============================================================

class CartItemInline(admin.TabularInline):

    model = CartItem

    extra = 0

    fields = (
        "product",
        "quantity",
    )

    autocomplete_fields = (
        "product",
    )


# ============================================================
# CART
# ============================================================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "short_id",
        "created_at",
        "item_count",
    )

    search_fields = (
        "id",
    )

    readonly_fields = (
        "id",
        "created_at",
    )

    inlines = (
        CartItemInline,
    )

    ordering = (
        "-created_at",
    )

    @admin.display(description="Cart ID")
    def short_id(self, obj):

        return f"{str(obj.id)[:8]}..."

    @admin.display(description="Items")
    def item_count(self, obj):
        return obj.items.count()


# ============================================================
# CART ITEM
# ============================================================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "cart",
        "product",
        "quantity",
    )

    search_fields = (
        "cart__id",
        "product__title",
    )

    autocomplete_fields = (
        "cart",
        "product",
    )


# ============================================================
# ORDER ACTIONS
# ============================================================

@admin.action(description="🟢 Mark selected orders as complete")
def mark_orders_complete(modeladmin, request, queryset):

    queryset.update(
        payment_status=Order.PAYMENT_STATUS_COMPLETE
    )


@admin.action(description="🟠 Mark selected orders as pending")
def mark_orders_pending(modeladmin, request, queryset):

    queryset.update(
        payment_status=Order.PAYMENT_STATUS_PENDING
    )


@admin.action(description="🔴 Mark selected orders as failed")
def mark_orders_failed(modeladmin, request, queryset):

    queryset.update(
        payment_status=Order.PAYMENT_STATUS_FAILED
    )


OrderAdmin.actions = (
    mark_orders_complete,
    mark_orders_pending,
    mark_orders_failed,
)


# ============================================================
# LOW STOCK FILTER
# ============================================================

class LowStockFilter(admin.SimpleListFilter):

    title = "Inventory"

    parameter_name = "inventory_status"

    def lookups(self, request, model_admin):

        return (
            ("out", "🔴 Out of stock"),
            ("low", "⚠️ Low stock"),
            ("available", "🟢 In stock"),
        )

    def queryset(self, request, queryset):

        if self.value() == "out":
            return queryset.filter(
                inventory=0
            )

        if self.value() == "low":
            return queryset.filter(
                inventory__gt=0,
                inventory__lte=5,
            )

        if self.value() == "available":
            return queryset.filter(
                inventory__gt=5
            )

        return queryset


ProductAdmin.list_filter = (
    "collection",
    "promotions",
    LowStockFilter,
    "last_update",
)

