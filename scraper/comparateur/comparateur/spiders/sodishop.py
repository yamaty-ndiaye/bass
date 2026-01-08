import scrapy
from comparateur.items import ProductItem

class SodishopSpider(scrapy.Spider):
    name = "sodishop"
    start_urls = ['https://www.sodishop.com/product-category/telephones/iphone/']

    def parse(self, response):
        for product in response.css('li.product'):
            item = ProductItem()
            
            # Titre (qui marche déjà bien)
            item['title'] = product.css('h2.woocommerce-loop-product__title::text').get().strip()
            
            # PRIX : On prend tout le texte dans la zone de prix, c'est plus sûr
            # On cherche n'importe quel bdi ou span qui contient le montant
            raw_price = product.css('.price bdi::text').get()
            if not raw_price:
                 raw_price = product.css('.price .amount::text').get()
            
            item['price'] = raw_price.strip() if raw_price else "Prix non trouvé"
            
            item['url'] = product.css('a.woocommerce-LoopProduct-link::attr(href)').get()
            item['source'] = 'Sodishop'
            
            yield item