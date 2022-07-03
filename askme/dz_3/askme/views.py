from django.shortcuts import render, redirect
from paginator import paginate
from askme.models import *
# Create your views here.

QUESTIONS = [
    {
        "title": f"Title number {i}",
        "text": f"This is my question number {i}"
    } for i in range(50)
]

HOT_QUESTIONS = [
    {
        "title": f"Title of hot question number {i}",
        "text": f"This is my hot question number {i}"
    } for i in range(50)
]


MEMBERS = ["MeetUpTeam", "yakwilik", "vkTeam", "Masharpik"]


users = Profile.objects.get_top_users(count=6)

top_tags = Tag.objects.top_tags(count=6)


def index(request):
    questions = Question.objects.new()
    page_questions = paginate(questions, request, 10)
    context = dict(questions=page_questions, tags=top_tags,
                   members=users, link_category="Популярные вопросы",
                   category="Новые вопросы", title="Главная")
    return render(request, "index.html", context)


def new_question(request):
    return render(request, "new_question.html", {"tags": top_tags, "members": users})


def one_question(request, question_id: int):
    return render(request, "one_question.html", {"tags": top_tags, "members": users})


def one_tag(request, i: str):
    questions = Question.objects.new()
    return render(request, "one_tag.html", {"questions": questions,
                                            "tags": top_tags, "members": users, "tag": i})


def registration(request):
    return render(request, "registr.html", {"tags": top_tags, "members": users})


def authentication(request):
    return render(request, "auth.html", {"tags": top_tags, "members": users})


def hot_questions(request):
    questions = Question.objects.hot()
    page_questions = paginate(questions, request, 10)
    category = 'Популярные вопросы'
    context = dict(questions=page_questions, tags=top_tags,
                   members=users, link_category="Новые вопросы",
                   category=category, title=category, redirect=True)
    return render(request, "index.html", context)
