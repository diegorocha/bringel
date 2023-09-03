from rest_framework.viewsets import ModelViewSet

from store.api.serializers import TagSerializer
from store.models import Tag


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
