from rest_framework import filters, mixins, viewsets


class BaseCategoryGenreViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class BaseUserTitleReviewCommentViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
