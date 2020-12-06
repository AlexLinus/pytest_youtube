from products.models import Product
import pytest
from mixer.backend.django import mixer


@pytest.fixture
def product(request, db):
    return mixer.blend('products.Product', quantity=request.param)


# если стоит indirect = True,то это значит что мы параметризируем нашу фикстуру.
@pytest.mark.parametrize('product', [1], indirect=True)
def test_product_is_in_stock(product):
    # мы можем указать парамтры, которые мы хотим задать сами. В данном случае.
    # quantity = 1
    product = mixer.blend('products.Product', quantity=1)
    assert product.is_in_stock == True


@pytest.mark.parametrize('product', [1], indirect=True)
def test_product_not_in_stock(product):
    product = mixer.blend('products.Product', quantity=0)
    assert product.is_in_stock == False
