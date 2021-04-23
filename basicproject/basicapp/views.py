from django.shortcuts import render
from basicapp.forms import FormPerson, UserForm
from fuzzywuzzy import fuzz

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request,'basicapp/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
    else:
        user_form = UserForm()

    return render(request,'basicapp/registration.html',
                   {'user_form':user_form,
                   'registered':registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('form_name'))

            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
            #return render(request,'basicapp/form.html',{})
        else:
            print('Someone tried to login and failed!')
            print('Username: {} and password {}'.format(username,password))
            return HttpResponse('Invalid login details supplied!')
    else:
        return render(request,'basicapp/login.html',{})


def form_name_view(request):
    form = FormPerson()

    if request.method == 'POST':
        form = FormPerson(request.POST)

        if form.is_valid():
            #DO SOMETHING CODE
            probability = 0
            print("VALIDATION SUCCESS!")
            print("NAME: "+form.cleaned_data['Person1_name'])
            print("BIRTHDAY: "+str(form.cleaned_data['Person1_birthday']))
            print("BSN: "+form.cleaned_data['Person1_bsn'])
            print("NAME: "+form.cleaned_data['Person2_name'])
            print("BIRTHDAY: "+str(form.cleaned_data['Person2_birthday']))
            print("BSN: "+form.cleaned_data['Person2_bsn'])

            person1_firstname, person1_lastname = form.cleaned_data['Person1_name'].split()
            person1_birthday = form.cleaned_data['Person1_birthday']
            person1_bsn = form.cleaned_data['Person1_bsn']

            person2_firstname, person2_lastname = form.cleaned_data['Person2_name'].split()
            person2_birthday = form.cleaned_data['Person2_birthday']
            person2_bsn = form.cleaned_data['Person2_bsn']

            if (person1_bsn == person2_bsn) and (person1_bsn != '') and (person2_bsn != '') and (person1_bsn != 'unknown') and (person2_bsn != 'unknown'):
                probability = 100
                return render(request,'basicapp/result.html',{'probability':probability})
            else:
                if (person1_birthday == person2_birthday) and (person1_birthday is not None) and (person2_birthday is not None):
                    probability = probability + 40
                    print("Probability :"+str(probability))
                if ((person1_firstname+person1_lastname) == (person2_firstname+person2_lastname)):
                    probability = probability + 60
                    print("Probability :"+str(probability))
                else:
                    if (person1_firstname == person2_firstname):
                        probability = probability + 20
                    elif (person1_lastname == person2_lastname):
                        if (person1_firstname == (person2_firstname[0]+'.')) or (person2_firstname == (person1_firstname[0]+'.')):
                            probability = probability + 55
                        else:
                            probability = probability + 40
                    elif (fuzz.partial_ratio(person1_firstname,person2_firstname) > 60):
                        probability = probability + 15
                    elif (person1_firstname == (person2_firstname[0]+'.')) or (person2_firstname == (person1_firstname[0]+'.')):
                        if (person1_lastname == person2_lastname):
                            probability = probability + 55
                        else:
                            probability = probability + 15
                    else:
                        probability = probability + 0
                        return render(request,'basicapp/result.html',{'probability':probability})
                

                print("Probability :"+str(probability))
                return render(request,'basicapp/result.html',{'probability':probability})
            
                

    return render(request,'basicapp/form.html',{'form':form})
