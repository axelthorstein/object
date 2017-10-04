import requests


class GraphQL:

    def request(query):
        return requests.post(
            'https://axelteststore.myshopify.com/api/graphql',
            data=query,
            headers={'Content-Type': 'application/graphql',
                     'X-Shopify-Storefront-Access-Token': '98b4b577fbc417686bc9354af95c735b'}).json()

    def get_products():
        products = {}
        all_products = requests.get("https://axelteststore.myshopify.com/admin/products.json",
                                    auth=("e7759a3699a682d55e2c25991596e3cc",
                                          "c586e1e6cf85d7a25e0df45ee8f66204")).json()
        for product in all_products["products"]:
            products[product['handle']] = GraphQL.get_product(product['handle'])

        return products

    def get_product(product_name):
        query = '{shop {productByHandle(handle: "' + product_name + '") {id}}}'
        return GraphQL.request(query)

    def get_graphql_variant():
        query = 'mutation {checkoutCreate(input: {lineItems: [{\
                variantId: "Z2lkOi8vc2hvcGlmeS9Qcm9kdWN0VmFyaWFudC8zNTQ1MDE0MDQxOA==", quantity: 1 }]})\
                {checkout {id webUrl lineItems(first: 5) {edges {node {title quantity}}}}}}'
        return GraphQL.request(query)
