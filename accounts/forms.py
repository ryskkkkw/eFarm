from django import forms

from django.conf import settings

from .models import CustomUser

class CustomUserForm(forms.ModelForm):
  password1 = forms.CharField(label='Password',
                              min_length=8,
                              widget=forms.PasswordInput)
  password2 = forms.CharField(label='password confirmation',
                              min_length=8,
                              widget=forms.PasswordInput)
  
  class Meta:
    model = CustomUser
    fields = ['email']
    
  def clean_password2(self):
    password1 = self.cleaned_data['password1']
    password2 = self.cleaned_data['password2']
    if password1 and password2 and password1 != password2:
      raise ValueError("Passwords don't match")
    return password2
  
  def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data['password1'])
    if commit:
      user.save()
    return user