from django.db import models

class Product(models.Model):
    # Product name
    name = models.CharField(max_length=100, unique=True)
    
    # Product description
    description = models.TextField(blank=True)
    
    # Original price (before promotion)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Current price (after promotion)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Quantity in stock
    stock = models.PositiveIntegerField()
    
    # Category (relationship to another table, if needed)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    # Date of creation
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Date of last update
    updated_at = models.DateTimeField(auto_now=True)
    
    # SKU (unique product identifier)
    identifier = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    # Product status (active or inactive)
    is_active = models.BooleanField(default=True)
    
    # Promo start date
    promo_start_date = models.DateTimeField(null=True, blank=True)
    
    # Promo end date
    promo_end_date = models.DateTimeField(null=True, blank=True)
    
    # Product link (URL for the product)
    product_link = models.URLField(max_length=200, null=True, blank=True)
    
    # Promo code (discount code for the product)
    promo_code = models.CharField(max_length=50, null=True, blank=True)

    # Removing the single image field
    # image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    click_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    
    def __str__(self):
        return f"Image for {self.product.name}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Functions for DB interrogation

@classmethod
def get_all_products(cls):
    return cls.objects.all()

def increment_click_count(self):
    """Incrémente le compteur de clics."""
    self.click_count += 1
    self.save()
