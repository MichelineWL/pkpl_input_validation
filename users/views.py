from django.shortcuts import render
from .forms import UserForm  # Pastikan ini ada

def user_form_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            return render(request, 'users/success.html', {'form': form.cleaned_data})
    else:
        form = UserForm()

    return render(request, 'users/form.html', {'form': form})
