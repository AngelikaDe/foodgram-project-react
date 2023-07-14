from django.shortcuts import render
from .models import CustomUser

def user_profile(request, username):
    user = CustomUser.objects.get(username=username)
    # other logic for handling subscription, favorite, shopping list, etc.

    context = {'user': user}
    return render(request, 'users/user_profile.html', context)

# other views for subscriptions, favorite, shopping list, etc.
