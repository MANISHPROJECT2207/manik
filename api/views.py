from django.shortcuts import render
import razorpay
from .models import Donation
from django.views.decorators.csrf import csrf_exempt

def payment(request):
    if request.method == 'POST':
        user = request.user
        amount = request.POST.get('amount')
        client = razorpay.client(auth = ("rzp_test_6PJ2rh7RU5EfGJ", "0qj3RitbQ5ctau1DJz5q52sm"))
        payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':1})
        donation = Donation(user=user, amount=amount, payment_id=payment['id'])
        return render(request, 'index.html', {'payment':payment})
        
    return render(request, 'payment.html')

@csrf_exempt
def success(request):
    if request.method == 'POST':
        a = request.POST
        print(a)
    return render(request, 'success.html')