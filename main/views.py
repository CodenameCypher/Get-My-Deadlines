from django.shortcuts import render


def homepage(request):
    if request.method == 'POST':
        buX_email = request.POST.get('email')
        buX_password = request.POST.get('password')
        semester = request.POST.get('semester')
        print(semester)
        return render(request, 'results.html')
    return render(request, 'index.html')


def get_deadlines(request):
    if request.method == 'POST':
        print(request.POST.get('email'))
        return render(request, 'results.html')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def faq(request):
    return render(request, 'faq.html')
