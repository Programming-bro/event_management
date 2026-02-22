from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import  Group
from django.contrib.auth import login, logout, get_user_model
from users.forms import CustomRegistrationForm, AssignRoleForm, CreateGroupForm, EditProfileForm, CustomPasswordChangeForm, CustomPasswordResetForm,CustomPasswordResetConfirmForm
from django.contrib import messages
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import FormView, TemplateView, UpdateView
from django.db.models import Prefetch

User = get_user_model()

# Create your views here.

# Test for users
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

class SignUp(FormView):
    template_name = "registration/register.html"
    form_class = CustomRegistrationForm
    success_url = reverse_lazy("sign-in")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get("password1"))
        user.is_active = False
        user.save()

        messages.success(
            self.request,
            "A Confirmation mail sent. Please check your email"
        )

        return super().form_valid(form)

class SignIn(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('home')


class SignOut(LoginRequiredMixin, LogoutView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('sign-in')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')


@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    print(users)
    group = request.user.groups.first().name
    
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'admin/dashboard.html', {"users": users, "group":group})


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')

    return render(request, 'admin/assign_role.html', {"form": form})


class CreateGroup(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/create_group.html'
    login_url = 'no-permission'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', CreateGroupForm())
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('create-group')
    def test_func(self):
        return is_admin(self.request.user)


class GroupList(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/group_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.prefetch_related('permissions').all()
        return context
    def test_func(self):
        return is_admin(self.request.user)

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['group'] = user.groups.first().name
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['phone'] = user.phone
        context['profile_image'] = user.profile_image

        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context
    
class EditProfileView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')

class ChangePassword(LoginRequiredMixin,PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)