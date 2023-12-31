from parsel import Selector
import requests, json, re
from bs4 import BeautifulSoup
from django.shortcuts import render, get_object_or_404

# import pandas as pd
import random
from .models import Detail_cited
from .models import Universitas


# Fungsi untuk mendapatkan user agent palsu (fake user agent)
def get_fake_user_agent():
    fake_user_agents = [
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    ]
    return random.choice(fake_user_agents)


def get_proxy():
    proxy = [
        "38.154.227.167:5868:yciaalgj:z8h1v3ja476u",
        "185.199.229.156:7492:yciaalgj:z8h1v3ja476u",
        "185.199.228.220:7300:yciaalgj:z8h1v3ja476u",
        "185.199.231.45:8382:yciaalgj:z8h1v3ja476u",
        "188.74.210.207:6286:yciaalgj:z8h1v3ja476u",
        "188.74.183.10:8279:yciaalgj:z8h1v3ja476u",
        "188.74.210.21:6100:yciaalgj:z8h1v3ja476u",
        "45.155.68.129:8133:yciaalgj:z8h1v3ja476u",
        "154.95.36.199:6893:yciaalgj:z8h1v3ja476u",
        "45.94.47.66:8110:yciaalgj:z8h1v3ja476u",
    ]
    return random.choice(proxy)


def insert_universitas():
    universitas = []
    Universitas.objects.get_or_create(
        nama_univ="input nama univ",
        url_univ="input url univ",
    )
    for x in range(310):
        Detail_cited.objects.get_or_create(
            nama_dosen=nama_dosen,
            afiiliation=affiliations,
            urldosen=link,
            email=email,
            cited_by=cited_by,
            fk_url_univ=universitas_obj,
        )
        print(x)


def scrape_all_authors_backup(url_universitas, fk_univ):
    # data = Universitas.objects.filter(id=fk_univ)

    params = {
        "view_op": "search_authors",  # author results
        "mauthors": url_universitas,  # search query
        "astart": 20,  # page number
    }
    para = 1

    aid_dos = 0
    increment = 1

    headers = {"User-Agent": get_fake_user_agent()}
    data = []
    # ...

    while True:
        html = requests.get(
            "https://scholar.google.com/citations",
            params=params,
            headers=headers,
            timeout=30,
        )
        print(html)
        soup = Selector(text=html.text)
        for author in soup.css(".gs_ai_chpr"):
            aid_dos += 1
            id_dosens = f"{url_universitas}{str(aid_dos)}"

            # Ensure id_dosen is unique
            while Detail_cited.objects.filter(id_dosen=id_dosens).exists():
                id_dosens = f"{url_universitas}{str(aid_dos)}"
            nama_dosen = author.css(".gs_ai_name a").xpath("normalize-space()").get()
            link = f'https://scholar.google.com{author.css(".gs_ai_name a::attr(href)").get()}'
            affiliations = author.css(".gs_ai_aff").xpath("normalize-space()").get()
            email = author.css(".gs_ai_eml").xpath("normalize-space()").get()
            try:
                cited_by = re.search(
                    r"\d+", author.css(".gs_ai_cby::text").get()
                ).group()  # Cited by 17143 -> 17143
            except:
                cited_by = 0
            if para > 2 and para <= 33:
                universitas_obj = Universitas.objects.get(id=fk_univ)
                Detail_cited.objects.get_or_create(
                    id_dosen=id_dosens,
                    nama_dosen=nama_dosen,
                    afiiliation=affiliations,
                    urldosen=link,
                    email=email,
                    cited_by=cited_by,
                    fk_url_univ=universitas_obj,
                )
                print(id_dosens)
            else:
                break
        # print(id_dosens)
        if soup.css(".gsc_pgn button.gs_btnPR::attr(onclick)").get() and para <= 33:
            # extracting next page token and passing to 'after_author' query URL parameter
            params["after_author"] = re.search(
                r"after_author\\x3d(.*)\\x26",
                str(soup.css(".gsc_pgn button.gs_btnPR::attr(onclick)").get()),
            ).group(
                1
            )  # -> XB0HAMS9__8J
            params["astart"] += 10
        else:
            break
        para += 1
        # print(json.dumps(data, indent=2, ensure_ascii=False))
        # df = pd.read_json(json.dumps(data, indent=2, ensure_ascii=False))
        # df.to_csv(hasil + "_Juli.csv", encoding="utf-8", index=False)


