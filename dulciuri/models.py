from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime

# Create your models here.
#Laborator 3 task 1 modelele corespunzatoare entitatilor din diagrama
class Produs(models.Model):
    class Meta:
        verbose_name_plural = "Produse"

    id_produs = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=200, db_index=True, help_text="Introduceti numele produsului.", 
                            error_messages={'required': 'Numele produsului este obligatoriu.', 
                                            'max_length': 'Numele produsului nu poate depasi 200 de caractere.'})
    imagine = models.ImageField(upload_to='produse/', null=True, blank=True)
    descriere = models.CharField(max_length=300)
    aroma = models.CharField(max_length=50)
    continut = ArrayField(models.CharField(max_length=100), default=list)
    pret = models.DecimalField(max_digits=10, decimal_places=2,db_index=True)
    data_adaugare = models.DateTimeField(default=datetime.now)
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT, related_name='produse')
    categorie = models.ForeignKey('Categorie', on_delete=models.PROTECT, related_name='produse')
    

    def __str__(self):
        return self.nume
#entitatea brand 
class Brand(models.Model):
    class Meta:
        ordering = ['nume']
        verbose_name_plural = "Branduri"

    id_brand = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=100, unique=True, help_text="Introduceti numele brandului.", 
                            error_messages={'required': 'Numele brandului este obligatoriu', 
                                            'unique': 'Exista deja un brand cu acest nume'})
    descriere = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nume
#entitatea categorie    
class Categorie(models.Model):
    class Meta:
        ordering = ['nume']
        verbose_name_plural = "Categorii"

    CATEGORII = [
        ('ciocolata', 'Ciocolata'),
        ('biscuiti', 'Biscuiti'),
        ('bomboane', 'Bomboane'),
        ('jeleuri', 'Jeleuri'),
        ('prajituri', 'Prajituri'),
    ]

    id_categorie = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=100, unique=True,choices = CATEGORII, help_text="Introduceti numele categoriei.", 
                            error_messages={'unique': 'Aceasta categorie exista deja in magazin.', 
                                            'max_length': 'Numele categoriei nu poate depasi 100 de caractere.'})
    descriere = models.TextField(null=True, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nume    
#ENTITATE SLABA STOC PRODUS 
class Stoc_Produs(models.Model):
    class Meta:
        verbose_name_plural = "Stocuri produse"
        constraints = [
            models.UniqueConstraint(fields=['produs', 'id_lot'], name='lot_unic_per_produs'),
            models.CheckConstraint(condition=models.Q(cantitate__gte=0), name='cantitate_stoc_pozitiva'),
            models.CheckConstraint(condition=models.Q(cost__gte=0), name='cost_stoc_pozitiv')
        ]

    id_lot = models.IntegerField()
    cantitate = models.IntegerField(default=0, help_text="Introduceti cantitatea disponibila.")
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    data_intrare = models.DateTimeField() #data introdus manual deoarec poate fi diferita fata de cea in care au sosit produsele
    produs = models.ForeignKey('Produs', on_delete=models.CASCADE, related_name='loturi')

    def __str__(self):
        return f"Lot {self.id_lot} - {self.produs.nume}"
    
class Eveniment(models.Model):
    class Meta:
        verbose_name_plural = "Evenimente"
        constraints = [
    models.CheckConstraint(condition=models.Q(data_final__gte=models.F('data_incepere')), name='eveniment_date_valide')
]

    id_eveniment = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=100)
    descriere = models.CharField(max_length=200, null=True, blank=True)
    data_incepere = models.DateTimeField(db_index=True, error_messages={'invalid': 'Introduceti o data si o ora valide pentru inceperea evenimentului.', 
                                                                        'required': 'Data inceperii evenimentului este obligatorie.'})
    data_final = models.DateTimeField()
    produse = models.ManyToManyField('Produs', related_name='evenimente', blank=True)

    def __str__(self):
        return self.nume
    
class Oferta(models.Model):
    class Meta:
        verbose_name_plural = "Oferte"
        constraints = [models.CheckConstraint(condition=models.Q(discount__gte=0) & models.Q(discount__lte=100), name='discount_valid'),
        models.CheckConstraint(condition=models.Q(data_final__gte=models.F('data_inceput')), name='oferta_date_valide')
    ]

    id_oferta = models.AutoField(primary_key=True)
    tip = models.CharField(max_length=100)
    descriere = models.CharField(max_length=200)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, 
                                help_text="Introduceti procentul de reducere", 
                                error_messages={'invalid': 'Reducerea trebuie sa fie un numar valid.',
                                                'max_decimal_places': 'Reducerea poate avea maximum doua zecimale.'})
    data_inceput = models.DateTimeField()
    data_final = models.DateTimeField(db_index=True) # data final indexata pentru a gasi ofertele care expira
    produse = models.ManyToManyField('Produs', related_name='oferte', blank=True)

    def __str__(self):
        return self.tip    



