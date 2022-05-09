from django.shortcuts import render

# Create your views here.

QUESTIONS = [
    {
        "title": f"Title number {i}",
        "text": f"This is my question number {i}"
    } for i in range(10 )
]

def index(request):
    return render(request, "index.html", {"questions": QUESTIONS})
