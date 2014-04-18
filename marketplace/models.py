import datetime

from django.db import models

from accounts.models import DubizzleUser


class GenericMotorAd(models.Model):
    USED_CARS = 0
    MOTORCYCLES = 1
    CATEGORY_ID = (
        (USED_CARS, 'Used Cars for Sale', '/motors/used-cars/'),
        (MOTORCYCLES, 'Motorcycles', '/motors/motorcycles/'),
    )

    CATEGORY_DICT = {'used-cars': 'used-cars', 'motorcycles': 'motorcycles'}

    SELLER = (
        (1, 'Owner'),
        (2, 'Dealer'),
    )

    WARRANTY = (
        (1, 'Does not apply'),
        (2, 'Yes'),
        (3, 'No'),
    )

    BODY_COND = (
        (1, 'Perfect inside and out'), (2, 'No accidents, very few faults'),
    )

    MECH_COND = (
        (1, 'Perfect inside and out'), (2, 'Minor faults, all fixed'),
    )

    LOCATION = (
        (1, 'Abu Hail'), (2, 'Acacia Avenues'), (3, 'Academic City'),
        (4, 'Akoya'), (5, 'Al Barari'),
    )

    title = models.CharField(max_length=250, blank=False)
    phone = models.PositiveIntegerField(blank=False)
    price = models.PositiveIntegerField(blank=False)
    description = models.TextField(blank=False)
    seller_type = models.IntegerField(choices=SELLER, blank=False)
    warranty = models.IntegerField(choices=WARRANTY, blank=False)
    location = models.IntegerField(choices=LOCATION, blank=False)
    publisher = models.ForeignKey(DubizzleUser)

    category_id = None

    class Meta:
        abstract = True


class MotorCycleAd(GenericMotorAd):
    AGE = (
        (1, 'Brand New'), (2, '0-1 month'),
    )

    USAGE = (
        (1, 'Still with the dealer'), (2, 'Only used once since it was purchased new'),
    )

    WHEELS = (
        (1, '2 wheels'), (2, '3 wheels'), (3, '4 wheels'),
    )

    Manufacturer = (
        (1, 'Bajaj'), (2, 'BMW Motorcycle'),
    )

    ENGINE = (
        (1, 'Less than 250 cc'), (2, '250 - 499 cc'),
    )

    age = models.IntegerField(choices=AGE, blank=False)
    usage = models.IntegerField(choices=USAGE, blank=False)
    body_condition = models.IntegerField(choices=GenericMotorAd.BODY_COND, blank=False)
    mech_condition = models.IntegerField(choices=GenericMotorAd.MECH_COND, blank=False)
    wheels = models.IntegerField(choices=WHEELS, blank=False)
    manufacturer = models.IntegerField(choices=Manufacturer, blank=False)
    engine_size = models.IntegerField(choices=ENGINE, blank=False)

    category_id = models.IntegerField(default=GenericMotorAd.MOTORCYCLES)


class CarAd(GenericMotorAd):
    YEAR = (
        tuple((year, year) for year in xrange(1921, datetime.datetime.now().year + 1, 1))
    )

    TRIM = (
        (1, 'Base'), (2, 'Exclusive'),
    )

    BODY_TYPE = (
        (1, 'SUV'), (2, 'Crossover'),
    )

    DOORS = (
        (2, '2 door'), (3, '3 door'), (4, '4 door'), (5, '5+ doors'),
    )

    CYLINDERS = (
        (3, '3'), (4, '4'), (5, '5'), (6, '6'), (8, '8'), (10, '10'),
        (12, '12'), (13, 'Unknown'),
    )

    COLOR = (
        (1, 'Black'), (2, 'Blue'), (3, 'Brown'),
        (4, 'Burgandy'), (5, 'Gold'), (6, 'Grey'),
        (7, 'Green'), (8, 'Purple'), (9, 'Other Color'),
    )

    TRANSMISSION = (
        (1, 'Manual'), (2, 'Automatic'),
    )

    HORSEPOWER = (
        (1, 'Less than 150 HP'), (2, '150-200 HP'),
    )

    FUEL = (
        (1, 'Gasoline'), (2, 'Hybrid'),
    )

    MAKE = (
        (0, 'Acura'), (1, 'Alpha Romeo'), (2, 'Aston')
    )

    make = models.CharField(max_length=100, blank=False)
    year = models.IntegerField(choices=YEAR, blank=False)
    kilometers = models.PositiveIntegerField(blank=False)
    color = models.IntegerField(choices=COLOR, blank=False)
    doors = models.IntegerField(choices=DOORS, blank=False)
    body_condition = models.IntegerField(choices=GenericMotorAd.BODY_COND, blank=False)
    mech_condition = models.IntegerField(choices=GenericMotorAd.MECH_COND, blank=False)
    trim = models.IntegerField(choices=TRIM, blank=False)
    body_type = models.IntegerField(choices=BODY_TYPE, blank=False)
    cylinders = models.IntegerField(choices=CYLINDERS, blank=False)
    transmission = models.IntegerField(choices=TRANSMISSION, blank=False)
    horse_power = models.IntegerField(choices=HORSEPOWER, blank=False)
    fuel = models.IntegerField(choices=FUEL, blank=False)

    #  Extras go here
    air_conditioning = models.BooleanField(default=False)
    body_kit = models.BooleanField(default=False)

    category_id = models.IntegerField(default=GenericMotorAd.USED_CARS)






