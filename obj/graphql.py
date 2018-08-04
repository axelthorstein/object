import requests

BASE_URL = 'https://axelteststore.myshopify.com'


class GraphQL:
    """An interface for GraphQL endpoints."""

    @staticmethod
    def request(query):
        return requests.post(
            BASE_URL + '/api/graphql',
            data=query,
            headers={
                'Content-Type':
                'application/graphql',
                'X-Shopify-Storefront-Access-Token':
                '98b4b577fbc417686bc9354af95c735b'
            }).json()

    @staticmethod
    def get_products():
        products = {}
        all_products = requests.get(
            BASE_URL + '/admin/products.json',
            auth=('e7759a3699a682d55e2c25991596e3cc',
                  'c586e1e6cf85d7a25e0df45ee8f66204')).json()
        for product in all_products["products"]:
            products[product['handle']] = GraphQL.get_product(product['handle'])

        return products

    @staticmethod
    def get_product(product_name):
        query = '{shop {productByHandle(handle: "' + product_name + '") {id}}}'

        return GraphQL.request(query)

    @staticmethod
    def get_product_variants(product_name):
        query = '{ shop { productByHandle(handle: "' + product_name + '")\
                 { variants(first:3) { edges { node { id }}}}}}'

        return GraphQL.request(query)

    @staticmethod
    def build_line_items(variants):
        variants = variants['data']['shop']['productByHandle']['variants'][
            'edges']
        line_items = "["
        for variant in variants:
            line_items += '{ variantId: "' + variant['node']['id'] + '", quantity: 1 }'

        return str(line_items + ']')

    @staticmethod
    def create_checkout(product_name):
        variants = GraphQL.get_product_variants(product_name)
        line_items = GraphQL.build_line_items(variants)
        query = (
            'mutation {checkoutCreate(input: {lineItems: ' + line_items +
            '}){checkout {id webUrl lineItems(first: 5) {edges {node {title quantity}}}}}}'
        )
        request = GraphQL.request(query)
        checkout = request['data']['checkoutCreate']['checkout']['webUrl']

        return checkout
