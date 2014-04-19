from django.shortcuts import redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.edit import FormView

from accounts.forms import AuthenticationForm, RegistrationForm, DubizzleUserProfileChangeForm
from accounts.models import DubizzleUser


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('accounts:profile')

    def post(self, request, *args, **kwargs):
        if request.session.get('user_id', None) is None:
            return super(LoginView, self).post(request, args, kwargs)
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        if request.session.get('user_id', None) is None:
            return super(LoginView, self).get(request, args, kwargs)
        else:
            return redirect(self.success_url)

    def form_valid(self, form):
        request = self.request
        user = authenticate(email=request.POST['email'], password=request.POST['password'])
        if user is not None and user.is_active:
            django_login(request, user)
            request.session['user_id'] = user.id
            request.session['user_short_name'] = user.get_short_name()
            return super(LoginView, self).form_valid(form)
        else:
            return super(LoginView, self).form_invalid(form)  # To tell that user with these credentials is not
            # registered with Dubizzle.

    def form_invalid(self, form):
        """
        Override this method later to perform custom validation checks on user credentials.
        """
        return super(LoginView, self).form_invalid(form)


class ProfileMainView(FormView):
    """
    This is only the main tab implementation of the profile page. The rest of the tabs would be in separate views.
    Correct if this methodology is wrong.
    """
    template_name = 'accounts/profile.html'
    form_class = DubizzleUserProfileChangeForm
    success_url = reverse_lazy('accounts:profile')

    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        user = DubizzleUser.objects.get(pk=user_id)
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        user_short_name = request.session.get('user_short_name')
        user = DubizzleUser.objects.get(pk=user_id)
        form = self.form_class(instance=user)
        return self.render_to_response(self.get_context_data(form=form, user=user, user_short_name=user_short_name))

    def form_valid(self, form):
        form.save()
        return super(ProfileMainView, self).form_valid(form)


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('accounts:profile')

    def post(self, request, *args, **kwargs):
        if request.session.get('user_id', None) is None:
            return super(RegisterView, self).post(request, args, kwargs)
        else:
            return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        if request.session.get('user_id', None) is None:
            return super(RegisterView, self).get(request, args, kwargs)
        else:
            return redirect(self.success_url)

    def form_valid(self, form):
        form.save()
        request = self.request
        user = authenticate(email=request.POST['email1'], password=request.POST['password1'])
        django_login(request, user)
        request.session['user_id'] = user.id
        request.session['user_short_name'] = user.get_short_name()
        return super(RegisterView, self).form_valid(form)


def logout(request):
    """
    Logout that redirects to Dubizzle homepage.
    """
    django_logout(request)
    return redirect('/')