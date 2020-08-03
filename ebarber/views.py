from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import Area, Barbershop, Customer, UserManager

def index(request):
    area = Area.objects.all()
    context = {'obj': area }
    if 'username' in request.session:
        username = request.session['username']
        surname = request.session['surname']
        name = request.session['name']
        phone = request.session['phone']

    return render(request, 'ebarber/index.html', context)

def search(request):
    area = Area.objects.all()
    aid = request.GET.get('area')
    if aid:
        aname = Area.objects.get(pk=aid)
        availables = Barbershop.um.all().filter(area=aid)
        if (len(availables) == 0):
            area = Area.objects.all()
            message = "There are no barbershops in this area yet "
            context = {'obj': area, 'message': message}
            return render(request, 'ebarber/index.html', context)
        else:
            num = len(availables)
            context = {'aid': aid, 'aname': aname, 'availables': availables, 'num': num } #Inside the brackets {{ ... }} we put the name in '...'
            return render(request, 'ebarber/AvailableBarbershops.html', context)
    else:
        context = { 'obj': area, 'message': 'Please select an area '}
        return render(request, 'ebarber/index.html', context)

def bprof(request):
    print(request.POST.get('username'))
    if request.POST.get('username'):
        username = request.session['username']
        address = request.session['address']
        email = request.session['email']
        phone = request.session['phone']
        area = request.session['area']
        return render(request, 'ebarber/BarbershopPage.html')

    if not request.POST.get('username'):
        area = Area.objects.all()
        context = {
            'message': 'Log in first! ',
            'obj': area
        }
        return render(request, 'ebarber/index.html', context)


def register(request):
    area = Area.objects.all()
    errors = UserManager().validator(request.POST)
    if len(errors):
        errors = "<ol>" + errors + "</ol>"
        if( request.POST['kind']=='customer' ):
            args = {'rcError': errors, 'obj': area}

        if( request.POST['kind']=='barbershop' ):
            args = {'rbError': errors, 'obj': area}
    else:
        us = request.POST['username']
        em = request.POST['email']

        if( request.POST['kind']=='customer' ):
            if( Customer.um.filter(username = us).exists() and Customer.um.filter(email = em).exists() ):
                args = {
                    'message': 'Username and email already exist!',
                    'obj': area
                }
                return render(request, 'ebarber/index.html', args, status=400)

            if( Customer.um.filter(username = us).exists() ):
                args = {
                    'message': 'Username already exists! Try another. ',
                    'obj': area
                }
                return render(request, 'ebarber/index.html', args, status=400)

            if( Customer.um.filter(email = em).exists() ):
                args = {
                    'message': 'Email already exists! Try another. ',
                    'obj': area
                }
                return render(request, 'ebarber/index.html', args, status=400)

            user = Customer.um.create(username=request.POST['username'], password=request.POST['password'],
                                    email=request.POST['email'], phone=request.POST['phone'],
                                    name=request.POST['name'], surname=request.POST['surname'])

        if( request.POST['kind']=='barbershop' ):
            if( Barbershop.um.filter(username = us).exists() and Barbershop.um.filter(email = em).exists() ):
                args = {
                    'message': 'Username and email already exist!',
                    'obj': area
                }
                return render(request, 'ebarber/index.html', args, status=400)

            if( Barbershop.um.filter(username = us).exists() ):
                args = {
                    'message': 'Username already exists! Try another. ',
                    'obj': area
                }
                return render(request, 'ebarber/index.html', args, status=400)

            if( Barbershop.um.filter(email = em).exists() ):
                args = {
                    'message': 'Email already exists! Try another. ',
                    'obj': area
                }
                return render(request, 'ebarber/index.html', args, status=400)

            user = Barbershop.um.create(username=request.POST['username'], password=request.POST['password'],
                                        email=request.POST['email'], phone=request.POST['phone'],
                                        address=request.POST['address'], area_id=request.POST['area'])

        user.save()
        success = 'Your registration was successfull!'
        args = {'success': success, 'obj': area}

    return render(request, 'ebarber/index.html', args)

def login(request):
    area = Area.objects.all()
    if not request.POST.get('username'):
        context = {
            'message': 'Username and password are needed to log in.',
            'obj':area
        }
        return render(request, 'ebarber/index.html', context)
    if not request.POST.get('password'):
        context = {
            'message': 'Username and password are needed to log in.',
            'obj':area
        }
        return render(request, 'ebarber/index.html', context)

    if( request.POST.get('ifbarber') == None ):
        if(Customer.um.filter(username=request.POST['username']).exists() and Customer.um.filter(password=request.POST['password']).exists()):
            user = Customer.um.filter(username=request.POST['username'])[0]
            request.session['id'] = user.id
            request.session['username'] = user.username
            request.session['name'] = user.name
            request.session['surname'] = user.surname
            request.session['phone'] = user.phone
            request.session['email'] = user.email
            user_ses = Customer.um.get(id=request.session['id'])
            context = {
                "user": user_ses,
                'success': 'You have logged in successfully!',
                'obj':area
            }
            return render(request, 'ebarber/index.html', context)
        else:
            message = "Wrong username or password. You may need to switch the box 'I am a barber"
            context = { 'obj':area, 'message': message }
            return render(request, 'ebarber/index.html', context)
    else:
        if(Barbershop.um.filter(username=request.POST['username']).exists() and Barbershop.um.filter(password=request.POST['password']).exists()):
            user = Barbershop.um.filter(username=request.POST['username'])[0]
            request.session['id'] = user.id
            request.session['username'] = user.username
            request.session['email'] = user.email
            request.session['phone'] = user.phone
            request.session['address'] = user.address
            request.session['area'] = user.area_id
            user_ses = Barbershop.um.get(id=request.session['id'])
            context = {
                "user": user_ses,
                'success': 'You have logged in successfully!'
            }
            return render(request, 'ebarber/BarbershopPage.html', context)
        else:
            message = "Wrong username or password. You may need to switch the box 'I am a barber"
            context = { 'obj':area, 'message': message }
            return render(request, 'ebarber/index.html', context)

def logout(request):
    area = Area.objects.all()
    gbname = request.session.get('username')
    request.session.flush()
    context = {'success': 'Hope we see you again', 'obj': area, 'gbname': gbname}
    return render(request, 'ebarber/index.html', context)
