from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from datetime import date

from .models import Insurer, Customer, Insurance


# first page
def index(request):
    # if we have not logged in a user
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": None})

    # if we log in a user redirect to user's dashboard
    return HttpResponseRedirect('dashboard')


def insurers(request):
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": None})

    if not request.user.is_staff:
        return render(request, "html/index.html", {"message": "You can't access this page"})

    insurers_admin = Insurer.objects.filter(is_staff=False)
    is_admin = True if request.user.is_staff else False

    user = {
        'insurers': insurers_admin,
        'is_admin': is_admin
    }

    return render(request, "html/insurers.html", user)


def insurer_details(request, insurer_id):
    # if we have not logged in a user
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    if not request.user.is_staff:
        return render(request, "html/index.html", {"message": "You can't access this page."})

    is_admin = True if request.user.is_staff else False
    insurer_to_display = Insurer.objects.get(id=insurer_id)
    insurances_to_display = Insurance.objects.filter(insurer=insurer_to_display)
    sum_total = 0
    sum_insurer = 0
    monthOfPublish = False
    has_insurances = True if insurances_to_display else False

    for insurance in Insurance.objects.all():
        sum_total += insurance.insurance_premiums

    for insurance in insurances_to_display:
        sum_insurer += insurance.insurance_premiums

    if sum_total != 0:
        percentage = (sum_insurer / sum_total) * 100
        percentage = round(percentage, 2)
    else:
        percentage = 0

    sum_month = 0
    if request.method == 'POST':
        mydate = request.POST.get('myInputMonth')
        if mydate:
            monthOfPublish = mydate
            my_month, my_year = mydate.split('/')
            insurances_to_display = insurances_to_display.filter(dateOfPublish__year=my_year,
                                                                 dateOfPublish__month=my_month)
            has_insurances = True if insurances_to_display else False
            for insurance in insurances_to_display:
                sum_month += insurance.insurance_premiums

    user = {
        'insurer': insurer_to_display,
        'insurances': insurances_to_display,
        'sum_total': sum_total,
        'sum_insurer': sum_insurer,
        'percentage': percentage,
        'is_admin': is_admin,
        'monthOfPublish': monthOfPublish,
        'has_insurances': has_insurances,
        'sum_month': sum_month
    }

    return render(request, "html/insurer_details.html", user)


