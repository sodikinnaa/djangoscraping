from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpRequest
from .models import Universitas
from .models import Detail_cited
from .helper import param_view

# Create your views here.
def universitas(request):
    data = Universitas.objects.all().values()
    template =  loader.get_template('all_univ.html')
    context = {
        'univ': data,
    }
    return HttpResponse(template.render(context, request))

def detail_sitasi(request, id):
    data = Detail_cited.objects.filter(fk_url_univ=id)

     # Menggunakan get_object_or_404 untuk memastikan universitas dengan ID tertentu ada
    universitas = get_object_or_404(Universitas, id=id)

    # Mengambil field url_universitas dari objek universitas
    url_universitas = universitas.url_univ
    template = loader.get_template('sitasi_detail.html')
    context = {
        'dosen': data,
        'url': id,
    }
    return HttpResponse(template.render(context, request))

def scrape_dosen(request, id):
    param_view(id)
    # data = Universitas.objects.filter(id=url_univ)
    # url = data.url_univ
    # template = loader.get_template('sitasi_detail.html')
    # return HttpResponse(template.render(request))
    return HttpResponse("berhasil jalan")
    