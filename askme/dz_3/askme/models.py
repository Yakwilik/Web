import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils import timezone

import heapq


class TagManager(models.Manager):
    def top_tags(self, count=6):
        return self.annotate(questions=Count('tag_related')).order_by('-questions')[:count]


class AnswerManager(models.Manager):
    def count_likes(self):
        return self.annotate(Count("likes"))

    def hot(self):
        return self.order_by('-likes')

    def answer_by_question(self, id):
        return self.order_by('-pub_date').filter(question__id=id)


class QuestionManager(models.Manager):
    def get_by_id(self, id):
        return self.get(id=id)

    def count_likes(self, id):
        return self.get(id=id).get_likes()

    def by_tag(self, tag):
        return self.filter(tags__name=tag)

    def new(self):
        return self.order_by('-pub_date')

    def hot(self):
        heap = []
        questions = Question.objects.all()
        for question in questions:
            heap.append(question)

        heap.sort(key=lambda x: x.likes(), reverse=True)

        return heap


class ProfileManager(models.Manager):
    def get_top_users(self, count=6):
        return self.annotate(answers=Count('profile_related')).order_by('-answers')[:count]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='profile_related')
    avatar = models.ImageField(blank=True, null=True, upload_to="avatar/%Y/%m/%d", default='default_acc.jpg')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = 'Tags'


class Question(models.Model):
    title = models.CharField(max_length=256)

    text = models.TextField()

    pub_date = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, related_name='tag_related')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def likes(self):
        return LikeQuestion.objects.filter(question__id=self.id).count()

    def dislikes(self):
        return DisLikeQuestion.objects.filter(question__id=self.id).count()

    def like(self, profile):
        like = LikeQuestion.objects.filter(question_id=self.id, profile=profile)
        if like:
            like.delete()
        else:
            like = LikeQuestion(question_id=self.id, profile=profile)
            like.save()

    def dislike(self, profile):
        dislike = DisLikeQuestion.objects.filter(question_id=self.id, profile=profile)
        if dislike:
            dislike.delete()
        else:
            dislike = DisLikeQuestion(question_id=self.id, profile=profile)
            dislike.save()

    def answers(self):
        return Answer.objects.filter(question_id=self.id).count()

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['-pub_date']


class LikeQuestion(models.Model):
    question = models.ForeignKey(Question, related_name="question_like", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.user.username} {self.question.title}"


class DisLikeQuestion(models.Model):
    question = models.ForeignKey(Question, related_name="question_dislike", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.user.username} {self.question.title}"


class Answer(models.Model):
    text = models.TextField()

    pub_date = models.DateTimeField(auto_now_add=True)

    correct = models.BooleanField(default=False)

    author = models.ForeignKey(Profile, related_name='profile_related', on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, related_name='tag_related_a')

    question = models.ForeignKey(Question, related_name='answer_related', on_delete=models.CASCADE)

    objects = AnswerManager()

    def __str__(self):
        return '%s' % (self.author.user.username)

    def likes(self):
        return LikeAnswer.objects.filter(answer_id=self.id).count()

    def dislikes(self):
        return DisLikeAnswer.objects.filter(answer_id=self.id).count()

    def like(self, profile):
        like = LikeAnswer.objects.filter(answer_id=self.id, profile=profile)
        if like:
            like.delete()
        else:
            like = LikeAnswer(answer_id=self.id, profile=profile)
            like.save()

    def dislike(self, profile):
        dislike = DisLikeAnswer.objects.filter(answer_id=self.id, profile=profile)
        if dislike:
            dislike.delete()
        else:
            dislike = DisLikeAnswer(answer_id=self.id, profile=profile)
            dislike.save()

    def correct_input(self):
        if self.correct:
            self.correct = False
            self.save()
        else:
            self.correct = True
            self.save()

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ['-pub_date']


class LikeAnswer(models.Model):
    answer = models.ForeignKey(Answer, related_name="answer_like", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.user.username} {self.answer.question.title}"


class DisLikeAnswer(models.Model):
    answer = models.ForeignKey(Answer, related_name="answer_dislike", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.user.username} {self.answer.question.title}"