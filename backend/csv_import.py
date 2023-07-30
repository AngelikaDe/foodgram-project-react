import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')
django.setup()

from api.models import Ingredient


def import_data_from_csv(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name = row[0]
            measurement_unit = row[1]
            existing_ingredient = Ingredient.objects.filter(
                name=name).first()

            if not existing_ingredient:
                ingredient = Ingredient.objects.create(
                    name=name, measurement_unit=measurement_unit)
                print(f"Created ingredient: {ingredient}")
            else:
                print(
                    f"Ingredient '{name}' already exists in the database.")


if __name__ == '__main__':
    csv_file_path = '../data/ingredients.csv'
    import_data_from_csv(csv_file_path)
