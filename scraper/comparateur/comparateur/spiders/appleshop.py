import scrapy
from comparateur.items import ProductItem

class AppleshopSpider(scrapy.Spider):
    name = "appleshop"
    start_urls = ['https://www.appleshop.sn/index.php/categorie-produit/iphone/']

    def parse(self, response):
        # 1. Extraction des produits de la page actuelle
        for product in response.css('li.product'):
            item = ProductItem()
            item['title'] = product.css('h2.woocommerce-loop-product__title::text').get().strip()
            
            # Gestion du prix promo vs normal (vu sur image_f20b9e.png)
            raw_price = product.css('ins span.woocommerce-Price-amount bdi::text').get()
            if not raw_price:
                raw_price = product.css('span.woocommerce-Price-amount bdi::text').get()
            
            if raw_price:
                item['price'] = "".join(filter(str.isdigit, raw_price))
            
            item['url'] = product.css('a.woocommerce-LoopProduct-link::attr(href)').get()
            item['source'] = 'Apple Shop'
            yield item

        # 2. Gestion de la pagination (vu sur image_fbee01.png)
        # On cherche le bouton "Suivant" (souvent classé 'next' ou simplement le lien après la page courante)
        next_page = response.css('a.next.page-numbers::attr(href)').get()
        
        # Si on ne trouve pas de classe 'next', on prend l'URL du lien "Page 2" que tu as montré
        if not next_page:
            # On cherche spécifiquement le lien vers la page 2, 3, etc.
            # Scrapy s'occupera de ne pas boucler à l'infini grâce à son filtre de duplicata
            next_pages = response.css('a.page-numbers::attr(href)').getall()
            for href in next_pages:
                yield response.follow(href, self.parse)
        else:
            yield response.follow(next_page, self.parse)