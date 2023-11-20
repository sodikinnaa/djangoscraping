from django.contrib import admin
from .models import Universitas
from .models import Detail_cited

# from .models import Detail_cited


# Register your models here.
class UniversitasAdmin(admin.ModelAdmin):
    list_display = (
        "nama_univ",
        "url_univ",
        "total_sitasi",
    )


class detail_sitasi(admin.ModelAdmin):
    list_display = (
        "nama_dosen",
        "afiiliation",
        "email",
        "cited_by",
        "urldosen",
    )


admin.site.register(Universitas, UniversitasAdmin)
admin.site.register(Detail_cited, detail_sitasi)
