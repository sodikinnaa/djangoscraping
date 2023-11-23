from django.urls import path
from . import views

urlpatterns = [
    path("universitas/", views.universitas, name="universitas"),
    path("universitas/<int:id>", views.detail_sitasi, name="detail_sitasi"),
    path("universitas/add", views.insert_univ, name="insert_univ"),
    path("universitas/berhasil", views.done, name="done"),
    path("universitas/scrape/<int:id>", views.scrape_dosen, name="detail_sitasi"),
    path("download-csv/<int:id>", views.download_csv, name="download_csv"),
]