# user's dashboard
def dashboard(request):
    # if we have not logged in a user
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    is_admin = True if request.user.is_staff else False

    if is_admin:
        insurers_admin         = Insurer.objects.filter(is_staff=False)
        customers_admin        = Customer.objects.all()
        insurances_admin       = Insurance.objects.all()
        # dependent_member_admin = DependentMember.objects.all()

        insurances_ethnikis = Insurance.objects.filter(insurance_company='Εθνική').all()
        insurances_NN       = Insurance.objects.filter(insurance_company='NN').all()
        insurances_groupama = Insurance.objects.filter(insurance_company='Groupama').all()

        sum_ethnikis_zwis   = 0
        sum_ethnikis_car    = 0
        sum_ethnikis_fire   = 0
        sum_ethnikis_public = 0
        for insurance in insurances_ethnikis:
            if insurance.kind_of_contract == "Ζωής":
                sum_ethnikis_zwis += insurance.insurance_premiums
            elif insurance.kind_of_contract == "Οχήματος":
                sum_ethnikis_car += insurance.insurance_premiums
            elif insurance.kind_of_contract == "Πυρός":
                sum_ethnikis_fire += insurance.insurance_premiums
            else:
                sum_ethnikis_public += insurance.insurance_premiums

        sum_NN_zwis   = 0
        sum_NN_car    = 0
        sum_NN_fire   = 0
        sum_NN_public = 0
        for insurance in insurances_NN:
            if insurance.kind_of_contract == "Ζωής":
                sum_NN_zwis += insurance.insurance_premiums
            elif insurance.kind_of_contract == "Οχήματος":
                sum_NN_car += insurance.insurance_premiums
            elif insurance.kind_of_contract == "Πυρός":
                sum_NN_fire += insurance.insurance_premiums
            else:
                sum_NN_public += insurance.insurance_premiums

        sum_Groupama_zwis = 0
        sum_Groupama_car = 0
        sum_Groupama_fire = 0
        sum_Groupama_public = 0
        for insurance in insurances_groupama:
            if insurance.kind_of_contract == "Ζωής":
                sum_Groupama_zwis += insurance.insurance_premiums
            elif insurance.kind_of_contract == "Οχήματος":
                sum_Groupama_car += insurance.insurance_premiums
            elif insurance.kind_of_contract == "Πυρός":
                sum_Groupama_fire += insurance.insurance_premiums
            else:
                sum_Groupama_public += insurance.insurance_premiums

        sum_sales = 0
        for insurance in insurances_admin:
            sum_sales += insurance.insurance_premiums

        user = {
            'insurers': insurers_admin,
            'customers': customers_admin,
            'insurances': insurances_admin,
            'sum_sales': sum_sales,
            'is_admin': is_admin,
            'insurances_ethnikis': insurances_ethnikis,
            'insurances_NN': insurances_NN,
            'insurances_groupama': insurances_groupama,
            'sum_ethnikis_zwis': sum_ethnikis_zwis,
            'sum_ethnikis_car': sum_ethnikis_car,
            'sum_ethnikis_fire': sum_ethnikis_fire,
            'sum_ethnikis_public': sum_ethnikis_public,
            'sum_NN_zwis': sum_NN_zwis,
            'sum_NN_car': sum_NN_car,
            'sum_NN_fire': sum_NN_fire,
            'sum_NN_public': sum_NN_public,
            'sum_Groupama_zwis': sum_Groupama_zwis,
            'sum_Groupama_car': sum_Groupama_car,
            'sum_Groupama_fire': sum_Groupama_fire,
            'sum_Groupama_public': sum_Groupama_public
        }
        return render(request, 'html/dashboard.html', user)

    sum_sales = 0
    try:
        for insurance in Insurer.objects.get(id=request.user.id).insurance_set.all():
            sum_sales += insurance.insurance_premiums
    except ObjectDoesNotExist:
        sum_sales += 0

    insurances = Insurer.objects.get(id=request.user.id).insurance_set.all()

    for insurance in insurances:
        if insurance.renew_date < date.today():
            insurance.active = False
            insurance.save()

    user = {
        "users": Insurer.objects.get(id=request.user.id),
        'customers': Insurer.objects.get(id=request.user.id).customer_set.all(),
        'insurances': Insurer.objects.get(id=request.user.id).insurance_set.all(),
        'sum_sale': sum_sales,
        'is_admin': is_admin
    }

    # if the user object created correctly go to this user's dashboard
    return render(request, 'html/dashboard.html', user)


# page with the form for adding a new customer
def new_customer(request):
    # if we have not logged in a user
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    if request.user.is_staff:
        return render(request, "html/index.html", {"message": "You cannot login with this account here."
                                                              " Try '/admin' page instead"})

    user = {
        "user": Insurer.objects.get(id=request.user.id),
        'customers': Insurer.objects.get(id=request.user.id).customer_set.all()
    }
    return render(request, "html/new_customer.html", user)


# method/view to handle customers creation
def add_new_customer(request):
    # if we have not logged in a user
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    if request.user.is_staff:
        return render(request, "html/index.html", {"message": "You cannot login with this account here."
                                                              " Try '/admin' page instead"})

    if request.method == 'POST':
        first_name           = request.POST["first_name"]
        last_name            = request.POST["last_name"]
        AFM                  = request.POST["AFM"]
        AMKA                 = request.POST["AMKA"]
        address              = request.POST["address"]
        dateOfBirth          = request.POST["dateOfBirth"]
        age                  = request.POST["age"]
        created_new_customer = Customer.objects.create(first_name=first_name,
                                                       last_name=last_name,
                                                       AFM=AFM,
                                                       AMKA=AMKA,
                                                       address=address,
                                                       dateOfBirth=dateOfBirth,
                                                       age=age,
                                                       insurer=Insurer.objects.get(id=request.user.id)
                                                       )

        created_new_customer.save()

        return HttpResponseRedirect('new_insurance')


# a view to handle the details of a customer
def customer_details(request, customer_id):
    # if we have not logged in a user
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})
    #
    # if request.user.is_staff:
    #     return render(request, "html/index.html", {"message": "You cannot login with this account here."
    #                                                           " Try '/admin' page instead"})

    is_admin = True if request.user.is_staff else False
    # if is_admin:

    try:
        customer = {
            'customer': Customer.objects.get(id=customer_id),
            'insurance_count': "0",
            'insurances': Insurance.objects.filter(customer=Customer.objects.get(id=customer_id)),
            'is_admin': is_admin
        }
    except ObjectDoesNotExist:
        message = {
            'message': "Customer does not exist"
        }
        return render(request, "html/customer_details.html", message)

    if Customer.objects.get(id=customer_id).insurance_set.count() > 0:
        customer = {
            'customer': Customer.objects.get(id=customer_id),
            'insurance_count': Customer.objects.get(id=customer_id).insurance_set.count(),
            'insurances': Insurance.objects.filter(customer=Customer.objects.get(id=customer_id)),
            'is_admin': is_admin
        }

    return render(request, "html/customer_details.html", customer)


