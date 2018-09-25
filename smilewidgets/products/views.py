from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .serializers.pricing import ProductPriceParametersSerializer
from .models import ProductPrice, Product


class ProductPriceViewSet(generics.RetrieveAPIView):
    queryset = Product.objects.all()

    lookup_url_kwarg = 'product_code'
    lookup_field = 'code'

    def initial(self, request, *args, **kwargs):
        super(ProductPriceViewSet, self).initial(request, *args, **kwargs)
        filter_params = ProductPriceParametersSerializer(data=self.request.query_params)
        filter_params.is_valid(raise_exception=True)
        valid_params = filter_params.validated_data
        self.kwargs.update(valid_params)

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        gift_card_code = kwargs.get('gift_card_code', None)
        total_price = ProductPrice.detect_total_price(product, kwargs['price_date'], gift_card_code)
        return Response({'price': total_price}, status=HTTP_200_OK)
