# Create your views here.
import random
from functools import reduce

from pydash import py_
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from aitojunction.models import Place, UserLike
from aitojunction.serializers import PlaceSerializer, UserLikeSerializer

from aito.client import AitoClient
import aito.api as aito_api

class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Place.objects.all()


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    pagination_class = LimitOffsetPagination

    @property
    def top_recommendation(self):
        AITO_INSTANCE_URL = 'https://junction-test.aito.app'
        AITO_API_KEY = '4yaBPf9Kmk9xHNW30jBop7ieEmWMz2eSpmKyWvBi'

        client = AitoClient(instance_url=AITO_INSTANCE_URL, api_key=AITO_API_KEY)
        queries = self.request.query_params
        query_type = queries.get("type", "Mexican")

        limit = int(queries.get("limit", 0))
        rec_query = {
            "from": "ratings",
            "where": {
                "placeID.cuisine": query_type,
            },
            "recommend": "placeID",
            "goal": {"rating": 2},
        }
        if limit:
            rec_query['limit'] = int(limit)

        res = aito_api.recommend(client=client, query=rec_query)
        return res.json['hits']

    def get_queryset(self):
        return super().get_queryset().filter(
            aito_id__in=py_.map(self.top_recommendation, 'placeID')
        )

class UserLikeViewSet(ModelViewSet):
    queryset = UserLike.objects.select_related('place')
    serializer_class = UserLikeSerializer

    def get_queryset(self):
        queries = self.request.query_params
        user_id = queries.get("userID")

        if user_id is not None:
            return super().get_queryset().filter(user_id=user_id)
        else:
            return super().get_queryset()

    @action(detail=False)
    def like(self, request):
        queries = request.query_params
        user_id = queries.get("userID")
        place_id = queries.get("placeID")
        is_super_like = queries.get("isSuperLike", False)

        if not user_id or not place_id:
            return Response({"message": "Please give me userID or placeID!!"}, status=status.HTTP_400_BAD_REQUEST)

        if not Place.objects.filter(id=place_id).exists():
            return Response({"message": "placeID is wrong."}, status=status.HTTP_400_BAD_REQUEST)

        UserLike.objects.get_or_create(
            user_id=user_id, place_id=place_id, defaults={'is_super_like': is_super_like}
        )
        return Response(status=status.HTTP_201_CREATED)

