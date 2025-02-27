from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Link, ContactSubmission
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect

def faq(request):
    return render(request, 'faq.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

@csrf_protect
def contact_after_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        object = request.POST.get('object')
        message = request.POST.get('message')

        # Sauvegarder les données dans la base de données
        ContactSubmission.objects.create(
            name=name,
            email=email,
            object=object,
            message=message
        )
        
        return render(request, 'answer_contact.html')
    return render(request, 'contact.html')

def increment_click_and_redirect(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.click_count += 1
    product.save()
    return redirect(product.product_link)


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

def home(request):

    # Récupérer les données pour le template
    sellers_sites = Product.get_all_seller_sites()
    bestProducts = Product.get_top_trending_products()
    categories = Category.get_all_categories()

    # Préparer le contexte pour le template
    title = "Meilleurs Plans du Moment"
    context = {
        'Products': bestProducts,
        'categories': categories,
        'sellers_sites': sellers_sites,
        'title': title,
    }

    return render(request, 'home.html', context)

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

def usful_links(request):
    # Récupérer tous les liens triés par score décroissant
    links = Link.objects.order_by('-score')
    return render(request, 'links.html', {'links': links})