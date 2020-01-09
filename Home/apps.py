from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'Home'

    def ready(self):
        import Home.signals
