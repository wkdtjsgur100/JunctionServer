from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin

from aitojunction.models import Place, Cuisine, UserLike
from import_export import resources


class PlaceResource(resources.ModelResource):

    class Meta:
        model = Place


@admin.register(Place)
class PlaceAdmin(ImportExportModelAdmin):
    resource_class = PlaceResource
    list_display = ('id', 'aito_id', 'name', 'address', 'country', )


class CuisineResource(resources.ModelResource):

    class Meta:
        model = Cuisine


@admin.register(Cuisine)
class CuisineAdmin(ImportExportModelAdmin):
    resource_class = CuisineResource
    list_display = ('id', 'name')


@admin.register(UserLike)
class UserLikeAdmin(ModelAdmin):
    list_display = ('id', 'user_id', 'place_name', 'is_super_like')
    list_select_related = ['place', ]

    def place_name(self, instance):
        return instance.place.name

    place_name.short_description = 'Place Name'