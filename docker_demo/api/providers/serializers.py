from django.utils.timezone import now
from rest_framework import serializers
from providers.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()

    class Meta:
        model = Provider
        # fields = '__all__'
        fields = ('id', 'providerID', 'providerName', 'days_since_created')

    def get_days_since_created(self, obj):
        return (now() - obj.created).days