# user's statistic page
def customers(request):
    # if we have not logged in a user
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    is_admin = True if request.user.is_staff else False

    if is_admin:
        user = {
            'user': Insurer.objects.get(id=request.user.id),
            'insurers': Insurer.objects.all(),
            'customers': Customer.objects.all(),
            'is_admin': is_admin
        }
        return render(request, 'html/customers.html', user)

    # if request.user.is_staff:
    #     return render(request, "html/index.html", {"message": "You cannot login with this account here."
    #                                                           " Try '/admin' page instead"})

    user = {
        "user": Insurer.objects.get(id=request.user.id),
        'customers': Insurer.objects.get(id=request.user.id).customer_set.all(),
        'is_admin': is_admin
    }
    # same as dashboard view but now we go to to user's statistics page
    return render(request, 'html/customers.html', user)


def new_insurance(request):
    # if we have not logged in a user
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    if request.user.is_staff:
        return render(request, "html/index.html", {"message": "You cannot login with this account here."
                                                              " Try '/admin' page instead"})

    user = {
        "user": Insurer.objects.get(id=request.user.id),
        'customers': Insurer.objects.get(id=request.user.id).customer_set.all()
    }
    # same as dashboard view but now we go to to user's statistics page
    return render(request, 'html/new_insurance.html', user)


def add_new_insurance(request):
    # if we have not logged in a user
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    if request.user.is_staff:
        return render(request, "html/index.html", {"message": "You cannot login with this account here."
                                                              " Try '/admin' page instead"})

    if request.method == 'POST':
        renew_date             = request.POST["renew_date"]
        insurance_company      = request.POST["insurance_company"]
        kind_of_contract       = request.POST["kind_of_contract"]
        dateOfPublish          = request.POST["dateOfPublish"]
        duration               = request.POST["duration"]
        paymentMethod          = request.POST["paymentMethod"]
        insurancePremiums      = request.POST["insurancePremiums"]
        insuranceCode          = request.POST["insuranceCode"]
        customer               = request.POST["customer"]
        *garbage, customer_afm = customer.split()
        del garbage
        customer_afm           = int(customer_afm)
        created_new_insurance  = Insurance.objects.create(renew_date=renew_date,
                                                          insurance_company=insurance_company,
                                                          active=True,
                                                          kind_of_contract=kind_of_contract,
                                                          dateOfPublish=dateOfPublish,
                                                          duration=duration,
                                                          payment_method=paymentMethod,
                                                          insurance_premiums=insurancePremiums,
                                                          insurance_code=insuranceCode,
                                                          customer=Customer.objects.get(AFM=customer_afm),
                                                          insurer=Insurer.objects.get(id=request.user.id)
                                                          )

        created_new_insurance.save()

        return HttpResponseRedirect('insurances_view')


# when the user tries to log in from the index page
def login_view(request):

    # sometimes the MultiValueDictKeyError occur when we try to login
    # this workaround fix this, I don't know why this error appear thought
    try:
        # take the username and pass the user types to the form
        username = request.POST["username"]
        password = request.POST["password"]
    except MultiValueDictKeyError:
        # take the username and pass the user types to the form
        username = request.POST.get("username")
        password = request.POST.get("password")

    # try to authenticate
    user = authenticate(request, username=username, password=password)

    # if the user types correct credentials
    if user is not None:
        # login the user with Django login
        login(request, user)
        # and go to dashboard view
        return HttpResponseRedirect('dashboard')

    # if the user types incorrect credentials
    else:
        # go to index page with a message
        return render(request, "html/index.html", {"message": "Invalid credentials."})


# when a user log out
def logout_view(request):
    # log user out with Django logout
    logout(request)
    # go to index view with message
    return render(request, "html/index.html", {"message": "Έχετε αποσυνδεθεί."})


