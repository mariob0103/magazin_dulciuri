from django.http import HttpResponse, request
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Produs
from django.shortcuts import render
from django.contrib import messages
from collections import Counter
from urllib.parse import urlsplit


zile = [
    "Luni", "Marti", "Miercuri", "Joi", "Vineri", "Sambata", "Duminica"
]
luni = [
    "Ianuarie", "Februarie", "Martie", "Aprilie", "Mai","Iunie", "Iulie","August", "Septembrie", "Octombrie","Noiembrie", "Decembrie"
]

#l1.4
# def get_ip(request):
#     req_headers = request.META
#     str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
#     if str_lista_ip:
#         return str_lista_ip.split(',')[-1].strip()
#     else:
#         return request.META.get('REMOTE_ADDR')

class Accesare:
    ultimul_id = 0
    def __init__(self, ip_client, url, parametri=None):
        Accesare.ultimul_id += 1
        self.id = Accesare.ultimul_id
        self.ip_client = ip_client
        self.url1 = url
        self.parametri = parametri if parametri is not None else {}
        self.data = datetime.now()
    #l1.5
    def lista_parametri(self):
        lista = []
        for cheie, valoare in self.parametri.items():
            if valoare == "":
                valoare = None
            lista.append((cheie,valoare))
        return lista  
    #l1.6
    def url(self):
        return self.url1
    
    def pagina(self):
        return '/' + self.url1.split('/')[-1]
    #l1.7, 1.10
    def calculeaza_data(self, format="%A, %d %B %Y, %H:%M:%S", parametru =''):
        acum = self.data
        if parametru == 'zi':
            format = "%A, %d %B %Y"
        elif parametru == 'timp':
            format = "%H:%M:%S"
        format = format.replace("%A", zile[acum.weekday()])
        format = format.replace("%B", luni[acum.month - 1])
        # return acum.strftime(format)
        return(f"""
            <section>
                <p>Data si ora {acum.strftime(format)}</p>
            </section>
        """
        )
    #l1.9
    def __str__(self):
        return f"Accesare(id={self.id}, ip_client={self.ip_client}, url={self.url()}, pagina = {self.pagina()}, parametri={self.lista_parametri()}, data={self.calculeaza_data()})"    

def index(request): #l1.2
    inregistreaza_accesare(request)
    accesare = Accesare(
        # get_ip(request),
        request.ip_client,
        request.build_absolute_uri(),
        request.GET.dict()
    )

    print(accesare.id)
    return render(request, 'dulciuri/index.html')
    
def afis_produse(request):
    inregistreaza_accesare(request)
    nrPagina=request.GET.get("pagina", 1)
    # veti trata situatia in care nu e dat un numar intreg
    produse=Produs.objects.all()
    paginator = Paginator(produse, 5) # 5 produse pe pagina
    mesajEroare=None
    try:
        obPagina = paginator.page(nrPagina)
    except EmptyPage:
        obPagina=None
        mesajEroare = "Nu mai sunt produse"
    return render(request, 'dulciuri/produse.html',
        {
            'pagina': obPagina,
            'eroare': mesajEroare
        }
    )


def info(request): #L1.2, 1.3, 1.4
    inregistreaza_accesare(request)
    accesare = Accesare(
            # get_ip(request),
            request.ip_client,
            request.build_absolute_uri(),
            request.GET.dict()
        )
    print(accesare.id) #l1.4
    print(accesare.pagina())#l1.5
    print(request.ip_client)#l1.8
    print(accesare)#l1.9
    # acum = datetime.now()
    # zi_saptamana = zile[acum.weekday()]
    # luna = luni[acum.month - 1]
    # data_formatata = (
    #     f"{zi_saptamana}, {acum.day} {luna} {acum.year}"
    # )
    # ora_formatata = acum.strftime("%H:%M:%S")
    #L1.7
    data_formatata = accesare.calculeaza_data()
    data_formatata1 = request.GET.get("data", "")
    data_final = accesare.calculeaza_data(parametru = data_formatata1)
    #L1.2,1.3
    html = f""" 
    <!DOCTYPE html>
    <html lang="ro">
    <head>
        <meta charset="UTF-8">
        <title>Informatii despre server</title>
    </head>
    <body>
        <h1>Informatii despre server</h1>

        <h2>Data si ora</h2>
        {data_final}
    </body>
    </html>
    """
    return HttpResponse(html)

