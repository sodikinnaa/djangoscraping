from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpRequest
from .models import Universitas
from .models import Detail_cited
from .helper import param_view, inserd_detail, param_update

# pdf require
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


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


# def insert_univ_backup(request):
#     success_message = None

#     if request.method == "POST":
#         form = add_universitas(request.POST)
#         if form.is_valid():
#             form.save()
#             success_message = "Universitas berhasil ditambahkan!"
#             return redirect("/universitas/")
#     else:
#         form = add_universitas()

#     return render(
#         request, "berhasil.html", {"form": form, "success_message": success_message}
#     )


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

            success_message = "Universitas berhasil ditambahkan!"
            return redirect(f"/universitas")
    else:
        form = add_universitas()

    return render(
        request, "add_univ.html", {"form": form, "success_message": success_message}
    )


def done_add(request, id_univ):
    return HttpResponse("sukses")


def update_dosen(request, id):
    param_update(id)
    return redirect(f"/universitas/{id}")


def scrape_dosen(request, id):
    param_view(id)

    return redirect(f"/universitas/{id}")


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


def download_pdf(request, id):
    # Ambil data dari model
    queryset = Detail_cited.objects.filter(fk_url_univ=id)

    # Tentukan nama file PDF
    univ = get_object_or_404(Universitas, id=id)
    filename = f"{univ.nama_univ}_exported_data_{timezone.now()}.pdf"

    # Buat objek PDF menggunakan ReportLab
    pdf_buffer = BytesIO()

    # Tentukan ukuran halaman dan margin
    width, height = letter
    left_margin = 30
    right_margin = 30

    # Buat objek canvas PDF
    pdf = SimpleDocTemplate(
        pdf_buffer,
        pagesize=(width, height),
        leftMargin=left_margin,
        rightMargin=right_margin,
    )

    # Tambahkan konten ke PDF
    data = [["No", "Nama Dosen", "Affiliation", "Email", "Cited By", "URL Dosen"]]

    styles = getSampleStyleSheet()
    style_table = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    for no, obj in enumerate(queryset, start=1):
        data.append(
            [
                str(no),
                Paragraph(getattr(obj, "nama_dosen"), styles["Normal"]),
                Paragraph(getattr(obj, "afiiliation"), styles["Normal"]),
                Paragraph(getattr(obj, "email"), styles["Normal"]),
                Paragraph(str(getattr(obj, "cited_by")), styles["Normal"]),
                Paragraph(
                    f'<a href="{getattr(obj, "urldosen")}">{getattr(obj, "urldosen")}</a>',
                    styles["Normal"],
                ),
            ]
        )

    table = Table(data, colWidths=[30, 120, 150, 150, 50, 150], style=style_table)

    # Build PDF
    elements = [table]
    pdf.build(elements)

    # Ambil PDF dari buffer dan kirim sebagai respons
    pdf_buffer.seek(0)
    response = HttpResponse(pdf_buffer.read(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    pdf_buffer.close()

    return response
