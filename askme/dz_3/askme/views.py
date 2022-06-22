from django.shortcuts import render, redirect
from paginator import paginate
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



first_row = {"1": "C++", "2": "Python", "3": "RUST"}
second_row = {"1": "C#", "2": "QT", "3": "GoLang"}
third_row = {"1": "Ruby", "2": "Java", "3": "PascalAbc"}

TAGS = [first_row, second_row, third_row]

tags = [f"tag{i % 2}" for i in range(30)]

QUESTIONS_WITH_TAGS = [
    {
        "title": f"Title of hot question number {i}",
        "text": f"This is my hot question number {i}",
        "tag": tags[i]
    } for i in range(30)
]


MEMBERS = ["MeetUpTeam", "yakwilik", "vkTeam", "Masharpik"]


# TAGS = ["C++", "Python", "RUST", "C#", "SQL", "GoLang", "Ruby", "Java", "JavaScript", "PascalAbc"]


def index(request):
    page_questions = paginate(QUESTIONS, request, 5)
    return render(request, "index.html", {"questions": page_questions, "tags": TAGS, "members": MEMBERS})


def new_question(request):
    return render(request, "new_question.html", {"questions": QUESTIONS, "tags": TAGS, "members": MEMBERS})


def one_question(request, i: int):
    return render(request, "one_question.html", {"questions": QUESTIONS,
                                                 "tags": TAGS, "members": MEMBERS})


def one_tag(request, i: str):
    print(i)
    for question in QUESTIONS_WITH_TAGS:
        print(question["tag"])
    return render(request, "one_tag.html", {"questions": QUESTIONS_WITH_TAGS,
                                                 "tags": TAGS, "members": MEMBERS, "tag": i})


def registration(request):
    return render(request, "registr.html", {"questions": QUESTIONS,
                                                 "tags": TAGS, "members": MEMBERS})


def authentication(request):
    return render(request, "auth.html", {"questions": QUESTIONS,
                                                 "tags": TAGS, "members": MEMBERS})


def hot_question(request):
    page_questions = paginate(HOT_QUESTIONS, request, 5)
    return render(request, "hot.html", {"questions": page_questions, "tags": TAGS, "members": MEMBERS})


