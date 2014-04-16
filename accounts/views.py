from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.core.urlresolvers import reverse
from django.core import serializers

from accounts.forms import AuthenticationForm, RegistrationForm, DubizzleUserProfileChangeForm
from accounts.models import DubizzleUser


def login(request):
    """Dubizzle login view"""

    # GET method should not be allowed here!
    if request.method == 'POST' and request.session.get('user_id', None) is None:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    request.session['user_id'] = user.id
                    request.session['user_short_name'] = user.get_short_name()
                    return redirect(reverse('accounts:profile'))  # Return to profile page.
    elif request.session.get('user_id', None) is None:
        form = AuthenticationForm()
    else:
        return redirect(reverse('accounts:profile'))

    # To return errors on the form.
    return render_to_response('accounts/register.html', {
        'form': form,
        'login_status': 'class=active'  # Playing with the html tabs here.
    }, context_instance=RequestContext(request))


def profile(request):
    user_id = request.session.get('user_id', None)
    if user_id:
        user = DubizzleUser.objects.get(pk=user_id)  # You can certainly cache this.
        if request.method != 'POST':
            form = DubizzleUserProfileChangeForm(instance=user)
        else:
            form = DubizzleUserProfileChangeForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
        return render_to_response('accounts/profile.html', {
            'form': form,
            'user': user,
            'user_short_name': request.session.get('user_short_name'),
        }, context_instance=RequestContext(request))

    else:
        return redirect(reverse('accounts:register'))

    # return render_to_response('accounts/profile.html', {})


def register(request):
    """
    Dubizzle user registration view.
    """
    if request.method == 'POST' and request.session.get('user_id', None) is None:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(email=request.POST['email1'], password=request.POST['password1'])
            django_login(request, user)
            request.session['user_id'] = user.id
            request.session['user_short_name'] = user.get_short_name()
            return redirect('/')  # Redirect to user profile page is a better idea.
    elif request.session.get('user_id', None) is None:
        form = RegistrationForm()
    else:
        return redirect('/')  # This should be the user profile page.
    return render_to_response('accounts/register.html', {
        'form': form,
        'register_status': 'class=active',
        'user_short_name': request.session.get('user_short_name'),
    }, context_instance=RequestContext(request))


def logout(request):
    """
    Logout that redirects to Dubizzle homepage.
    """
    django_logout(request)
    return redirect('/')