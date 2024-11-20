from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Q

def home(request):
    sellers_sites  = Product.get_all_seller_sites()
    bestProducts = Product.get_top_trending_products() 
    title = "Meilleurs Plans du Moment"  # Vous pouvez aussi le rendre dynamique selon les besoins
    return render(request, 'home.html', {'Products' : bestProducts, 'sellers_sites': sellers_sites,'title': title})

def faq(request):
    return render(request, 'faq.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product.html', {'product': product})

def category_products(request, category_name):
    """
    Récupère les produits d'une catégorie spécifique et les affiche dans la vue.
    """
    # Récupérer les produits associés à la catégorie par son nom
    products = Product.get_products_by_category_name(category_name)
    sellers_sites  = Product.get_all_seller_sites()
    # Passer les produits à la template
    return render(request, 'home.html', {'Products': products, 'sellers_sites': sellers_sites, 'title': category_name})

def products_with_bestPromo(request): 
    products = Product.get_products_with_best_discount()
    title = "Meilleurs promo du moment"
    sellers_sites  = Product.get_all_seller_sites()
    # Passer les produits à la template
    return render(request, 'home.html', {'Products': products, 'sellers_sites': sellers_sites, 'title': title})

def products_without_promo_code(request):
    products = Product.get_products_without_code_promo()
    title = "Produits avec promotion sans code"
    sellers_sites  = Product.get_all_seller_sites()
    # Passer les produits à la template
    return render(request, 'home.html', {'Products': products, 'sellers_sites': sellers_sites, 'title': title})
    
def products_with_promo_code(request):
    products = Product.get_products_with_code_promo()
    title = "Produits avec code promo"
    sellers_sites  = Product.get_all_seller_sites()
    # Passer les produits à la template
    return render(request, 'home.html', {'Products': products, 'sellers_sites': sellers_sites, 'title': title})

def products_by_seller(request, seller_site):
    print("Seller Site URL: ", seller_site)
    products = Product.get_products_by_seller_site(seller_site)
    title = "Les Meilleurs plans sur : "
    title = title + seller_site
    sellers_sites  = Product.get_all_seller_sites()
    print("Seller Site: ", seller_site)
    print("Title: ", title)
    print("Products: ", products)  # Affiche la liste ou un objet représentant les produits
    print("Sellers Sites: ", sellers_sites)  # Affiche la liste de tous les sites de vendeurs
    return render(request, 'home.html', {'Products': products, 'sellers_sites': sellers_sites, 'title': title})

def search(request):
    query = request.GET.get('query', '')  # Récupère le texte de la barre de recherche
    products = []
    sellers_sites  = Product.get_all_seller_sites()
    if query:
        # Découper la recherche en mots individuels
        words = query.split()
        
        # Créer une requête qui cherche dans le nom des produits en utilisant "Q" pour faire une recherche OR
        q_object = Q(name__icontains=words[0])  # Recherche sur le premier mot
        for word in words[1:]:
            q_object |= Q(name__icontains=word)  # Ajoute les autres mots avec une recherche OR
        
        # Filtrer les produits qui correspondent à la recherche
        products = Product.objects.filter(q_object)
        if len(products) == 0:
            title = "Aucun produits ne correspond à votre recherche : \"" + query +"\""
        else : 
            title = "Résultats pour : \""  + query +"\""
        return render(request, 'home.html', {'Products': products, 'sellers_sites': sellers_sites, 'title': title})
    
    title = "Meilleurs Plans du Moment"
    bestProducts = Product.get_top_trending_products() 
    return render(request, 'home.html', {'Products': bestProducts, 'sellers_sites': sellers_sites, 'title': title})
