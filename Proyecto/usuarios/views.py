from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def delete_user(request):

    user = request.user

    # try:

    user.delete()

    return render(request, 'delete.html')
