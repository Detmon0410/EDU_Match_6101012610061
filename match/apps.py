from django.apps import AppConfig


class MatchConfig(AppConfig):
    name = 'match'

    def ready(self):
        import match.signals


class UsersConfig(AppConfig):
    name = 'match'

    def ready(self):
        import match.signals
