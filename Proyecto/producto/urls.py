
from django.urls import path
from .views import (
    ProductoCreateView,
    ProductoDetailView,


)

# app_name = 'productos'

# urlpatterns = [
#     # path('', ArticleListView.as_view(), name='article-list'),
#     path('create/', ProductoCreateView.as_view(), name='procuto-create', ),
#     path('<int:id>/', ProductoDetailView.as_view(), name='producto-detail'),
#     path('<int:id>/update/', ArticleUpdateView.as_view(), name='article-update'),
#     path('<int:id>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
# ]