def scrape_all_authors(url_universitas, fk_univ):
    # data = Universitas.objects.filter(id=fk_univ)

    params = {
        "view_op": "search_authors",  # author results
        "mauthors": url_universitas,  # search query
        "astart": 20,  # page number
    }
    para = 1

    aid_dos = 0
    increment = 1

    headers = {"User-Agent": get_fake_user_agent()}
    data = []
    # ...

    while True:
        html = requests.get(
            "https://scholar.google.com/citations",
            params=params,
            headers=headers,
            timeout=30,
        )
        print(html)
        soup = Selector(text=html.text)
        for author in soup.css(".gs_ai_chpr"):
            aid_dos += 1
            id_dosens = f"{url_universitas}{str(aid_dos)}"

            # Ensure id_dosen is unique
            while Detail_cited.objects.filter(id_dosen=id_dosens).exists():
                id_dosens = f"{url_universitas}{str(aid_dos)}"
                nama_dosen = (
                    author.css(".gs_ai_name a").xpath("normalize-space()").get()
                )

                link = f'https://scholar.google.com{author.css(".gs_ai_name a::attr(href)").get()}'
                affiliations = author.css(".gs_ai_aff").xpath("normalize-space()").get()
                email = author.css(".gs_ai_eml").xpath("normalize-space()").get()
                try:
                    cited_by = re.search(
                        r"\d+", author.css(".gs_ai_cby::text").get()
                    ).group()
                except:
                    cited_by = 0
                if para > 2 and para <= 33:
                    universitas_obj = Universitas.objects.get(id=fk_univ)

                    # Use update_or_create instead of get_or_create
                    Detail_cited.objects.update_or_create(
                        id_dosen=id_dosens,
                        defaults={
                            "nama_dosen": nama_dosen,
                            "afiiliation": affiliations,
                            "urldosen": link,
                            "email": email,
                            "cited_by": cited_by,
                            "fk_url_univ": universitas_obj,
                        },
                    )
                    print(id_dosens)
                else:
                    break
                aid_dos += 1
                if (
                    soup.css(".gsc_pgn button.gs_btnPR::attr(onclick)").get()
                    and para <= 33
                ):
                    # extracting next page token and passing to 'after_author' query URL parameter
                    params["after_author"] = re.search(
                        r"after_author\\x3d(.*)\\x26",
                        str(soup.css(".gsc_pgn button.gs_btnPR::attr(onclick)").get()),
                    ).group(
                        1
                    )  # -> XB0HAMS9__8J
                    params["astart"] += 10
                else:
                    break
                para += 1
            nama_dosen = author.css(".gs_ai_name a").xpath("normalize-space()").get()
            link = f'https://scholar.google.com{author.css(".gs_ai_name a::attr(href)").get()}'
            affiliations = author.css(".gs_ai_aff").xpath("normalize-space()").get()
            email = author.css(".gs_ai_eml").xpath("normalize-space()").get()
            try:
                cited_by = re.search(
                    r"\d+", author.css(".gs_ai_cby::text").get()
                ).group()  # Cited by 17143 -> 17143
            except:
                cited_by = 0
            if para > 2 and para <= 33:
                universitas_obj = Universitas.objects.get(id=fk_univ)
                Detail_cited.objects.get_or_create(
                    id_dosen=id_dosens,
                    nama_dosen=nama_dosen,
                    afiiliation=affiliations,
                    urldosen=link,
                    email=email,
                    cited_by=cited_by,
                    fk_url_univ=universitas_obj,
                )
                print(id_dosens)
            else:
                break
        # print(id_dosens)
        if soup.css(".gsc_pgn button.gs_btnPR::attr(onclick)").get() and para <= 33:
            # extracting next page token and passing to 'after_author' query URL parameter
            params["after_author"] = re.search(
                r"after_author\\x3d(.*)\\x26",
                str(soup.css(".gsc_pgn button.gs_btnPR::attr(onclick)").get()),
            ).group(
                1
            )  # -> XB0HAMS9__8J
            params["astart"] += 10
        else:
            break
        para += 1
        # print(json.dumps(data, indent=2, ensure_ascii=False))
        # df = pd.read_json(json.dumps(data, indent=2, ensure_ascii=False))
        # df.to_csv(hasil + "_Juli.csv", encoding="utf-8", index=False)


