from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.text_dataset = [{"hello": "greeting"}, {"goodbye": "bying"}]

    def handle(self, *args, **options):
        print(self.text_dataset[::-1])
    #     print(type(self.text_dataset))


command = Command()

command.handle()
