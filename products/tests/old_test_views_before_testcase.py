import pytest
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from django.contrib.auth.models import User, AnonymousUser

from products.views import product_detail


@pytest.mark.django_db
class TestViews:

    def test_product_detail_authenticated(self):
        # т.к у нас создается тестовая бд. То там продуктов нет.
        # И перед тем как проверять, нужно создать продукт, чтобы было что брать по pk
        mixer.blend('products.Product')
        path = reverse('product_detail', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        # передаем во вьюху нашу
        response = product_detail(request, pk=1)
        assert response.status_code == 200

    def test_product_detail_unauthenticated(self):
        mixer.blend('products.Product')
        path = reverse('product_detail', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = product_detail(request, pk=1)
        # т.к только для авторизованных вьюха расчитана.
        # то она будет возвращать 302 статус редиректа, на страницу авторизации
        # temporary redirect
        assert response.status_code == 302
        # проверяем, редиректит ли на url авторизации содержится ли accounts/login/ в url
        assert 'accounts/login/' in response.url
