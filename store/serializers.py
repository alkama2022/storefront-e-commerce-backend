from rest_framework import serializers

class productSerializer(serializers.Serializer):
  id = serializers.IntegerField()
  title = serializers.CharField(max_length=255)
  price = serializers.DecimalField(max_digits=6,decimal_places=2)