def update_all_authors(url_universitas, fk_univ):
    # data = Universitas.objects.filter(id=fk_univ)

    params = {
        "view_op": "search_authors",  # author results
        "mauthors": url_universitas,  # search query
        "astart": 20,  # page number
    }
    para = 1

    aid_dos = 0
    increment = 1

    headers = {"User-Agent": get_fake_user_agent()}
    data = []
    # ...

    while True:
        html = requests.get(
            "https://scholar.google.com/citations",
            params=params,
            headers=headers,
            timeout=30,
        )
        print(html)
        soup = Selector(text=html.text)
        for author in soup.css(".gs_ai_chpr"):
            aid_dos += 1
            id_dosens = f"{url_universitas}{str(aid_dos)}"

            nama_dosen = author.css(".gs_ai_name a").xpath("normalize-space()").get()
            link = f'https://scholar.google.com{author.css(".gs_ai_name a::attr(href)").get()}'
            affiliations = author.css(".gs_ai_aff").xpath("normalize-space()").get()
            email = author.css(".gs_ai_eml").xpath("normalize-space()").get()
            try:
                cited_by = re.search(
                    r"\d+", author.css(".gs_ai_cby::text").get()
                ).group()
            except:
                cited_by = 0
            if para > 2 and para <= 33:
                universitas_obj = Universitas.objects.get(id=fk_univ)

                # Use update_or_create instead of get_or_create
                Detail_cited.objects.update_or_create(
                    id_dosen=id_dosens,
                    defaults={
                        "nama_dosen": nama_dosen,
                        "afiiliation": affiliations,
                        "urldosen": link,
                        "email": email,
                        "cited_by": cited_by,
                        "fk_url_univ": universitas_obj,
                    },
                )
                print(id_dosens)
            else:
                break

        # print(id_dosens)
        if soup.css(".gsc_pgn button.gs_btnPR::attr(onclick)").get() and para <= 33:
            # extracting next page token and passing to 'after_author' query URL parameter
            params["after_author"] = re.search(
                r"after_author\\x3d(.*)\\x26",
                str(soup.css(".gsc_pgn button.gs_btnPR::attr(onclick)").get()),
            ).group(
                1
            )  # -> XB0HAMS9__8J
            params["astart"] += 10
        else:
            break
        para += 1


def param_view(id):
    # Menggunakan get_object_or_404 untuk memastikan universitas dengan ID tertentu ada
    universitas = get_object_or_404(Universitas, id=id)

    # Mengambil field url_universitas dari objek universitas
    url_universitas = universitas.url_univ
    id_univ = universitas.id
    scrape_all_authors(url_universitas, id_univ)


def param_update(id):
    # Menggunakan get_object_or_404 untuk memastikan universitas dengan ID tertentu ada
    universitas = get_object_or_404(Universitas, id=id)

    # Mengambil field url_universitas dari objek universitas
    url_universitas = universitas.url_univ
    id_univ = universitas.id
    print(url_universitas, id_univ)
    update_all_authors(url_universitas, id_univ)


def inserd_detail(url_univ, id_univ):
    for x in range(310):
        id_dosen = url_univ + str(x)
        Detail_cited.objects.get_or_create(
            id_dosen=id_dosen,
            nama_dosen="Data Belum di Singkronisasikan",
            afiiliation="Data Belum di Singkronisasikan",
            urldosen="Data Belum di Singkronisasikan",
            email="Data Belum di Singkronisasikan",
            cited_by=0,
            fk_url_univ=id_univ,
        )
        print(x, url_univ)


def insert_detail_rev(url_univ, id_univ):
    try:
        univ_instance = Universitas.objects.get(id=52)
    except Universitas.DoesNotExist:
        # Handle kesalahan jika objek tidak ditemukan
        univ_instance = None

    # Periksa apakah objek ditemukan sebelum mencoba mengassign
    if univ_instance:
        for x in range(1, 311):
            id_dosen = f"{url_univ}{x}"
            Detail_cited.objects.get_or_create(
                id_dosen=id_dosen,
                nama_dosen="Data Belum di Singkronisasikan",
                afiiliation="Data Belum di Singkronisasikan",
                urldosen="Data Belum di Singkronisasikan",
                email="Data Belum di Singkronisasikan",
                cited_by=0,
                fk_url_univ=univ_instance,
            )
    else:
        # Handle jika objek Universitas dengan ID 52 tidak ditemukan
        print("Objek Universitas dengan ID 52 tidak ditemukan.")
