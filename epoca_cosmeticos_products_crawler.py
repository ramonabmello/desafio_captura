# Meu código é pep8? Sim, na medida do possível
import csv
import logging
from itertools import count

import requests
from requests.exceptions import ConnectionError

from bs4 import BeautifulSoup
# O que é logging? Pq usar?
"""
Logging é um modulo de Python que registra eventos ocorridos quando o software
é executado. No caso, é utilizado para informar erros que podem ocorrer no
crawler.
"""
# O que é itertools e count? Pq usar?
"""
Itertools é um módulo de Python que produz um valor diferente a cada vez que o
acessamos. No caso de count, deve ser usado dentro de um loop que pare o fluxo,
pois gera valores infinitos. itertools.count() funciona como um contador,
retornando números em ordem a partir do número dado como inicial.
"""
# Pq usar BeautifulSoup?
"""
BeautifulSoup é uma biblioteca Python usada para puxar dados de um arquivo HTML
"""


# Pq criei funções? Pq elas estão nessa ordem?
"""
As funções são criadas para separar o código em blocos de execução, podendo ser
repetidas quantas vezes forem necessárias, sem precisar repetir o código.
"""


def save_csv(file_name, products):
    """
    A função save_csv() escreve e salva um arquivo .csv, que separa os
    elementos por vírgula. São 3 colunas: "Product's Name", "Title of Page" e
    "URL", e em cada linha acrescenta um elemento de products.
    """
    with open(file_name, 'w', newline='') as captura:
        # Pq usar Context Manager?
        """
        Context Manager define o tempo de execução de um bloco de código ao
        executar uma instrução with.
        """
        # O que é open?
        """
        open() é usado para abrir um arquivo existente ou criar um novo,
        dependendo do modo como foi aberto. Utilizando o modo 'w', o arquivo
        será aberto em modo de escrita, podendo incluir conteúdo ao arquivo.
        """
        write = csv.writer(captura, delimiter=',', quoting=csv.QUOTE_ALL)
        # Pq usar quoting?
        """
        quoting controla quando o quote deve ser gerado pelo escritor e
        reconhecido pelo leitor. No caso, alguns nomes de produtos ou títulos
        de páginas são separados por ';', então o QUOTE_ALL instrui o escritor
        a não definir o ';' como delimitador.
        """
        write.writerow(["Product's Name", "Title of Page", "URL"])
        write.writerows(products)


def get_page_title(product_page_html):
    """
    A função get_page_title() encontra no HTML da página do produto a tag
    "title" e retorna o texto da tag, que é o Título da Página.
    """
    return product_page_html.find('title').text
    # O que é find?
    """
    find() é um método em BeautifulSoup utilizado para encontrar o resultado,
    que contenha o parâmetro oferecido, dentro do HTML parseado.
    """
    # O que é .text?
    """
    .text retorna o conteúdo da tag encontrada no HTML
    """


def get_product_name(product_page_html):
    """
    A função get_product_name() encontra no HTML da página do produto a tag
    "div" que está na classe "productName", e retorna o texto da tag, que é o
    Nome do Produto.
    """
    return product_page_html.find('div', attrs={'class': 'productName'}).text
    # Pq usar find ao invés de find_all?
    """
    O método find_all() scaneia todo o documento em busca dos resultados, mas
    às vezes queremos somente um resultado. Quando conhecemos o documento e
    sabemos que só tem um resultado possível, podemos utilizar o método find().
    """


def get_products_from_page(search_page_html):
    """
    A função get_products_from_page() parseia o conteúdo do HTML da página de
    pesquisa utilizando BS4, encontra e retorna todas as tags "a" com
    "shelf-default__link".
    """
    page_parser = BeautifulSoup(search_page_html, 'html.parser')
    # O que é html.parser?
    """
    html.parser é um módulo de Python usado para parsear arquivos de texto em
    HTML.
    """
    return page_parser.find_all('a', 'shelf-default__link')
    # O que é find_all?
    """
    find_all() é um método em BeautifulSoup para encontrar todos os resultados,
    que contenham os parâmetros oferecidos, dentro do HTML parseado.
    """


def get_html(url):
    """
    A função get_html() faz a requisição da URL e retorna o conteúdo do HTML
    dessa URL.
    """
    response = requests.get(url)
    return response.content


