from playwright.sync_api import sync_playwright
from ...models import Product
import csv
import sys
import os

# Forcer l'encodage en UTF-8 pour éviter les problèmes d'encodage
sys.stdout.reconfigure(encoding='utf-8')

product_links = Product.get_amazon_product_links()

# Cookies extraits manuellement, avec l'ajout de l'URL associée
cookies = [
    {"name": "session-id", "value": "261-0862546-5874349", "domain": ".amazon.fr", "path": "/"},
    {"name": "ubid-acbfr", "value": "261-4403407-6187609", "domain": ".amazon.fr", "path": "/"},
    {"name": "lc-acbfr", "value": "fr_FR", "domain": ".amazon.fr", "path": "/"},
    {"name": "x-acbfr", "value": "WGuMR7aKNVhplLzJ9bcxOESKv0169Lp7feIyWddVGpQ0oeF@29ZCR8BP7rb78Fuv", "domain": ".amazon.fr", "path": "/"},
    {"name": "sst-acbfr", "value": "Sst1|PQFix5BDtFQ4pR7JYh_O2Nn7DPy9OM8U_QFjiwKNTpImx_tfiwAepgHQdk8iRFFMCZzrnFtIKOYIGKJVTFc2xAVTRBWxDCE9SnrVqjpM7zBFbNY6Y4rK8oApTTo88sAb0tPAdhLhfMEbyZiX4r53Oloj6yJEW4MYMCCcr1j8CWIU_uFhM4lVGmQXqAxytbJyeWyNTMXtRJmFuliEKyqeTIjJsJSAUTc1bJO3Y_Lco5irS8GfIMCQzc2EibB2K4fxp3h2xaRIABS76dt1hmOog0mr6Hjo5lIFa7JCRISBNhHkhW__b9vpBiY4q6Ro1Ne_tQaHrf0sl2m-Vy-Da7BmVmWU0RjDrZdJ31bBnn8XyHZqncY", "domain": ".amazon.fr", "path": "/"},
    {"name": "i18n-prefs", "value": "EUR", "domain": ".amazon.fr", "path": "/"},
    {"name": "session-id-time", "value": "2082787201l", "domain": ".amazon.fr", "path": "/"},
    {"name": "sess-at-acbfr", "value": "E7HFbJdlj/XTplurzOA/OxIJPBKtokRg16FujGoKlxI=", "domain": ".amazon.fr", "path": "/"},
    {"name": "at-acbfr", "value": "Atza|IwEBIKao3ulAG4MCXzlcJg0W_lW92bfTXg4mLpP-f4lOUvIr_v9CwhD9_QP4VtvuDPVX1DeWQpk2xWV5bLkKMbIpa3sTahF8lXcdt_-zwZRm-GEsD13PJ4rKi6Agp-8fKLveNZuc9Qj7vyL1ryVgt21ReUewM54CT11n9dsi_ns_ITlh0lF2KJfJWrWmk2jWR2H_hl1Cnl3IAYFs3TEaOBB7xCBaNADuGNcK8Kd7EcngGdz2QGZTidbVU8yFbeuApoNxw7zrW0M0oX-DTLM1SRN7IpOFmVfSan9876LcyHw62XwRYBUphQTZVA7o_aomU0cE23i8z9UP-2XaxlS_tSOZwrH-", "domain": ".amazon.fr", "path": "/"},
    {"name": "session-token", "value": "Dr3z32r8ojNY0ZJijHvlmwv4Kwnyr5DWsq60JOvgje32OO6CuLLc/BBArWNFxA0pbaBmC/RLQerXToMHwKmUUenlUce3umjmebdb6REGcJ6xmHEw0EJtO5DFIE2X3nb4yqHf6G0c3El3BvQNFky15lusg/LPbyfehTUmhTgBiO4sJ28rwlBGxY7D2vAxp6Sn5hZ7gMN6NiuBncRjRYFtwv1usbZYUYKvysyjqhDjhUhuSwq17QerQ/hj8I+k4BU0nur9XsmuWRSdQcD5hp/s7LJ4hHhme7X8f4kTGXv4KjQARQKv4EzRpmk93SyljtM9SdbvxYwcYgjRAyu/gQ79dfWfhpdMrxC3uWlGZLvCN7yreWRL95+6GjquE2RzH0z0YmTpDTK6Lw+z1zfW+cEAHYnj08SI0TOklHyArpHzdPDjI0Y/g9xD1A==", "domain": ".amazon.fr", "path": "/"}
]

def get_price_from_amazon(playwright, url):
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies(cookies)  # Ajouter les cookies au contexte
        page = context.new_page()
        page.goto(url)

        # Attendre le chargement complet de la page
        page.wait_for_selector("#priceblock_ourprice, #priceblock_dealprice, .a-price .a-offscreen")

        # Rechercher les prix
        selectors = [
            "#priceblock_ourprice",
            "#priceblock_dealprice",
            ".a-price .a-offscreen"
        ]

        for selector in selectors:
            try:
                price = page.query_selector(selector)
                if price:
                    return price.inner_text().strip()
            except Exception:
                continue

        browser.close()
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération pour {url}: {str(e)}")
        return None

output_file = "amazon_prices.csv"
# Assurez-vous que le fichier est bien enregistré dans le répertoire courant
output_file_path = os.path.join(os.getcwd(), output_file)

with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Product Link", "Price"])

    with sync_playwright() as playwright:
        for link in product_links:
            price = get_price_from_amazon(playwright, link)
            writer.writerow([link, price])
            print(f"Lien : {link}, Prix : {price}")

print(f"Données enregistrées dans {output_file}")
