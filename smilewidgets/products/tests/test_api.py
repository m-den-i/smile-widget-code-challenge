from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Product, GiftCard, ProductPriceGroup, ProductPrice


class BaseApiTestCase(APITestCase):
    # SetUpClass is used because models are read-only
    @classmethod
    def setUpClass(cls):
        super(BaseApiTestCase, cls).setUpClass()
        cls.products = Product.objects.bulk_create([
            Product(**dt) for dt in ({
                "name": "Big Widget",
                "code": "big_widget",
                "price": 100000
            }, {
                "name": "Small Widget",
                "code": "sm_widget",
                "price": 9900
            })
        ])
        GiftCard.objects.create(**{
            "code": "10OFF",
            "amount": 1000,
            "date_start": "2018-07-01",
            "date_end": None
        })
        cls.now = datetime.now().date()

    def test_api(self):
        resp = self.client.get('/api/get-price/', data={'date': self.now, 'productCode': 'big_widget'})
        self.assertEqual(resp.data['price'], 100000)

    def test_gift_card(self):
        resp = self.client.get('/api/get-price/', data={
            'date': self.now,
            'productCode': 'sm_widget',
            'giftCardCode': '10OFF'
        })
        self.assertEqual(resp.data['price'], 8900)

    def test_invalid_gift_card_code(self):
        resp = self.client.get('/api/get-price/', data={
            'date': self.now,
            'productCode': 'sm_widget',
            'giftCardCode': 'test'
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_outdated_gift_card_code(self):
        resp = self.client.get('/api/get-price/', data={
            'date': self.now - timedelta(days=365),
            'productCode': 'sm_widget',
            'giftCardCode': '10OFF'
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_price_override(self):
        pg = ProductPriceGroup.objects.create(name='Black Fri', date_start=self.now - timedelta(days=7))
        ProductPrice.objects.create(product=self.products[1], price_group=pg, value=3000)
        resp = self.client.get('/api/get-price/', data={
            'date': self.now,
            'productCode': 'sm_widget',
            'giftCardCode': '10OFF'
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['price'], 2000)
