from django.core.management.base import BaseCommand
from form_and_game.models import *
from faker import Faker
from random import randint
from form_and_game.management.commands.villes import VILLES

class Command(BaseCommand):

    """
    This function executes whenever the command is called. It takes care of creating
    meaningful fake rows in the ranking to prevent it from ever being empty.
    We want:
        8 players ranked higher than one can be ranked if just doing the introduction form
            This player should be in increasing difficulty to beat (one can be beat by just sharing once,
            the other by just sharing twice, and then you need a form.)
        12 players ranked below that person 
    """

    def __init__(self):
        super().__init__()
        self.faker = Faker('fr_FR')
        Faker.seed(0)
        self.number_points_after_introduction_form = 745
        self.number_higher_ranked = 8
        self.number_lower_ranked = 12

    def handle(self, *args, **options):
       self.create_higher_ranked_players()
       self.create_lower_ranked_players()

    def create_higher_ranked_players(self):
        for i in range(self.number_higher_ranked):
            _user = self.create_random_user()
            player = Player.objects.create(
                user = _user,
                points = self.number_points_after_introduction_form + randint((i-1)*100,(i*100)) + randint(1,50),
            )   
            GeneralIntroductionFormAnswer.objects.create(player=player,ville=VILLES[randint(0,len(VILLES)-1)],metier="Chef de cuisine et pâtissier propriétaire",age=12,experience=12,nombre_couverts=13,nombre_places=15,nombre_cuisiniers=13,prix_moyen_couvert=25)

    
    def create_lower_ranked_players(self):
        for i in range(self.number_lower_ranked):
            _user = self.create_random_user()
            player = Player.objects.create(
                user = _user,
                points = self.number_points_after_introduction_form - randint(1,self.number_points_after_introduction_form//10)*10,
            )   
            GeneralIntroductionFormAnswer.objects.create(player=player,ville=VILLES[randint(0,len(VILLES)-1)],metier="Chef de cuisine et pâtissier propriétaire",age=12,experience=12,nombre_couverts=13,nombre_places=15,nombre_cuisiniers=13,prix_moyen_couvert=25)
   
    def create_random_user(self):
        _first_name = self.faker.first_name(),
        _last_name = self.faker.last_name()
        return User.objects.create(
                first_name = _first_name[0].lower(),
                last_name = _last_name.lower(),
                email = f"{_first_name[0][0].lower()}{_last_name.lower()}@{self.faker.domain_name()}",
                randomly_created = True
            )