def insurances_view(request):
    # if we have not logged in a user
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    is_admin = True if request.user.is_staff else False
    if is_admin:
        user = {
            'user': Insurer.objects.get(id=request.user.id),
            'insurers': Insurer.objects.filter(is_staff=False),
            'customers': Customer.objects.all(),
            'insurances': Insurance.objects.all(),
            'is_admin': is_admin
        }
        return render(request, 'html/insurances.html', user)

    user = {
        "user": Insurer.objects.get(id=request.user.id),
        'customers': Insurer.objects.get(id=request.user.id).customer_set.all(),
        'insurances': Insurer.objects.get(id=request.user.id).insurance_set.all(),
        'is_admin': is_admin
    }

    return render(request, 'html/insurances.html', user)


def insurance_details(request, insurance_code):
    # if we have not logged in a user
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    is_admin = True if request.user.is_staff else False

    try:
        insurance = {
            'insurance': Insurance.objects.get(insurance_code=insurance_code),
            'is_admin': is_admin
        }
    except ObjectDoesNotExist:
        message = {
            'message': "Insurance does not exist",
            'is_admin': is_admin
        }
        return render(request, "html/insurance_details.html", message)

    return render(request, "html/insurance_details.html", insurance)


def update_customer(request, customer_id):
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    is_admin = True if request.user.is_staff else False
    if is_admin:
        return render(request, "html/index.html", {"message": 'You can not access this page.'})

    customer = Customer.objects.get(id=customer_id)

    user = {
        'user': Insurer.objects.get(id=request.user.id),
        'customer': customer,
        'is_admin': is_admin
    }

    return render(request, 'html/update_customer.html', user)


def delete_customer(request, customer_id):
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    is_admin = True if request.user.is_staff else False
    if is_admin:
        return render(request, "html/index.html", {"message": 'You can not access this page.'})

    customer = Customer.objects.get(id=customer_id)
    customer.delete()

    return HttpResponseRedirect('/customers')


def delete_insurance(request, insurance_id):
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    is_admin = True if request.user.is_staff else False
    if is_admin:
        return render(request, "html/index.html", {"message": 'You can not access this page.'})

    insurance = Insurance.objects.get(id=insurance_id)
    insurance.delete()

    return HttpResponseRedirect('/insurances_view')


def add_new_updated_customer(request, customer_id):
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    is_admin = True if request.user.is_staff else False

    if request.method == "POST":
        customer             = Customer.objects.get(id=customer_id)
        customer.first_name  = request.POST["first_name"]
        customer.last_name   = request.POST["last_name"]
        customer.AFM         = request.POST["AFM"]
        customer.AMKA        = request.POST["AMKA"]
        customer.address     = request.POST["address"]
        customer.dateOfBirth = request.POST["dateOfBirth"]
        customer.age         = request.POST["age"]

        customer.save()

        return HttpResponseRedirect('/customers')


def update_insurance(request, insurance_id):
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    is_admin = True if request.user.is_staff else False
    if is_admin:
        return render(request, "html/index.html", {"message": 'You can not access this page.'})

    insurance = Insurance.objects.get(id=insurance_id)

    user = {
        'user': Insurer.objects.get(id=request.user.id),
        'insurance': insurance,
        'is_admin': is_admin
    }

    return render(request, 'html/update_insurance.html', user)


def add_new_updated_insurance(request, insurance_id):
    if not request.user.is_authenticated:
        return render(request, "html/index.html", {"message": 'Invalid credentials.'})

    is_admin = True if request.user.is_staff else False
    if is_admin:
        return render(request, "html/index.html", {"message": 'You can not access this page.'})

    if request.method == 'POST':
        insurance = Insurance.objects.get(id=insurance_id)
        insurance.renew_date             = request.POST["renew_date"]
        insurance.insurance_company      = request.POST["insurance_company"]
        insurance.kind_of_contract       = request.POST["kind_of_contract"]
        insurance.dateOfPublish          = request.POST["dateOfPublish"]
        insurance.duration               = request.POST["duration"]
        insurance.paymentMethod          = request.POST["paymentMethod"]
        insurance.insurance_premiums      = request.POST["insurancePremiums"]
        insurance.insuranceCode          = request.POST["insuranceCode"]
        customer               = request.POST["customer"]
        *garbage, customer_afm = customer.split()
        del garbage
        customer_afm           = int(customer_afm)
        insurance.customer = Customer.objects.get(AFM=customer_afm)

        insurance.save()

        return HttpResponseRedirect(f'/insurance_details/{insurance.insurance_code}')