def afisare(request):
    messages.debug(request, "DEBUG: Verificăm funcționarea paginii.")
    messages.info(request, "Bine ai venit în magazinul de dulciuri!")
    messages.success(request, "Pagina a fost încărcată cu succes!")
    messages.warning(request, "Atenție! Unele produse pot fi indisponibile.")
    messages.error(request, "Exemplu de mesaj de eroare.")

    return render(request, 'dulciuri/mesaje.html')

#L2.1.1 folosita apoi in fiecare pagina
accesari = []
urmatorul_id = 1


def inregistreaza_accesare(request):
    global urmatorul_id

    accesari.append({
        "id": urmatorul_id,
        "url": request.get_full_path(),
        "data": datetime.now()
    })

    urmatorul_id += 1


def log(request):
    inregistreaza_accesare(request)

    lista = accesari
    mesaj = ""

    ultimele = request.GET.get("ultimele") #returnează o singură valoare

    if ultimele is not None:
        try:
            n = int(ultimele)

            if n < 0:
                return HttpResponse(
                    "Eroare: ultimele trebuie sa fie un numar natural."
                )

            lista = accesari[-n:] if n > 0 else []

            if n > len(accesari):
                mesaj = (
                    f"Exista doar {len(accesari)} accesari "
                    f"fata de {n} accesari cerute"
                )

        except ValueError:
            return HttpResponse(
                "Eroare: parametrul ultimele trebuie sa fie un numar intreg."
            )

    html = "<h1>Istoric accesari</h1><ul>"

    for accesare in lista:
        html += (
            f"<li>ID: {accesare['id']} - "
            f"URL: {accesare['url']} - "
            f"Data: {accesare['data']}</li>"
        )

    html += "</ul>"

    if mesaj:
        html += f"<p>{mesaj}</p>"

    return HttpResponse(html)

