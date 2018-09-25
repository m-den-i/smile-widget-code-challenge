from django.db import models

from .mixins import DateFramedMixin
from .product import Product

CENTS_IN_USD = 100


class GiftCard(models.Model):
    code = models.CharField(max_length=30, unique=True)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)
    
    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / CENTS_IN_USD)


class ProductPriceGroup(DateFramedMixin):
    name = models.CharField(max_length=256, blank=True, help_text='Name of price offer')

    @classmethod
    def get_price_groups_for_date(cls, date):
        return cls.objects.filter(DateFramedMixin.date_intersections(date))

    def __str__(self):
        name = ' ({})'.format(self.name) if self.name else ''
        return '[{} to {}]{}'.format(self.date_start, self.date_end, name)


class ProductPrice(models.Model):
    price_group = models.ForeignKey(ProductPriceGroup, on_delete=models.CASCADE, related_name='prices')
    value = models.PositiveIntegerField(help_text='Price for the specified period')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')

    @classmethod
    def detect_total_price(cls, product, date, gift_card_code=None):
        # Detect possible price groups
        search_in_groups = ProductPriceGroup.get_price_groups_for_date(date)

        # It is not obvious which price should be applied in case when multiple prices exists
        # So, we take the price with lowest value
        override_price = cls.objects\
            .filter(price_group__in=search_in_groups, product=product)\
            .order_by('value')\
            .first()

        product_price = override_price.value if override_price else product.price

        # Detect if gift card should be applied
        if gift_card_code:
            gift_card = GiftCard.objects.get(code=gift_card_code)
            product_price -= gift_card.amount
        return product_price if product_price >= 0 else 0

    @property
    def price_usd(self):
        return self.value / CENTS_IN_USD

    def __str__(self):
        return '{}$ for product {}'.format(self.price_usd, self.product_id)

    class Meta:
        unique_together = ('price_group', 'product')
