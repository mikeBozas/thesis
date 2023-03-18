from django.db import models
from django.contrib.auth.models import AbstractUser


class Insurer(AbstractUser):
    employee_externalPartner_choices = (
        ('Υπάλληλος', 'Υπάλληλος'),
        ('Εξωτερικός', 'Εξωτερικός')
    )
    first_name               = models.CharField(max_length=64, default="")
    last_name                = models.CharField(max_length=64, default="")
    address                  = models.CharField(max_length=254, default="")
    age                      = models.IntegerField(default=1)
    AFM                      = models.IntegerField(null=True, default=None, unique=True)
    employee_externalPartner = models.CharField(max_length=64, choices=employee_externalPartner_choices, default="")

    def __str__(self):
        return f"Insurer: {self.first_name} - {self.last_name} (id={self.id}) " \
               f"has {self.customer_set.count()} customers and" \
               f"\n has username = {self.username}"

    class Meta:
        verbose_name_plural = "Insurers"


class Customer(models.Model):
    first_name  = models.CharField(max_length=64, default="")
    last_name   = models.CharField(max_length=64, default="")
    AFM         = models.IntegerField(default=0, unique=True)
    AMKA        = models.IntegerField(default=0, unique=True)
    address     = models.CharField(max_length=128, default="")
    dateOfBirth = models.DateField(null=True)
    age         = models.IntegerField(null=True, default=0)
    insurer     = models.ForeignKey(Insurer, on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.first_name} {self.last_name} (id = {self.id}), ΑΜΚΑ = {self.AMKA}, " \
               f"ΑΦΜ = {self.AFM}, Ασφαλιστής = {self.insurer.first_name} {self.insurer.last_name}"


class Insurance(models.Model):
    duration_choices = (
        ("Ετήσια", "Ετήσια"),
        ("Εξάμηνη", "Εξάμηνη"),
        ("Τρίμηνη", "Τρίμηνη")
    )
    payment_method_choices = (
        ("Ετήσια", "Ετήσια"),
        ("Εξάμηνη", "Εξάμηνη"),
        ("Τρίμηνη", "Τρίμηνη")
    )
    insurance_company_choices = (
        ("Εθνική", "Εθνική"),
        ("NN", "NN"),
        ("Groupama", "Groupama")
    )
    kind_of_contract_choices = (
        ("Ζωής", "Ζωής"),
        ("Οχήματος", "Οχήματος"),
        ("Πυρός", "Πυρός"),
        ("Αστικής Ευθύνης", "Αστικής Ευθύνης")
    )
    kind_of_contract   = models.CharField(max_length=128, choices=kind_of_contract_choices, default="")
    active             = models.BooleanField(default=True)
    insurance_company  = models.CharField(max_length=64, choices=insurance_company_choices, default="")
    renew_date         = models.DateField(null=True)
    dateOfPublish      = models.DateField(null=True)
    duration           = models.CharField(max_length=64, choices=duration_choices)
    payment_method     = models.CharField(max_length=64, choices=payment_method_choices)
    insurance_premiums = models.FloatField(null=True, default=0)
    insurance_code     = models.IntegerField(null=True, default=0, unique=True)
    customer           = models.ForeignKey(Customer, on_delete=models.CASCADE)
    insurer            = models.ForeignKey(Insurer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Code: {self.insurance_code}, Date of publish: {self.dateOfPublish}, " \
               f"Customer: {self.customer.first_name}, duration: {self.duration}"