#L2.1.1, L2.1.2
def log(request):
    inregistreaza_accesare(request)

    lista = accesari
    mesaj = ""

    #L2.1.1
    ultimele = request.GET.get("ultimele")

    if ultimele is not None:
        try:
            n = int(ultimele)

            if n < 0:
                return HttpResponse(
                    "Eroare: ultimele trebuie sa fie un numar natural."
                )

            lista = accesari[-n:] if n > 0 else []

            if n > len(accesari):
                mesaj = (
                    f"Exista doar {len(accesari)} accesari "
                    f"fata de {n} accesari cerute"
                )

        except ValueError:
            return HttpResponse(
                "Eroare: parametrul ultimele trebuie sa fie un numar intreg."
            )

    #L2.1.2
    iduri = request.GET.getlist("iduri")

    if iduri:
        lista = []
        dubluri = request.GET.get("dubluri", "false").lower() == "true"
        iduri_vazute = set()

        for grup in iduri:
            for valoare in grup.split(","):
                try:
                    id_cautat = int(valoare.strip())
                except ValueError:
                    return HttpResponse(
                        "Eroare: ID-urile trebuie sa fie numere intregi."
                    )

                if not dubluri and id_cautat in iduri_vazute:
                    continue

                iduri_vazute.add(id_cautat)

                for accesare in accesari:
                    if accesare["id"] == id_cautat:
                        lista.append(accesare)
                        break

    #L2.1.2
    afiseaza_numar = request.GET.get("accesari") == "nr"

    # afisarea paginii
    html = "<h1>Istoric accesari</h1><ul>"

    for accesare in lista:
        html += (
            f"<li>ID: {accesare['id']} - "
            f"URL: {accesare['url']} - "
            f"Data: {accesare['data']}</li>"
        )

    html += "</ul>"

    if mesaj:
        html += f"<p>{mesaj}</p>"

    if afiseaza_numar:
        html += (
            f"<h2>Numar accesari</h2>"
            f"<p>{len(accesari)}</p>"
        )
        
    # L2.1.3 afiseaza o lista neordonata cu data si ora fiecarei accesari
    if request.GET.get("accesari") == "detalii":
        html += "<h2>Data si ora accesarilor</h2><ul>"

        for accesare in accesari:
            html += f"<li>{accesare['data']}</li>"

        html += "</ul>"
        
    # Sectiunea parametri afiseaza numele si numarul parametrilor primiti prin URL
    html += "<h2>Parametri</h2>"
    parametri = request.GET
    html += f"<p>Numar parametri: {len(parametri)}</p>"
    html += "<ul>"
    for nume in parametri:
        html += f"<li>{nume}</li>"
    html += "</ul>"
    
    
    #L2.1.4 afisare tabel
    tabel = request.GET.get("tabel")

    if tabel is not None:
        if tabel == "tot":
            coloane = ["id", "url", "data"]
        else:
            coloane = tabel.split(",")

        coloane_valide = ["id", "url", "data"]

        for coloana in coloane:
            if coloana not in coloane_valide:
                return HttpResponse(
                    f"Eroare: coloana {coloana} nu exista."
                )

        html += "<h2>Tabel accesari</h2>"
        html += "<table border='1'>"

        # Antetul tabelului
        html += "<tr>"
        for coloana in coloane:
            html += f"<th>{coloana}</th>"
        html += "</tr>"

        # Randurile tabelului
        for accesare in lista:
            html += "<tr>"
            for coloana in coloane:
                html += f"<td>{accesare[coloana]}</td>"
            html += "</tr>"

        html += "</table>"



# L2.1.5 pagini cele mai / cel mai putin accesate

    numarari = Counter()

    for accesare in accesari:
        pagina = urlsplit(accesare["url"]).path
        numarari[pagina] += 1

    if numarari:
        maxim = max(numarari.values())
        minim = min(numarari.values())

        pagini_maxim = [
            pagina for pagina, nr in numarari.items()
            if nr == maxim
        ]

        pagini_minim = [
            pagina for pagina, nr in numarari.items()
            if nr == minim
        ]

        html += "<h2>Statistici pagini</h2>"
        html += (
            f"<p>Cele mai accesate pagini: "
            f"{', '.join(pagini_maxim)} ({maxim} accesari)</p>"
        )
        html += (
            f"<p>Cele mai putin accesate pagini: "
            f"{', '.join(pagini_minim)} ({minim} accesari)</p>"
        )

    return HttpResponse(html)

def detalii_accesare(request, id):
    inregistreaza_accesare(request)
    id = int(id)
    for accesare in accesari:
        if accesare["id"] == id:
            html = "<h1>Detalii accesare</h1>"
            html += f"<p>ID: {accesare['id']}</p>"
            html += f"<p>URL: {accesare['url']}</p>"
            html += f"<p>Data: {accesare['data']}</p>"
            return HttpResponse(html)

    return HttpResponse(
        "Eroare: accesarea nu exista.",
        status=404
    )

def istoric(request):
    inregistreaza_accesare(request)
    return HttpResponse("<h1>Pagina Istoric</h1>")


def despre(request):
    inregistreaza_accesare(request)
    return HttpResponse(
        "<h1>Despre noi</h1>"
        "<p>Suntem un magazin online de dulciuri.</p>"
    )

def in_lucru(request):
    inregistreaza_accesare(request)
    return render(request, 'dulciuri/in_lucru.html')