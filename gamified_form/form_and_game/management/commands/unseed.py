from django.core.management.base import BaseCommand
from form_and_game.models import *

class Command(BaseCommand):

    """
    This function executes whenever the command is called. It takes care of emptying all of the
    tables present in our database.
    """
    def handle(self, *args, **options):
        Player.objects.all().delete()
        User.objects.filter(is_staff=False, is_superuser=False).delete()
        GeneralIntroductionFormAnswer.objects.all().delete()
        ComptaFormAnswer.objects.all().delete()
        CommandeFormAnswer.objects.all().delete()
        ConnaissanceAchatFormAnswer.objects.all().delete()
        RecetteFormAnswer.objects.all().delete()
        CarteFormAnswer.objects.all().delete()
        FonctionnalitesPrefereesFormAnswer.objects.all().delete()
        ExtraInformation.objects.all().delete()