from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q

def home(request):
    sellers_sites  = Product.get_all_seller_sites()
    bestProducts = Product.get_top_trending_products() 
    categories = Category.get_all_categories()
    title = "Meilleurs Plans du Moment"  # Vous pouvez aussi le rendre dynamique selon les besoins
    return render(request, 'home.html', {'Products' : bestProducts, 'categories': categories, 'sellers_sites': sellers_sites,'title': title})

def faq(request):
    return render(request, 'faq.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def product_detail(request, slug):
    # Récupérer le produit spécifique par son slug
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug)
     # Récupérer tous les produits de la même catégorie sans slice
    similar_products = Product.objects.filter(category__name=product.category.name).exclude(id=product.id)
    # Limiter à 10 produits populaires après exclusion
    similar_products = similar_products[:10]
    return render(request, 'product.html', {'product': product, 'products': similar_products})

def category_products(request, category_name):
    """
    Récupère les produits d'une catégorie spécifique et les affiche dans la vue.
    """
    # Récupérer les produits associés à la catégorie par son nom
    products = Product.get_products_by_category_name(category_name)
    sellers_sites  = Product.get_all_seller_sites()
    categories = Category.get_all_categories()
    # Passer les produits à la template
    return render(request, 'home.html', {'Products': products, 'categories': categories, 'sellers_sites': sellers_sites, 'title': category_name})

def products_with_bestPromo(request): 
    products = Product.get_products_with_best_discount()
    title = "Meilleurs promo du moment"
    sellers_sites  = Product.get_all_seller_sites()
    categories = Category.get_all_categories()
    # Passer les produits à la template
    return render(request, 'home.html', {'Products': products, 'categories': categories,'sellers_sites': sellers_sites, 'title': title})

def products_without_promo_code(request):
    products = Product.get_products_without_code_promo()
    title = "Produits avec promotion sans code"
    sellers_sites  = Product.get_all_seller_sites()
    categories = Category.get_all_categories()
    # Passer les produits à la template
    return render(request, 'home.html', {'Products': products, 'categories': categories, 'sellers_sites': sellers_sites, 'title': title})
    
def products_with_promo_code(request):
    products = Product.get_products_with_code_promo()
    title = "Produits avec code promo"
    sellers_sites  = Product.get_all_seller_sites()
    categories = Category.get_all_categories()
    # Passer les produits à la template
    return render(request, 'home.html', {'Products': products, 'categories': categories,'sellers_sites': sellers_sites, 'title': title})

def products_by_seller(request, seller_site):
    products = Product.get_products_by_seller_site(seller_site)
    title = "Les Meilleurs plans sur : "
    title = title + seller_site
    sellers_sites  = Product.get_all_seller_sites()
    categories = Category.get_all_categories()
    return render(request, 'home.html', {'Products': products,'categories': categories, 'sellers_sites': sellers_sites, 'title': title})


def search(request):
    query = request.GET.get('query', '')  # Récupère le texte de la barre de recherche
    products = []
    sellers_sites = Product.get_all_seller_sites()
    categories = Category.get_all_categories()
    if query:
        # Découper la recherche en mots individuels
        words = query.split()

        # Créer des requêtes pour plusieurs champs
        q_objects = Q()
        for word in words:
            q_objects |= Q(name__icontains=word)  # Recherche dans le nom du produit
            q_objects |= Q(description__icontains=word)  # Recherche dans la description du produit
            q_objects |= Q(category__name__icontains=word)  # Recherche dans le nom de la catégorie

        # Filtrer les produits qui correspondent à la recherche
        products = Product.objects.filter(q_objects).distinct()

        # Trier les produits par score de popularité (trending score) en ordre décroissant
        products = products.order_by('-trending_score')

        if len(products) == 0:
            title = f"Aucun produit ne correspond à votre recherche : \"{query}\""
        else:
            title = f"Résultats pour : \"{query}\""
        return render(request, 'home.html', {'Products': products, 'sellers_sites': sellers_sites, 'title': title})

    title = "Meilleurs Plans du Moment"
    bestProducts = Product.get_top_trending_products()
    return render(request, 'home.html', {'Products': bestProducts, 'categories': categories, 'sellers_sites': sellers_sites, 'title': title})
