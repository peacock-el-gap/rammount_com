import json
import logging
import math
import pandas as pd
import requests
import re
import sys

MAX_LIMIT = 70

log = logging.getLogger(__name__ )
log_handler = logging.StreamHandler(stream=sys.stdout)
log_handler.setLevel(logging.DEBUG)
log.addHandler(log_handler)
log.setLevel(logging.DEBUG)


def get_results_from_rammount(collection_scope=0, page=1, limit=MAX_LIMIT):
    callback = "AAAA"
    url = f"https://services.mybcapps.com/bc-sf-filter/filter?shop=rammount.myshopify.com&page={page}&limit={limit}&collection_scope={collection_scope}&callback={callback}"
    result = requests.get(url).content.decode('utf-8')
    m = re.search(f"(.*{callback}\()(.*)(\);)", result)
    json_object = {"__result__":"__something_went_wrong__"}
    if m:
        json_data = m.group(2)
        json_object = json.loads(json_data)
    return json_object


def get_total_product_numner(collection_scope=0):
    return get_results_from_rammount(collection_scope=collection_scope, limit=10)["total_product"]


def get_products(collection_scope=0, page=1, limit=MAX_LIMIT):
    products = []
    for p in get_results_from_rammount(collection_scope, page, limit)["products"]:
        products.append(
            {
                'sku':          p['skus'][0], 
                'title':        p['title'],
                'body_html':    p['body_html'],
                'collections':  pd.DataFrame(p['collections']).drop('sort_value', axis=1).drop('template_suffix', axis=1).drop_duplicates().to_dict('records'),
                'id':           p['id'],
                'handle':       p['handle'],
                'product_type': p['product_type']
            }
        )    
    return products


def get_all_products(collection_scope=0):
    total_number_of_products = get_total_product_numner(collection_scope=collection_scope)
    number_of_pages = math.ceil(total_number_of_products / MAX_LIMIT)

    log.debug(f"total number of products {'' if collection_scope == 0 else f'(for collection_scope={collection_scope}) '}= {total_number_of_products}")
    log.debug(f"number of pages = {number_of_pages}")

    products = []
    for p in range(1, number_of_pages + 1):
    # for p in range(1, 2 + 1):
        log.debug(f"page: {p}")
        products.extend(get_products(collection_scope=collection_scope, page=p))
    return products


def get_collections(products):
    collections = []
    for product in products:
        collections.extend(product["collections"])
    collections_distinct = pd.DataFrame(collections).drop_duplicates().to_dict('records')
    return collections_distinct




#====================================================================

def main():
    products = get_all_products()
    collections = get_collections(products=products)
    log.debug(f"number of gathered products: {len(products)}")

    # print(json.dumps(products, indent=2))

    products_df = pd.json_normalize(
        products, 
        record_path="collections",
        record_prefix="collections_", 
        meta=[
            'sku', 
            'title',
            'body_html',
            'id',
            'handle',
            'product_type'
        ]
    )

    collections_df = pd.DataFrame(collections)

    products_df.to_csv(
        './products.csv', 
        encoding='utf-8',
        index=False
    )

    collections_df.to_csv(
        './collections.csv', 
        encoding='utf-8',
        index=False
    )


if __name__ == '__main__':
    main()