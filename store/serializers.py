from rest_framework import serializers

from store.models import Product, ShoppingCartItem


class CartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, max_value=100)

    class Meta:
        model = ShoppingCartItem
        fields = ('product', 'quantity')


class ProductSerializer(serializers.ModelSerializer):
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    cart_items = serializers.SerializerMethodField()
    price = serializers.DecimalField(min_value=1.00, max_value=100000,
                                     max_digits=None, decimal_places=2)
    sale_start = serializers.DateTimeField(
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:01 PM 16 April 2022"',
        style={'input_type': 'text', 'placeholder': '12:01 AM 28 July 2022'},
    )
    sale_end = serializers.DateTimeField(
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:01 PM 16 April 2022"',
        style={'input_type': 'text', 'placeholder': '12:01 AM 28 July 2022'},
    )
    photo = serializers.ImageField(default=None)
    warranty = serializers.FileField(read_only=True, default=None)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'price', 'sale_start', 'sale_end',
            'is_on_sale', 'current_price', 'cart_items', 'price', 'photo')

        # def to_representation(self, instance):
        #     data = super().to_representation(instance)
        #     data['is_on_sale'] = instance.is_on_sale()
        #     data['current_price'] = instance.current_price()
        #     return data

    def get_cart_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        return CartItemSerializer(items, many=True).data

    def update(self, instance, validated_data):
        if validated_data.get('warranty', None):
            instance.description += '\n\nWarranty Information:\n'
            instance.description += b'; '.join(
                validated_data['warranty'].readlines()
            ).decode()
        return instance


class ProductStatSerializer(serializers.Serializer):
    stats = serializers.DictField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
        )
    )
