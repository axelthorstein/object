httpChannel.setRequestHeader("X-Shopify-Storefront-Access-Token", "98b4b577fbc417686bc9354af95c735b", false);
curl https://e7759a3699a682d55e2c25991596e3cc:c586e1e6cf85d7a25e0df45ee8f66204@axelteststore.myshopify.com/admin/products.json | python -m json.tool

function getProduct() {
const shopClient = ShopifyBuy.buildClient({
  accessToken: '98b4b577fbc417686bc9354af95c735b',
  appId: '6',
  domain: 'axelteststore.myshopify.com'
});
console.log(shopClient)
// fetch a product using resource id
shopClient.fetchAllProducts()
.then(function(products) {
  // all products in store
}).catch(function () {
    console.log('Request failed');
  });
}
