from django.contrib import admin
from .models import Product, ProductSize, ProductPot, ProductVariant, ProductImage, Category, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter  = ['rating', 'product']

@admin.register(ProductPot)
class ProductPotAdmin(admin.ModelAdmin):
    list_display = ['product', 'pot_name', 'icon', 'order']
    list_filter  = ['product']

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['size', 'pot', 'price', 'old_price', 'stock', 'sku']
    list_filter  = ['size__product']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'icon', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name']

# ── Image Inline 
class ProductImageInline(admin.TabularInline):
    model   = ProductImage
    extra   = 4        
    fields  = ['image', 'order']


# ── Variant Inline (Size + Pot combination) ───────────────
class ProductVariantInline(admin.TabularInline):
    model   = ProductVariant
    extra   = 1
    fields  = ['pot', 'price', 'old_price', 'stock', 'sku']


# ── Size Admin (Image + Variant ) ───────────────
@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    inlines      = [ProductImageInline, ProductVariantInline]
    list_display = ['product', 'size_name', 'pot_size_label', 'order']
    list_filter  = ['product']


# ── Pot Inline (Product ) ────────────────────────
class ProductPotInline(admin.TabularInline):
    model  = ProductPot
    extra  = 3        # 3 pot slots
    fields = ['pot_name', 'icon', 'order']


# ── Size Inline (Product ) ───────────────────────
class ProductSizeInline(admin.TabularInline):
    model  = ProductSize
    extra  = 3        # 3 size slots
    fields = ['size_name', 'pot_size_label', 'order']


# ── Main Product Admin ────────────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizeInline, ProductPotInline]

    list_display  = ['name', 'category', 'is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['name', 'category']
    list_filter   = ['category', 'is_active', 'air_purifying']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'category', 'description', 'badge_text', 'is_active')
        }),
        ('Plant Details', {
            'fields': ('scientific_name', 'common_name', 'family', 'origin',
                       'plant_type', 'mature_height', 'growth_rate', 'toxicity', 'air_purifying'),
            'classes': ('collapse',)   # ← click karke open hoga
        }),
        ('Care Info', {
            'fields': ('watering', 'sunlight', 'temperature', 'humidity', 'care_guide'),
            'classes': ('collapse',)
        }),
    )