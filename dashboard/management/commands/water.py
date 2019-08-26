from django.core.management.base import BaseCommand, CommandError
from dashboard.models import Garden, Plant

class Command(BaseCommand):
    help = 'Waters the specified plant'

    def add_arguments(self, parser):
        parser.add_argument('plant_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for plant_id in options['plant_ids']:
            try:
                garden = Garden.objects.get(garden_name="NYC Apartment")
                plant = garden.plant_set.get(pk=plant_id)
            except Plant.DoesNotExist:
                raise CommandError('Plant "%s" does not exist' % plant_id)

            plant.water()

            self.stdout.write(self.style.SUCCESS('Successfully watered plant "%s"' % plant_id))