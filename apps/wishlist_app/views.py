from django.shortcuts import render, redirect
from .models import User, Item, Wishlist
from django.contrib import messages
# Create your views here.
# urlpatterns = [
#     url(r'^dashboard/$', views.dashboard),
#     url(r'^/wish_items/add$', views.add_wishitem),
#     url(r'^/wish_items/create$', views.create_item),
#     url(r'^/wish_items/(?P<id>\d+)$', views.item_users),
# ]

def index(request):
    return render(request, 'wishlist_app/index.html')

def process(request):
    if request.method == 'POST':
        no_errors = User.objects.check_registration_form(request)
        if no_errors == False:
            return redirect('/')
        else:
            User.objects.create(name=request.POST['name'], email=request.POST['email'], password=request.POST['password'])
            messages.success(request,'Thank you for registering!')
            user = User.objects.get(email=request.POST['email'])
            request.session['name'] = user.name
            request.session['user_id'] = user.id
            return redirect('/dashboard/')

def login(request):
    if request.method == 'POST':
        no_validation_error = User.objects.verify_login(request)
    try:
        user = User.objects.get(email=request.POST['email'])
        if no_validation_error == True:
            request.session['name'] = user.name
            request.session['user_id'] = user.id
            return redirect('/dashboard/')
    except:
        messages.error(request, 'Email format not valid')
        return redirect('/')

def success(request):
    return render(request, '/dashboard/', context)

def dashboard(request):
    return render(request, 'wishlist_app/dashboard.html')

def add_wishitem(request):
    return render(request, 'wishlist_app/create.html')

def create_item(request):
    if request.method == 'POST':
        print request.POST
        if len(request.POST['item']) < 3:
            messages.error(request, 'Please enter a real item!')
            return redirect('/wish_items/add/')
        else:
            current_user = User.objects.get(pk=request.session['user_id'])
            current_user.save()
            new_item = Item.objects.create(name=request.POST['item'])
            new_item.save()

            add_wishlist = Wishlist.objects.create(item=new_item, user = current_user)
            add_wishlist.save()
            # add_wishlist = Wishlist.objects.create(item=new_item, user=current_user)
            # add_wishlist.save()
    return redirect('/dashboard/')

def item_users(request,id):
    context = {
    # 'same_item': User.objects.filter(user.id=user_item.id)
    }
    return render(request, 'wishlist_app/wish_item.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')
