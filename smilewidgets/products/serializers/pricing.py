from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models.mixins import DateFramedMixin
from ..models import GiftCard


class ProductPriceParametersSerializer(serializers.Serializer):
    productCode = serializers.CharField(required=True, source='product_code')
    date = serializers.DateField(allow_null=False, required=True, source='price_date')
    giftCardCode = serializers.CharField(allow_blank=False, required=False, source='gift_card_code')

    def validate(self, attrs):
        gift_card_code = attrs.get('gift_card_code', None)
        if gift_card_code:
            in_dates = DateFramedMixin.date_intersections(attrs['price_date'])
            if not GiftCard.objects.filter(in_dates, code=gift_card_code).exists():
                raise ValidationError('Gift card is not valid')
        return attrs