if __name__ == '__main__':
    """
    __name__ == '__main__' diferencia se o código está sendo executado pelo
    terminal ou como um módulo Python importado.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    products = set()
    # O que é set? Pq usar?
    """
    products atribui um conjunto das propriedades dos produtos. set() é
    utilizado para não haver elementos duplicados na hora de salvar o arquivo
    .csv.
    """
    categories = ['f1000001', 'f1000037', 'f1000004', 'f1000130', 'f1000089',
                  'f1000070', 'f1000013']
    """
    categories atribui uma lista com o código de todas as categorias utilizadas
    no site Época Cosméticos.
    """
    for category in categories:
        # Para uma categoria dentro da lista de categorias
        for page_number in count(1):
            # E para um número de página dentro do contador
            product_page_url = f'https://www.epocacosmeticos.com.br/buscapagina?fq=C%3a%2{category}%2f&PS=16&sl=f804bbc5-5fa8-4b8b-b93a-641c059b35b3&cc=4&sm=0&PageNumber={page_number}'
            """
            A f-string em product_page_url substitui o valor da categoria e do
            número da página até que não haja mais conteúdo no HTML, então pula
            para a próxima categoria.
            """
            # O que é f-string? Pq usar?
            """
            f-string é uma string que pode ser formatada. Usamos para
            substituir valores dentro de uma string por valores de uma
            variável. É similar ao método .format(), mas muito mais simples de
            escrever e ler.
            """
            try:
                # Pq uso try/except?
                """
                Para poder levantar exceções no código ao invés de quebrar com
                erro.
                """
                search_page_html = get_html(product_page_url)
                """
                search_page_html faz a requisição da URL em product_page_url
                e retorna o conteúdo do HTML da página de pesquisa.
                """
            except ConnectionError:
                # O que é ConnectionError? Pq usar?
                """
                ConnectionError é uma exceção da biblioteca requests.
                É levantada quando há algum problema com a conexão.
                """
                logger.info(f"Couldn't get the content for {product_page_url}")
                continue
                """
                Caso não consiga conexão com a URL requerida, o erro é
                informado e segue para o else, para verificar se o conteúdo do
                HTML é vazio.
                """
                # Pq usar continue?
                """
                continue é usado dentro de um loop para interromper a execução
                de um ciclo e seguir para o próximo, sem interromper todo o
                loop.
                """
            else:
                if search_page_html == b'':  # b'' = Conteúdo HTML vazio
                    break
                """
                Se o conteúdo do HTML é vazio, significa que não existem mais
                produtos cadastrados para aquela categoria. Então o loop para e
                pula para a requisição da primeira página da próxima categoria
                da lista.
                """
                # Pq usar break?
                """
                break é usado dentro de um loop para interromper a execução do
                loop, seguindo com a execução do programa.
                """

            products_anchor_tags = get_products_from_page(search_page_html)
            """
            products_anchor_tags retorna todas as tags "a" com
            "shelf-default__link" da página de pesquisa.
            """

            for product_anchor_tag in products_anchor_tags:
                # Para cada tag de produto dentro das tags de produtos
                product_url = product_anchor_tag.attrs['href']
                # product_url atribui a URL do produto
                try:
                    product_page_html = get_html(product_url)
                    """
                    product_page_html faz a requisição da URL do produto e
                    retorna o conteúdo do HTML da página do produto.
                    """
                except ConnectionError:
                    logger.info(f"Couldn't get the content for {product_url}")
                    continue
                    """
                    Caso não consiga conexão com a URL requerida, o erro é
                    informado e segue para a requisição da próxima página de
                    produto.
                    """

                product_html_parser = BeautifulSoup(product_page_html, 'html.parser')
                """
                product_html_parser parseia o conteúdo do HTML da página de
                produto utilizando BS4.
                """

                try:
                    product_name = get_product_name(product_html_parser)
                    # product_name retorna o Nome do Produto
                except AttributeError:
                    # O que é AttributeError?
                    """
                    AttributeError é uma exceção que é levantada quando tenta
                    acessar um atributo em um objeto que não possui aquele
                    atributo. No caso, quando a função get_product_name()
                    retorna None, None não possui o atributo text.
                    """
                    logger.info(f"For some reason {product_url} is different from the others and we couldn't retrieve the product name.")
                    continue
                    """
                    Caso o HTML da página de produto seja diferente e não
                    utilize as mesmas tags para nomear o produto, este erro é
                    informado e segue para a próxima página de produto.
                    """

                try:
                    page_title = get_page_title(product_html_parser)
                    # page_title retorna o Título da Página de produto
                except AttributeError:
                    logger.info(f"For some reason {product_url} is different from the others and we couldn't retrieve the product name.")
                    continue
                    """
                    Caso o HTML da página de produto seja diferente e não
                    utilize as mesmas tags para nomear o produto, este erro é
                    informado e segue para a próxima página de produto.
                    """

                products_properties = (
                    product_name,
                    page_title,
                    product_url
                )
                """
                products_properties atribui uma tupla (lista imutável) com o
                nome do produto, o título e a URL da página do produto.
                """

                products.add(products_properties)
                # products recebe os valores de products_properties

    save_csv('epoca_cosmeticos_products.csv', products)
    """
    Escreve e salva o arquivo epoca_cosmeticos_products.csv com os elementos de
    products.
    """
