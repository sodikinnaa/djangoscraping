from django.contrib import admin
from .models import Universitas
from .models import Detail_cited

# from .models import Detail_cited


# Register your models here.
class UniversitasAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nama_univ",
        "url_univ",
        "total_sitasi",
    )


class detail_sitasi(admin.ModelAdmin):
    list_display = (
        "id_dosen",
        "nama_dosen",
        "afiiliation",
        "email",
        "cited_by",
        "urldosen",
        "fk_url_univ",
    )


admin.site.register(Universitas, UniversitasAdmin)
admin.site.register(Detail_cited, detail_sitasi)
