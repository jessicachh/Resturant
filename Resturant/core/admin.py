from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Momo, CartItem, Order, OrderItem


# Admin panel header
admin.site.site_header = "BITE"
admin.site.site_title = "Bite"
admin.site.index_title = "Admin"

# Category registration
admin.site.register(Category)

# Momo registration with customization
@admin.register(Momo)
class MomoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'desc', 'price', 'display_img']
    list_display_links = ['name']
    list_editable = ['category']
    list_filter = ['price', 'category']
    list_per_page = 2
    ordering = ['name']

    def display_img(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100px" height="100px"; >', obj.image.url)

# CartItem (optional to track current carts)
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    list_filter = ['user', 'product']

# Inline display of order items within an order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Do not show extra empty rows
    readonly_fields = ['product', 'quantity', 'price']  # Optional: prevent editing

# Order admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'phone', 'payment_method', 'total', 'created_at']
    list_filter = ['payment_method', 'created_at']
    search_fields = ['name', 'user__username', 'phone']
    inlines = [OrderItemInline]
    readonly_fields = ['user', 'name', 'phone', 'address', 'payment_method', 'total']  # Optional: prevent editing

# OrderItem registration (optional if you want separate view)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order', 'product']
