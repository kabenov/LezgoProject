from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView

from myLezgo.forms import OrderForm, CreateUserForm
from myLezgo.models import Car, Order


def index(request):
    return render(request, 'myLezgo/index.html')


def support(request):
    return render(request, 'myLezgo/support.html')


def feedback(request):
    return render(request, 'myLezgo/feedback.html')


def order(request):
    if request.method == "POST":
        name = request.POST['name']
        surname = request.POST['surname']
        number = request.POST['phone_number']
        city = request.POST['city']
        car = Car.objects.filter(id=int(request.POST['cars'])).first()
        water = False
        if request.POST['water'] == 'on':
            water = True
        driver = False
        if request.POST['driver'] == 'on':
            driver = True
        trip = False
        if request.POST['trip'] == 'on':
            trip = True
        sweets = False
        if request.POST['sweets'] == 'on':
            sweets = True
        comment = request.POST['comment']
        Order.objects.create(name=name,
                             surname=surname,
                             number=number,
                             city=city,
                             car=car,
                             water=water,
                             driver=driver,
                             outOfTown=trip,
                             sweets=sweets,
                             comments=comment)

        return redirect('/')
    else:
        return render(request, 'myLezgo/order.html', {'car_list': Car.objects.all()})


class CarDetailView(DetailView):
    model = Car
    slug_field = 'slug'
    slug_url_kwarg = 'car_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(Car.objects.get(slug=self.kwargs['car_slug']).name)
        return context


def sign_up(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)

            return redirect('sign_in')

    context = {'form': form}
    return render(request, 'myLezgo/registration.html', context)


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect!')

    context = {}
    return render(request, 'myLezgo/sign_in.html', context)


def sign_out(request):
    logout(request)
    return redirect('home')
