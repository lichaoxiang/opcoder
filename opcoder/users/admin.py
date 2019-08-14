from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import UserProfile


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)
    class Meta:
        model = UserProfile
        fields = ('username', 'email', )
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'is_active')
    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        ('基础信息', {'fields': (('username', 'password'), ('email', 'mobile'), )}),
        ('权限信息', {'fields': (('is_active', 'is_staff', 'is_superuser'), 'groups', 'user_permissions')}),
        ('重要日期', {'fields': (('last_login', 'date_joined'), )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('username', 'email'), ('password1', 'password2'), )}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username', 'email',)
    filter_horizontal = ()


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        ('基础信息', {'fields': (('username', 'password'), ('email', 'mobile'), )}),
        ('权限信息', {'fields': (('is_active', 'is_staff', 'is_superuser'), 'groups', 'user_permissions')}),
        ('重要日期', {'fields': (('last_login', 'date_joined'), )}),
    )
    search_fields = ('username', 'email')
admin.site.register(UserProfile, UserAdmin)