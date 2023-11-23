from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpRequest
from .models import Universitas
from .models import Detail_cited
from .helper import param_view, inserd_detail

# from django.core.universitas import call
from django.core.management import call_command
from django.http import JsonResponse
from django.utils import timezone

from .forms import add_universitas
import csv


# Create your views here.
def universitas(request):
    data = Universitas.objects.all().values()
    template = loader.get_template("all_univ.html")

    context = {
        "univ": data,
    }
    return HttpResponse(template.render(context, request))


def detail_sitasi_backup(request, id):
    data = Detail_cited.objects.filter(fk_url_univ=id)
    universitas = get_object_or_404(Universitas, id=id)

    cited = universitas.total_sitasi
    template = loader.get_template("sitasi_detail.html")
    context = {
        "dosen": data,
        "url": id,
        "universitas": universitas,
        "sitasi": cited,
    }
    return HttpResponse(template.render(context, request))


def detail_sitasi(request, id):
    # Mengambil data dari Detail_cited yang sesuai dengan fk_url_univ
    data = Detail_cited.objects.filter(fk_url_univ=id).order_by("-cited_by")

    # Mengambil objek Universitas berdasarkan id
    universitas = get_object_or_404(Universitas, id=id)

    # Mengambil total sitasi dari objek Universitas
    sitasi_universitas = universitas.total_sitasi

    # Mengambil objek Universitas untuk teknokrat.ac.id
    url_teknokrat = "teknokrat.ac.id"
    teknokrat_queryset = Universitas.objects.filter(url_univ=url_teknokrat)

    # Memastikan bahwa ada objek yang ditemukan
    if teknokrat_queryset.exists():
        # Mengambil objek pertama jika ada lebih dari satu
        teknokrat = teknokrat_queryset.first()
        sitasi_teknokrat = teknokrat.total_sitasi
        selisih_sitasi = sitasi_universitas - sitasi_teknokrat
    else:
        # Handle jika objek teknokrat.ac.id tidak ditemukan
        sitasi_teknokrat = 0
        selisih_sitasi = 0

    # Menyusun data untuk konteks
    context = {
        "dosen": data,
        "url": id,
        "universitas": universitas,
        "sitasi_universitas": sitasi_universitas,
        "selisih_sitasi": selisih_sitasi,
    }

    # Membuat respons dengan template
    template = loader.get_template("sitasi_detail.html")
    return HttpResponse(template.render(context, request))


def insert_univ_backup(request):
    success_message = None

    if request.method == "POST":
        form = add_universitas(request.POST)
        if form.is_valid():
            form.save()
            success_message = "Universitas berhasil ditambahkan!"
            return redirect("/universitas/")
    else:
        form = add_universitas()

    return render(
        request, "add_univ.html", {"form": form, "success_message": success_message}
    )


def insert_univ(request):
    success_message = None

    if request.method == "POST":
        form = add_universitas(request.POST)
        if form.is_valid():
            # Simpan data universitas
            universitas = form.save()

            # Masukkan data Detail_cited untuk setiap universitas
            url_univ = universitas.url_univ
            id_univ = universitas.id
            print(url_univ, id_univ)
            inserd_detail(url_univ, id_univ)
            # insert_detail(universitas.url_univ, universitas.id)

            success_message = "Universitas berhasil ditambahkan!"
            return redirect("/universitas/")
    else:
        form = add_universitas()

    return render(
        request, "add_univ.html", {"form": form, "success_message": success_message}
    )


def scrape_dosen(request, id):
    param_view(id)

    return HttpResponse("berhasil jalan")


def download_csv(request, id):
    # Ambil data dari model
    # queryset = Detail_cited.objects.filter(fk_univ=id)
    queryset = Detail_cited.objects.filter(fk_url_univ=id)
    # queryset = get_object_or_404(Detail_cited, fk_url_univ=id)

    # Tentukan nama file CSV
    response = HttpResponse(content_type="text/csv")

    univ = get_object_or_404(Universitas, id=id)
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{univ.nama_univ}_exported_data_{timezone.now()}.csv"'

    # Buat writer CSV dan tulis header
    csv_writer = csv.writer(response)
    csv_writer.writerow(
        ["Nama Dosen", "Affilliation", "Email", "Cited By", "Url Dosen"]
    )

    # Tulis data ke file CSV
    for obj in queryset:
        csv_writer.writerow(
            [
                getattr(obj, "nama_dosen"),
                getattr(obj, "afiiliation"),
                getattr(obj, "email"),
                getattr(obj, "cited_by"),
                getattr(obj, "urldosen"),
            ]
        )

    return response


def done(request):
    return render(request, "berhasil.html")
