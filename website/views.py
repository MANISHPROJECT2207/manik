from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Subject
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from django.contrib import messages
from manik.settings import BASE_DIR
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

def about(request):
    return render(request, 'about.html')

def home(request):
    top_subjects = Subject.objects.order_by('-views')[:3]
    total_users = User.objects.all().count()
    return render(request, 'index.html', {'top_subjects':top_subjects, 'total_users':total_users})

def testimonial(request):
    return render(request, 'testimonial.html')

def _404_error(request):
    return render(request, '404.html')

def courses(request):
    return render(request, 'courses.html')

def subjectpages(request):
    items = Item.objects.all()
    numerator = items.filter(status="completed").count()
    denominator = items.count()
    subjects = Subject.objects.all()
    a = Subject.objects.all().filter(year = 1)
    b = Subject.objects.all().filter(year = 2)
    c = Subject.objects.all().filter(year = 3)
    d = Subject.objects.all().filter(year = 4)
    g = Subject.objects.all().filter(year = 0)
    return render(request, 'subjectpages.html', {
        'items' : items,
        'subjects' : subjects,
        'numerator':numerator,
        'denominator':denominator,
        'a':a, 'b':b, 'c':c, 'd':d, 'g':g
    })

def contact(request):
    return render(request, 'contact.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        x = request.POST.get('ue')
        password = request.POST.get('password')
        user = authenticate(request, username=x, password=password)
        if user is None:
            user = authenticate(request, email=x, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
            
    return render(request, 'signin.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pswd = request.POST.get('password')
        p2 = request.POST.get('p2')
        username = request.POST.get('username')
        
        if pswd != p2:
            return redirect('register')

        try:
            user = User.objects.create_user(email=email, password=pswd, username=username)
            user.save()
        except Exception as e:
            return redirect('register')

        # Attempt to authenticate the user
        user = authenticate(request, email=email, password=pswd)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('home')
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return redirect('home')


def search(request):
    items = Item.objects.all()
    query = request.GET.get('query', '')
    subjects = Subject.objects.all()
    numerator = items.filter(status="completed").count()
    denominator = items.count()
    if query:
        items = items.filter(Q(description__icontains=query) | Q(title__icontains=query))
        subjects = subjects.filter(Q(name__icontains=query) | Q(branch__icontains=query))
    return render(request, 'subjectpages.html', {
        'items': items,
        'subjects': subjects,
        'numerator':numerator,
        'denominator':denominator,
        'query': query,
    })
    
    
@csrf_exempt
@require_POST
def status_completed(request):
    data = json.loads(request.body)
    item_id = data.get('item_id')
    status = data.get('status')
    
    try:
        item = Item.objects.get(id=item_id)
        item.status = "completed" if status else 'not_completed'
        item.save()
        return JsonResponse({'success': True})
    except Item.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@csrf_exempt
@require_POST
def revision(request):
    data = json.loads(request.body)
    item_id = data.get('item_id')
    rev = data.get('revision')

    try:
        item = Item.objects.get(id=item_id)
        print(f"Before: Item {item_id} revision={item.revision}")
        item.revision = rev
        item.save()
        print(f"After: Item {item_id} revision={item.revision}")
        return JsonResponse({'success': True})
    except Item.DoesNotExist:
        print(f"Item {item_id} not found")
        return JsonResponse({'success': False, 'error': 'Item not found'})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'success': False, 'error': str(e)})

    
def show_revision(request):
    subjects = Subject.objects.annotate(
        revision_count=Count('items', filter=Q(items__revision=True))
    ).filter(revision_count__gt=0)
    items = Item.objects.all().filter(revision=True)
    total_items = items.count()
    a = Subject.objects.all().filter(year = 1)
    b = Subject.objects.all().filter(year = 2)
    c = Subject.objects.all().filter(year = 3)
    d = Subject.objects.all().filter(year = 4)
    g = Subject.objects.all().filter(year = 0)
    return render(request, 'show_revision.html', {'items':items, 'subjects': subjects,
        'a':a, 'b':b, 'c':c, 'd':d, 'g':g,
        'total_items':total_items
    })
    
def subject_desc(request, sub_name):
    subject = Subject.objects.get(name=sub_name)
    subjects = Subject.objects.all()
    if subject : items = Item.objects.all().filter(subject=subject)
    numerator = items.filter(status="completed").count()
    denominator = items.count()
    subjects = Subject.objects.all()
    a = Subject.objects.all().filter(year = 1)
    b = Subject.objects.all().filter(year = 2)
    c = Subject.objects.all().filter(year = 3)
    d = Subject.objects.all().filter(year = 4)
    g = Subject.objects.all().filter(year = 0)
    return render(request, 'subject_desc.html', {
        'subject':subject,
        'items':items,
        'numerator':numerator,
        'denominator':denominator,
        'subjects':subjects,
        'a':a, 'b':b, 'c':c, 'd':d, 'g':g
        })
    

@login_required
@require_POST
@csrf_exempt
def like_item(request):
    import json
    data = json.loads(request.body)
    item_id = data.get('item_id')
    liked = data.get('liked')

    try:
        item = Item.objects.get(id=item_id)
        user = request.user

        if liked:
            item.likes += 1
            item.liked_by.add(user)
        else:
            item.likes -= 1
            item.liked_by.remove(user)
        
        item.save()

        return JsonResponse({'success': True, 'likes': item.likes})
    except Item.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'})
    
def year(request, year):
    subjects = Subject.objects.all().filter(year=year)
    items = Item.objects.filter(subject__in=subjects)
    numerator = items.filter(status="completed").count()
    denominator = items.count()
    
    print(type(subjects))
    
    a = Subject.objects.all().filter(year = 1)
    b = Subject.objects.all().filter(year = 2)
    c = Subject.objects.all().filter(year = 3)
    d = Subject.objects.all().filter(year = 4)
    g = Subject.objects.all().filter(year = 0)
    return render(request, 'year.html', {
        'subjects':subjects,
        'items':items,
        'numerator':numerator,
        'denominator':denominator,
        'subjects':subjects,
        'a':a, 'b':b, 'c':c, 'd':d, 'g':g,
        'year':year
        })