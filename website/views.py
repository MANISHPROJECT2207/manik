from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Subject, Profile
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
from django.utils.decorators import method_decorator
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
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request,'profile.html', {'user':request.user, 'profile':profile})

def courses(request):
    return render(request, 'courses.html')

def firstyear(request):
    return render(request, 'firstyear.html')

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
        user.save()
        profile = Profile.objects.get_object_or_404(user=user)
        if not profile: profile = Profile.objects.create(user = user)
        profile.save()
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
    items = Item.objects.filter(subject=subject)
    grouped_items = {}
    unit_ticks = {}

    for item in items:
        if item.unit not in grouped_items:
            grouped_items[item.unit] = []
            unit_ticks[item.unit] = False
        grouped_items[item.unit].append(item)
        if item.completed:
            unit_ticks[item.unit] = True

    total_units = len(grouped_items)
    year = subject.year
    a = Subject.objects.filter(year=1)
    b = Subject.objects.filter(year=2)
    c = Subject.objects.filter(year=3)
    d = Subject.objects.filter(year=4)
    g = Subject.objects.filter(year=0)

    return render(request, 'subject_desc.html', {
        'subject': subject,
        'items': items,
        'total_units': total_units,
        'grouped_items': grouped_items,
        'unit_ticks': unit_ticks,
        'year': year,
        'a': a, 'b': b, 'c': c, 'd': d, 'g': g,
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

@csrf_exempt
@login_required   
def update_views(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subject_id = data.get('subject_id')
        user = request.user

        try:
            subject = Subject.objects.get(id=subject_id)
            print(subject)
            if user not in subject.viewed_by.all():
                subject.views += 1
                subject.viewed_by.add(user)
                subject.save()
            return JsonResponse({'success': True, 'views': subject.views})
        except Subject.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Subject not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

def show_completed(request):
    subjects = Subject.objects.annotate(
        revision_count=Count('items', filter=Q(items__completed=True))
    )
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