from django.contrib import admin
from .models import Product, Category, ProductImage, ContactSubmission, Link

# Inline admin for ProductImage
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra forms to display

# Register the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon')  # Fields to display in the admin list
    search_fields = ('name', 'description', 'icon')  # Fields to be searchable

# Register the Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller_site', 'trending_score', 'category', 'original_price', 'current_price', 'promo_start_date', 'promo_end_date', 'is_active', 'click_count')
    list_filter = ('category', 'is_active', 'seller_site')  # Filters for the admin panel
    search_fields = ('name', 'identifier', 'description')  # Fields to be searchable
    date_hierarchy = 'created_at'  # Date hierarchy for easy browsing
    ordering = ('-created_at',)  # Ordering by the created date

    inlines = [ProductImageInline]  # Include the inline for ProductImage

# Register the ProductImage model
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')  # Fields to display in the admin list

# Register the ContactSubmission model
@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'object', 'submitted_at')
    ordering = ('-submitted_at',)  # Ordering by the submitted date

# Register the Link model
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('link', 'description', 'score')  # Champs affichés dans la liste des liens
    search_fields = ('link', 'description')  # Champs recherchables
    list_filter = ('score',)  # Filtres pour trier par score
    ordering = ('-score',)  # Trier par score décroissant par défaut