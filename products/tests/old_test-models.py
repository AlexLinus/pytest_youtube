from products.models import Product
import pytest
from mixer.backend.django import mixer


# если не укажем этот декоратор, то pytest не будет иметь доступ к базе данных
@pytest.mark.django_db
class TestModels:

    def test_product_is_in_stock(self):
        # мы можем указать парамтры, которые мы хотим задать сами. В данном случае.
        # quantity = 1
        product = mixer.blend('products.Product', quantity=1)
        assert product.is_in_stock == True

    def test_product_not_in_stock(self):
        product = mixer.blend('products.Product', quantity=0)
        assert product.is_in_stock == False
