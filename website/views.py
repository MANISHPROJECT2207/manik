from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Subject, Profile, Unit, Feedback
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


Branches = [
    ("Common", "common/all"),
    ("CSE.", "computer science and engg"),
    ("EC.","electronics and comm."),
    ("Elec.","electrical"),
    ("IT.", "information technology"),
    ("Mech.", "mechanical"),
    ("Civil", "civil"),
    ("AI.", "Artificial Intelligence"),
]

def about(request):
    return render(request, 'about.html')

def test(request):
    return render(request, 'test.html')

def home(request):
    top_subjects = Subject.objects.order_by('-views')[:3]
    total_users = User.objects.all().count()
    popular = Subject.objects.all().order_by('-views')[:8]
    subject_list = []
    user = request.user
    try:
        for subject in popular:
                total_items = Item.objects.all().filter(subject=subject).count()
                completed_items  = Item.objects.all().filter(completed_by=user, subject=subject).count()
            
                if total_items > 0: progress = int((completed_items / total_items) * 100)
                else: progress = 0
                
                subject_data = {
                    'subject': subject,
                    'progress': progress
                }
                subject_list.append(subject_data)
    except Exception as e:
        pass
        
    if request.method == 'POST':
        x = request.POST.get('feedback')
        feedback = Feedback.objects.create(user=request.user, text=x)
        feedback.save()
        return redirect('home')
    
    return render(request, 'index.html', {
        'top_subjects':top_subjects,
        'total_users':total_users,
        'popular':popular,
        'subject_list':subject_list,
        })

def testimonial(request):
    return render(request, 'testimonial.html')

def _404_error(request):
    return render(request, '404.html')

def profile(request): 
    profile, created = Profile.objects.get_or_create(user=request.user)
    branch_dict = {}
    for branch_code, branch_name in Subject._meta.get_field('branch').choices:
        subjects = Subject.objects.filter(branch=branch_code, year=profile.year)
        
        subject_list = []
        for subject in subjects:
            total_units = Item.objects.all().count()
            completed_units = Item.objects.all().filter(subject=subject, completed_by=request.user).count()
         
            if total_units > 0:
                progress = (completed_units / total_units) * 100
            else:
                progress = 0
            
            subject_data = {
                'subject': subject,
                'progress': progress
            }
            subject_list.append(subject_data)
        
        branch_dict[branch_name] = subject_list
        
    print(branch_dict)
   
    return render(request,'profile.html', {'user':request.user, 'profile':profile,
    'Branches': Branches, 'branch_dict':branch_dict})

def courses(request):
    return render(request, 'courses.html')

