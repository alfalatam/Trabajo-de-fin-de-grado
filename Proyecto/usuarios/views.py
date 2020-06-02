from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def delete_user(request):

    user = request.user

    # try:
    user.delete()
    # messages.success(request, "The user is deleted")

    # messages.error(request, "User not exist")
    # return render(request, 'profile.html')

    # except Exception as e:
    #     print('No se ha podido borrar el usuario ')
    #     return render(request, 'profile.html', {'err': e.message})

    return render(request, 'delete.html')
