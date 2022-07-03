from django.core.management.base import BaseCommand
from askme.models import *
from django.contrib.auth.models import User
from django.utils.timezone import timezone

import requests
import random
import datetime
import copy


class Command(BaseCommand):
    RANDOM_API_KEY = '78c7df1074544d209e549dc135589056'
    RANDOM_TEXT_API = 'https://randommer.io/api/Text/LoremIpsum'
    RANDOM_NAME_API = 'https://randommer.io/api/Name'
    PARAGRAPHS_AMOUNT = 1

    SCALE = 1000
    USERS_NEEDS = 100000 // SCALE
    QUESTIONS_NEEDS = 1000000 // SCALE
    ANSWERS_NEEDS = 1000000 // SCALE
    TAGS_NEEDS = 10000 // SCALE
    LIKES_NEEDS = 2000000 // SCALE

    TITLE_LEN = 10
    MIN_TEXT_LEN = 20
    MAX_TEXT_LEN = 100
    MAX_ANSWERS = 10
    MAX_TAGS = 3

    MAX_LIKES = USERS_NEEDS
    MAX_DISLIKES = 5

    def __init__(self):
        super().__init__()
        self.text_dataset = self.generate_words_dataset()
        self.names_set = self.generate_names_set()

    def generate_words_dataset(self):
        params = {'loremType': 'normal', 'type': 'paragraphs', 'number': self.PARAGRAPHS_AMOUNT}
        r = requests.get(
            self.RANDOM_TEXT_API,
            params=params,
            headers={'X-Api-Key': self.RANDOM_API_KEY}
        )
        return r.text.split()

    def generate_names_set(self):
        params = {'nameType': 'fullname', 'quantity': 100}
        r = requests.get(
            self.RANDOM_NAME_API,
            params=params,
            headers={'X-Api-Key': self.RANDOM_API_KEY}
        )
        return r.json()

    def create_text_by_word_length(self, len):
        result_string = str()
        for i in range(len):
            result_string = result_string + random.choice(self.text_dataset) + ' '
        return result_string

    def create_users_and_ref_profiles(self):
        def create_user(user_counter):
            name_choice = f'{random.choice(self.names_set)}{user_counter}'
            name_split = name_choice.split()
            pwd = f'{random.choice(self.text_dataset)}{random.choice(self.text_dataset)}{random.choice(self.text_dataset)}'
            user_dict_repr = {
                'username': name_choice,
                'first_name': name_split[0],
                'last_name': name_split[1],
                'password': pwd,
                'email': f'{random.choice(self.text_dataset)}@domen.mail',
                'is_staff': False,
                'is_active': True,
                'is_superuser': False,
                'last_login': datetime.datetime.now(tz=timezone.utc),
            }
            return user_dict_repr

        users_set = []
        profiles_set = []
        for i in range(self.USERS_NEEDS):
            user = User.objects.create_user(**create_user(i))
            user.save()
            users_set.append(user)
            profile = Profile(user=user)
            profiles_set.append(profile)

        Profile.objects.bulk_create(profiles_set)

    def create_questions(self, users):
        def create_question(profile):
            question_fields = {
                'title': self.create_text_by_word_length(self.TITLE_LEN),
                'text': self.create_text_by_word_length(random.randint(self.MIN_TEXT_LEN, self.MAX_TEXT_LEN)),
                'pub_date': datetime.datetime.now(tz=timezone.utc),
                'author': profile,
            }
            return question_fields

        questions_set = []
        for i in range(self.QUESTIONS_NEEDS):
            question = Question(**create_question(random.choice(users)))
            questions_set.append(question)

        Question.objects.bulk_create(questions_set)

    def create_answers(self, users, questions):
        def create_answer(profile, question):
            answer_fields = {
                'text': self.create_text_by_word_length(random.randint(self.MIN_TEXT_LEN, self.MAX_TEXT_LEN)),
                'correct': random.choice([True, False]),
                'pub_date': datetime.datetime.now(tz=timezone.utc),
                'question': question,
                'author': profile,
            }
            return answer_fields

        answers_created_indicate = self.ANSWERS_NEEDS
        answers_set = []
        while answers_created_indicate > 0:
            one_question_answers_count = random.randint(0, self.MAX_ANSWERS)
            answers_created_indicate -= one_question_answers_count
            for i in range(one_question_answers_count):
                answer = Answer(**create_answer(random.choice(users), random.choice(questions)))
                answers_set.append(answer)

        Answer.objects.bulk_create(answers_set)

    def create_tags(self):
        tags_created_indicate = self.TAGS_NEEDS
        tags_set = []

        while tags_created_indicate > 0:
            tag = Tag(name=self.text_dataset.pop(random.randint(0, len(self.text_dataset) - 1)))
            tags_set.append(tag)
            tags_created_indicate -= 1

        Tag.objects.bulk_create(tags_set)

    def set_tags(self, questions, tags):
        for question in questions:
            for i in range(self.MAX_TAGS):
                question.tags.add(random.choice(tags))

    def create_likes_question(self, profiles, questions):
        def create_like(profile, question):
            like_fields = {
                'profile': profile,
                'question': question
            }
            return like_fields

        likes_created_indicate = self.LIKES_NEEDS
        likes_set = []
        while likes_created_indicate > 0:
            one_question_like_amount = random.randint(0, self.MAX_LIKES)

            likes_created_indicate -= one_question_like_amount

            rand_profile = profiles.pop(random.randint(0, len(profiles) - 1))

            copy_question = copy.copy(questions)
            for i in range(one_question_like_amount):
                rand_question = copy_question.pop(random.randint(0, len(copy_question) - 1))

                like = LikeQuestion(**create_like(rand_profile, rand_question))

                likes_set.append(like)

        LikeQuestion.objects.bulk_create(likes_set)

    def create_dislikes_question(self, profiles, questions):
        def create_dislike(profile, question):
            dislike_fields = {
                'profile': profile,
                'question': question
            }
            return dislike_fields

        dislikes_created_indicate = self.LIKES_NEEDS
        dislikes_set = []
        while dislikes_created_indicate > 0:
            one_question_dislike_amount = random.randint(0, self.MAX_LIKES)

            dislikes_created_indicate -= one_question_dislike_amount

            rand_profile = profiles.pop(random.randint(0, len(profiles) - 1))

            copy_question = copy.copy(questions)
            for i in range(one_question_dislike_amount):
                rand_question = copy_question.pop(random.randint(0, len(copy_question) - 1))

                dislike = DisLikeQuestion(**create_dislike(rand_profile, rand_question))

                dislikes_set.append(dislike)

        DisLikeQuestion.objects.bulk_create(dislikes_set)

    def create_likes_answer(self, profiles, answers):
        def create_like(profile, answer):
            like_fields = {
                'profile': profile,
                'answer': answer
            }
            return like_fields

        likes_created_indicate = self.LIKES_NEEDS
        likes_set = []
        while likes_created_indicate > 0:
            one_answer_like_amount = random.randint(0, self.MAX_LIKES)

            likes_created_indicate -= one_answer_like_amount

            rand_profile = profiles.pop(random.randint(0, len(profiles) - 1))

            copy_answers = copy.copy(answers)
            for i in range(one_answer_like_amount):
                rand_answer = copy_answers.pop(random.randint(0, len(copy_answers) - 1))

                like = LikeAnswer(**create_like(rand_profile, rand_answer))

                likes_set.append(like)

        LikeAnswer.objects.bulk_create(likes_set)

    def create_dislikes_answer(self, profiles, answers):
        def create_dislike(profile, answer):
            dislike_fields = {
                'profile': profile,
                'answer': answer
            }
            return dislike_fields

        dislikes_created_indicate = self.LIKES_NEEDS
        dislikes_set = []
        while dislikes_created_indicate > 0:
            one_answer_dislike_amount = random.randint(0, self.MAX_LIKES)

            dislikes_created_indicate -= one_answer_dislike_amount

            rand_profile = profiles.pop(random.randint(0, len(profiles) - 1))

            copy_answers = copy.copy(answers)
            for i in range(one_answer_dislike_amount):
                rand_answer = copy_answers.pop(random.randint(0, len(copy_answers) - 1))

                dislike = DisLikeAnswer(**create_dislike(rand_profile, rand_answer))

                dislikes_set.append(dislike)

        DisLikeAnswer.objects.bulk_create(dislikes_set)

    def handle(self, *args, **options):
        self.create_users_and_ref_profiles()
        profiles = Profile.objects.all()
        tags = Tag.objects.all()
        self.create_tags()

        self.create_questions(profiles)
        questions = Question.objects.all()
        self.set_tags(questions, tags)

        self.create_answers(profiles, questions)
        answers = Answer.objects.all()
        self.set_tags(answers, tags)

        list_profiles = []
        for profile in profiles:
            list_profiles.append(profile)

        list_questions = []
        for question in Question.objects.all():
            list_questions.append(question)

        list_answers = []
        for answer in Answer.objects.all():
            list_answers.append(answer)

        self.create_likes_question(copy.copy(list_profiles), list_questions)
        self.create_dislikes_question(list_profiles, list_questions)

        self.create_likes_answer(copy.copy(list_profiles), list_answers)
        self.create_dislikes_answer(copy.copy(list_profiles), list_answers)

        self.stdout.write(self.style.SUCCESS('SUCCESS'))