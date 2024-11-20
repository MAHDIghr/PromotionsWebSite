from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

class Product(models.Model):
    # Product name
    name = models.CharField(max_length=100, unique=True)
    
    # Product description
    description = models.TextField(blank=True)
    
    # Original price (before promotion)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Current price (after promotion)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Category (relationship to another table, if needed)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    # Date of creation
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Date of last update
    updated_at = models.DateTimeField(auto_now=True)
    
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

    # Slug field 
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    click_count = models.IntegerField(default=0)
    
    # Seller site name
    seller_site = models.CharField(max_length=100, null=True, blank=True)

    # Trending score (rating out of 10)
    trending_score = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    def __str__(self):
        return self.name
    
    @classmethod
    def get_top_trending_products(cls, limit=20):
        """
        Récupère les produits avec les scores de tendance les plus élevés.

        :param limit: Nombre maximum de produits à récupérer.
        :return: QuerySet des produits triés par trending_score décroissant.
        """
        return cls.objects.filter(is_active=True).order_by('-trending_score')[:limit]

    @classmethod
    def get_products_by_category_name(cls, category_name, limit=None):
        """
        Récupère les produits d'une catégorie donnée en utilisant le nom de la catégorie,
        triés par score de tendance.

        :param category_name: Le nom de la catégorie pour filtrer les produits.
        :param limit: Le nombre de produits à récupérer (facultatif).
        :return: QuerySet des produits triés par trending_score décroissant.
        """
        # Filtrer les produits par le nom de la catégorie et trier par trending_score
        products = cls.objects.filter(category__name=category_name, is_active=True).order_by('-trending_score')

        if limit:
            return products[:limit]  # Limiter le nombre de produits retournés si `limit` est défini
        return products
    
    @classmethod
    def get_products_by_seller_site(cls, seller_site):
        """
        Récupère tous les produits d'un site vendeur spécifique et les trie par leur score de tendance.
        
        :param seller_site: Le nom du site vendeur pour filtrer les produits.
        :return: QuerySet des produits triés par trending_score décroissant.
        """
        return cls.objects.filter(seller_site=seller_site, is_active=True).order_by('-trending_score')

    @classmethod
    def get_all_seller_sites(cls):
        """
        Récupère tous les 'seller_site' distincts de la base de données.
        
        :return: Liste des seller_sites distincts.
        """
        # Utilisation de .values() pour obtenir des valeurs distinctes de 'seller_site'
        return cls.objects.values_list('seller_site', flat=True).distinct()
    
    @classmethod
    def get_products_without_code_promo(cls):
        """
        Récupère les produits sans code promo et les trie par score de tendance décroissant.
        
        :return: QuerySet des produits sans code promo, triés par trending_score.
        """
        return cls.objects.filter(promo_code__isnull=True, is_active=True).order_by('-trending_score')
    
    @classmethod
    def get_products_with_code_promo(cls):
        """
        Récupère les produits avec un code promo et les trie par score de tendance décroissant.
        
        :return: QuerySet des produits avec code promo, triés par trending_score.
        """
        return cls.objects.filter(promo_code__isnull=False, promo_code__gt='', is_active=True).order_by('-trending_score')

    @classmethod
    def get_products_with_best_discount(cls, limit=30):
        """
        Récupère les produits avec les meilleures réductions en calculant
        la différence entre le prix original et le prix actuel,
        triés par ordre décroissant de la réduction.

        :param limit: Le nombre maximum de produits à retourner (par défaut 30).
        :return: QuerySet des produits triés par réduction décroissante.
        """
        # Annoter chaque produit avec un champ temporaire calculant la réduction
        products = cls.objects.filter(is_active=True, original_price__isnull=False).annotate(discount=models.F('original_price') - models.F('current_price')).order_by('-discount')
        # Trier par la réduction décroissante

        return products[:limit]  # Limiter à `limit` produits

# Signal post_save pour générer le slug après la création du produit
@receiver(post_save, sender=Product)
def generate_product_slug(sender, instance, created, **kwargs):
    if created and not instance.slug:  # Si le produit est nouvellement créé et n'a pas de slug
        instance.slug = slugify(f"{instance.name}-{instance.id}")  # Créer le slug basé sur le nom et l'ID
        instance.save()  # Sauvegarder à nouveau pour mettre à jour le slug avec l'ID

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

