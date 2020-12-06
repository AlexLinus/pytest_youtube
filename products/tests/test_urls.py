from django.urls import reverse, resolve


class TestUrls:

    def test_detail_url(self):
        path = reverse('product_detail', kwargs={'pk': 1})
        assert resolve(path).view_name == 'product_detail'
