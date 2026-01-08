import mysql.connector
import re

class ConversionPipeline:
    def open_spider(self, spider):
        self.connection = mysql.connector.connect(
            host='127.0.0.1', 
            user='root',
            password='root',
            database='comparateur_db',
            port=3306
        )
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        try:
            # 1. Nettoyage du prix
            price_raw = str(item['price']).replace('CFA', '').replace('.', '').replace(' ', '').replace('\xa0', '').strip()
            item['price'] = int(price_raw)
            
            # 2. Nettoyage INTELLIGENT du titre
            raw_title = item['title'].upper()
            
            # Extraction de la capacité (64GB, 128GB, etc.)
            capacity = ""
            # On cherche les chiffres suivis de GB ou GO ou Gb
            match_cap = re.search(r'(\d+)\s*(?:GB|GO|Gb|Puces|Tera)', raw_title, re.IGNORECASE)
            if match_cap:
                capacity = match_cap.group(1) + "GB"
                # Correction pour 1Tera -> 1TB
                if "TERA" in raw_title: capacity = "1TB"

            # Extraction du modèle (X, 11, 12 Pro, XS Max, etc.)
            model = ""
            # On cherche le mot iPhone suivi du modèle
            if "IPHONE" in raw_title:
                # Liste des modèles connus pour filtrer le reste du texte de Sodishop
                for m in ["16 PRO MAX", "16 PRO", "16 PLUS", "16", "15 PRO MAX", "15 PRO", "15 PLUS", "15", 
                          "14 PRO MAX", "14 PRO", "14 PLUS", "14", "13 PRO MAX", "13 PRO", "13 MINI", "13",
                          "12 PRO MAX", "12 PRO", "12 MINI", "12", "11 PRO MAX", "11 PRO", "11",
                          "XS MAX", "XS", "XR", "X", "8 PLUS", "8", "7 PLUS", "7", "SE"]:
                    if m in raw_title:
                        model = m
                        break
            
            # Reconstruction du titre final "Propre"
            if model and capacity:
                item['title'] = f"iPhone {model} {capacity}"
            elif model:
                item['title'] = f"iPhone {model}"
            
            # On harmonise l'écriture (ex: ProMax -> Pro Max)
            item['title'] = item['title'].replace("PROMAX", "PRO MAX").title()

            # 3. Insertion en base
            self.cursor.execute(
                "INSERT INTO articles (title, price, url, source) VALUES (%s, %s, %s, %s)",
                (item['title'], item['price'], item['url'], item['source'])
            )
            self.connection.commit()
            
        except Exception as e:
            spider.logger.error(f"Erreur nettoyage/insertion : {e}")
            
        return item

    def close_spider(self, spider):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'connection'):
            self.connection.close()