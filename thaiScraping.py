import requests
from bs4 import BeautifulSoup

baseUrl = 'https://thaishark.com.br/'

productlinks = []
page = 1
# Coleta de links de produtos
while True:
    r = requests.get(f'{baseUrl}collections/produtos?page={page}')
    soup = BeautifulSoup(r.content, 'lxml')
    thaiProducts = soup.find_all('div', class_="product-list product-list--collection product-list--with-sidebar")
    for item in thaiProducts:
        for link in item.find_all('a', href=True):
            productlinks.append(baseUrl + link['href'])
    
    page += 1

# Remover duplicatas da lista de links
    print(productlinks)
    productlinks = list(set(productlinks))

    # Coleta de informações de cada produto
    for link in productlinks:
        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'lxml')
            
            # Nome do produto
            name_tag = soup.find('h1', class_='product-meta__title heading h1')
            if name_tag:
                name = name_tag.text
                print(f'Nome: {name}')
            else:
                print('Nome não encontrado para o link:', link)
                continue
            
            # Preço do produto
            price_tag = soup.find('div', class_='price-list')
            if price_tag:
                price = price_tag.text.strip()
                print(f'Preço: {price}')
            else:
                print('Preço não encontrado para o link:', link)
                continue
            
            # Cores do produto
            colors = soup.find_all('div', class_='variant-swatch')
            print("Cores:")
            for itens in colors:
                for color_tag in itens.find_all('label', title=True):
                    print(color_tag['title'])
        except Exception as e:
            print(f'Erro ao processar o link {link}: {e}')
