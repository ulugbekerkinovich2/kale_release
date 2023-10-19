import csv
import os
import django
from django.conf import settings

# Assuming your CSV file is named 'products.csv' and is in the same directory as this script
csv_file_path = r'D:\kale\main_product.csv'

# Set the Django settings module for the script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()

from basic_app.models import Product, ProductCategory


def import_products_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            # Create a Product instance for each row in the CSV file
            product = Product.objects.create(
                title_ru=row['title_ru'],
                title_uz=row['title_uz'],
                title_en=row['title_en'],
                code=row['code'],
                unit=row['unit'],
                brand=row['brand'],
                proportions=row['proportions'],
                description_ru=row['description_ru'],
                description_uz=row['description_uz'],
                description_en=row['description_en'],
                manufacturer=row['manufacturer'],
                rest_count=float(row['rest_count']),
                price=float(row['price']),
                is_deleted=bool(row['is_deleted']),
                top_product=bool(row['top_product']),
            )
            # Assuming 'category_name' is a column in your CSV containing the category name
            category_name = row['category_id']
            # Get or create the category
            category, created = ProductCategory.objects.get_or_create(name_uz=category_name)
            # Assign the category to the product
            product.category = category
            product.save()


# Call the function with the path to your CSV file
import_products_from_csv(csv_file_path)