def contact(request):
    return render(request, 'contact.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        x = request.POST.get('ue')
        password = request.POST.get('password')
        user = authenticate(request, username=x, password=password)
        
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
            return render(request, 'register.html')

        user = authenticate(request, email=email, password=pswd)
        
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return redirect('home')


def search(request):
    items = Item.objects.all()
    query = request.GET.get('query', '')
    subjects = Subject.objects.all()
    if query:
        items = items.filter(Q(description__icontains=query) | Q(title__icontains=query))
        subjects = subjects.filter(Q(name__icontains=query) | Q(branch__icontains=query))
    return render(request, 'base.html', {
        'items': items,
        'subjects': subjects,
        'query': query,
    })
    
    
@csrf_exempt
@require_POST
def status_completed(request):
    data = json.loads(request.body)
    item_id = data.get('item_id')
    status = data.get('status')
    user = request.user
    
    try:
        item = Item.objects.get(id=item_id)
        unit = Unit.objects.get(number=item.unit, subject=item.subject)
        if status:
            item.completed_by.add(user)
        else:
            item.completed_by.remove(user)
            
        all_items = Item.objects.filter(unit=unit)
        for item in all_items:
            if item.completed_by == False:
                unit.completed_by.remove(user)
                print("booyah")
                break
            else: unit.completed_by.add(user)
        item.save()
        unit.save()
        
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
    user = request.user 
    
    try:
        item = Item.objects.get(id=item_id)
        item.revision = rev
        if item.revision == True:
            item.revision_by.add(user)
        else:
            item.revision_by.remove(user)
        item.save()
        return JsonResponse({'success': True})
    except Item.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

    
def show_revision(request, subject):
    subject = Subject.objects.get(name=subject)
    user = request.user
    if user is not None or user.is_authenticated:
        items = Item.objects.all().filter(revision_by=user, subject=subject)
    else: items = Item.objects.all().filter(subject=subject)
    total_items = items.count()
    grouped_items = {}
    for item in items:
        unit = Unit.objects.get(subject=subject, number=item.unit)
        if unit not in grouped_items: grouped_items[unit] = []
        grouped_items[unit].append(item)

    total_units = len(grouped_items)
    year = subject.year
    a = Subject.objects.all().filter(year = 1)
    b = Subject.objects.all().filter(year = 2)
    c = Subject.objects.all().filter(year = 3)
    d = Subject.objects.all().filter(year = 4)
    g = Subject.objects.all().filter(year = 0)
    return render(request, 'subject_desc.html', {'subject': subject,
        'a':a, 'b':b, 'c':c, 'd':d, 'g':g,
        'total_items':total_items,
        'items': items,
        'total_units': total_units,
        'grouped_items': grouped_items,
        'year': year,
    })
    
def subject_desc(request, sub_name):
    user = request.user
    subject = Subject.objects.get(name=sub_name)
    if not subject.viewed_by.filter(id=user.id).exists():
        subject.viewed_by.add(user)
        x = subject.views
        subject.views = x + 1
        subject.save()
    items = Item.objects.filter(subject=subject)
    grouped_items = {}
    units = Unit.objects.filter(subject=subject).order_by('number')
    for unit in units:
        grouped_items[unit] = []
    for item in items:
        unit = Unit.objects.all().filter(subject=subject, number=item.unit).first()
        grouped_items[unit].append(item)

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
    user = request.user
    numerator = items.filter(completed_by=user).count()
    denominator = items.count()
    
    branch_dict = {}
    for branch_code, branch_name in Subject._meta.get_field('branch').choices:
        subjects = Subject.objects.filter(branch=branch_code, year=year)
        subject_list = []
        for subject in subjects:
            total_topics = Item.objects.all().count()
            completed_topics = Item.objects.all().filter(completed_by=user, subject=subject).count()
        
            if total_topics > 0: progress = int((completed_topics  / total_topics) * 100)
            else: progress = 0
            
            subject_data = {
                'subject': subject,
                'progress': progress
            }
            subject_list.append(subject_data)
        
        branch_dict[branch_name] = subject_list
    print(branch_dict)
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
        'year':year,
        'branches':branch_dict,
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
    
# seperate page waala
def editprofile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        year = request.POST.get('year')
        branch = request.POST.get('branch')
        
        if username: 
            user.username = username
        if email: 
            user.email = email
        if year: 
            profile.year = year
        if branch and branch in dict(Branches).keys():
            profile.branch = branch
        
        user.save()
        profile.save()

        return render(request, 'profile.html', {'profile': profile, 'Branches': Branches,'user':user})

    return render(request, 'editprofile.html', {'profile': profile, 'Branches': Branches,'user':user})
    
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        year = request.POST.get('year')
        branch = request.POST.get('branch')
        
        if username: 
            user.username = username
        if email: 
            user.email = email
        if year: 
            profile.year = year
        if branch and branch in dict(Branches).keys():
            profile.branch = branch
        
        user.save()
        profile.save()

        return render(request, 'profile.html', {'profile': profile, 'Branches': Branches,'user':user})

    return render(request, 'profile.html', {'profile': profile, 'Branches': Branches,'user':user})

@login_required
def feedback(request):
    if request.method == 'POST':
        x = request.POST.get('feedback')
        feedback = Feedback.objects.create(user=request.user, text=x)
        feedback.save()
        return redirect('home')
    return render(request, 'feedback.html')