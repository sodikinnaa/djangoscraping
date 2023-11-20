
from django.urls import path
from . import views
urlpatterns = [
    path('universitas/', views.universitas, name='universitas'),
    path('universitas/<int:id>', views.detail_sitasi, name='detail_sitasi'),
    path('universitas/scrape/<int:id>', views.scrape_dosen, name='detail_sitasi'),
]