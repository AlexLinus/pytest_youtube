import pytest
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from django.contrib.auth.models import User, AnonymousUser

from products.views import product_detail

# scope='module' говорит нам, чтобы инициировалась фикстура только 1 раз.
# т.к иначе, она будет вызываться для каждого теста. Тем самым если будет 100 тестов.
# использующих эту фикстуру. То будет 100 раз запрос в базу, или просто инициализроваться что-то.

@pytest.fixture(scope='module')
def factory():
    print('FACTORY INSTANTIATED')
    return RequestFactory()

# вместо @pytest.mark.django_db, можно передавать db как фикстуру

@pytest.fixture
def product(db):
    return mixer.blend('products.Product')


def test_product_detail_authenticated(factory, product):
    # т.к у нас создается тестовая бд. То там продуктов нет.
    # И перед тем как проверять, нужно создать продукт, чтобы было что брать по pk

    path = reverse('product_detail', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = mixer.blend(User)

    # передаем во вьюху нашу
    response = product_detail(request, pk=1)
    assert response.status_code == 200
    assert False
# вместо @pytest.mark.django_db, можно передавать db как фикстуру


def test_product_detail_unauthenticated(factory, product):
    path = reverse('product_detail', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = product_detail(request, pk=1)
    # т.к только для авторизованных вьюха расчитана.
    # то она будет возвращать 302 статус редиректа, на страницу авторизации
    # temporary redirect
    assert response.status_code == 302
    # проверяем, редиректит ли на url авторизации содержится ли accounts/login/ в url
    assert 'accounts/login/' in response.url
    assert False