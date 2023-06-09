from accounts import config, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from mini_avito_app.models import Client


def register(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            surname = form.cleaned_data.get('surname')
            email = form.cleaned_data.get('email')
            number = form.cleaned_data.get('number')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=surname,
                email=email,
                password=password,
            )
            Client.objects.create(
                user=user,
                phone=number,
                full_name=f'{first_name} {surname}',
            )
            return redirect('login')
        else:
            form = form.errors
    else:
        form = forms.RegistrationForm()

    context = {'form': form}
    return render(request, config.REGISTER_ACCOUNTS, context)


@csrf_exempt
def login_view(request):
    error_msg = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            error_msg = 'Invalid username or password'
    else:
        error_msg = None
    return render(request, config.LOGIN_ACCOUNTS, {'error_msg': error_msg})


def logout_view(request):
    logout(request)
    return redirect('homepage')
