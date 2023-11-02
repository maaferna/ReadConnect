from django.shortcuts import render, redirect

# Create your views here.
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

#Add permission to the views
from django.contrib.auth.decorators import login_required, permission_required
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.helpers import render_authentication_error
from django.http import HttpResponseRedirect
from allauth.socialaccount.models import SocialLogin
from django.views.decorators.csrf import csrf_exempt

def view_login(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username,
      password=password)
      if user is not None:
        login(request, user)
        messages.info(request, f"Iniciaste sesión como: {username}.")
        return HttpResponseRedirect('/')
      else:
        messages.error(request,"Invalido username o password.")
    else:
      messages.error(request,"Invalido username o password.")
  form = AuthenticationForm()
  return render(request=request, template_name="registration/login.html",context={"login_form":form})


def view_register(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the authentication backend
            login(request, user)
            messages.success(request, "Registrado Satisfactoriamente.")
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Registro inválido. Algunos datos ingresados no son correctos.")
    else:
        form = RegistroUsuarioForm()
    return render(request, template_name="registration/registro.html", context={"register_form": form})

@login_required
def view_logout(request):
  logout(request)
  messages.info(request, "Se ha cerrado la sesión satisfactoriamente.")
  return redirect('home')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'registration/success.html')
    form = ContactForm
    context = {'form': form}
    return render(request, 'registration/contact.html', context)


@login_required
def profile_view(request):
    # You can access the user's profile or any other information here
    user = request.user  # This is the logged-in user
    context = {
        'user': user,
        # Add any other context data you want to display on the profile page
    }
    return render(request, 'registration/edit_profile.html', context)

class CustomGoogleOAuth2LoginView(OAuth2LoginView):
    def login(self):
        if self.request.method == 'POST':
            try:
                app = self.adapter.get_app(self.request)
                client = app.get_social_app(self.adapter.provider_id)
                provider = app.get_provider(self.adapter.provider_id)

                response = self.adapter.complete_login(self.request, app, client)

                if not response:
                    return render_authentication_error(self.request)

                login = self.adapter.login_by_token(self.request, app, response)
                if login:
                    # Customize login logic here if needed
                    # Example: Set a flag to indicate this login is via Google
                    login.state['via_google'] = True
                    login.save(request=self.request)
                    return self.login_by_auth_token(
                        app, login.token, state=response.get('state')
                    )

            except OAuth2Error:
                return render_authentication_error(self.request)
        return self.oauth2_login()

@csrf_exempt
def login_vue(request):
    if request.method == 'POST':
        # Handle the login logic here
        # ...
        return JsonResponse({'message': 'Login successful'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


