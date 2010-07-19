import random
from datetime import date, datetime, timedelta, time
from decimal import Decimal

from django.template.defaultfilters import slugify

from faker.generators import lorem, internet

class FakeField(object):
    def __init__(self, field_instance, override=False):
        self.field_instance = field_instance
        self.override = override

    def get_value(self):
        if self.override:
            return self.get_override_value()
        elif self.field_instance.choices:
            return random.choice(self.field_instance.choices)[0]
        return self.get_random_value()

    def get_override_value(self):
        val = self.override
        if callable(val):
            return val()
        if type(val) == list:
            return random.choice(val)
        if type(val) == tuple:
            return self.get_random_value(*val)
        return val

    def get_random_value(self, lower=None, upper=None):
        raise NotImplementedError 


class ForeignKey(FakeField):
    def __init__(self, field_instance, override=False):
        super(ForeignKey, self).__init__(field_instance, override)
        self.related_model = self.field_instance.rel.to

    def _get_random_instance(self, queryset):
        count = queryset.count()
        if count == 0:
            if self.field_instance.null:
                return None
            raise self.related_model.DoesNotExist
        if count == 1:
            return queryset[0]
        return queryset[random.randint(0, count-1)]

    def get_override_value(self):
        val = self.override
        if type(val) == dict:
            queryset = self.related_model.objects.filter(**val)
            return self._get_random_instance(queryset)
        raise ValueError('Only dictionaries can be used for ForeignKey fields')
    
    def get_random_value(self, lower=None, upper=None):
        return self._get_random_instance(self.related_model.objects.all())


class BooleanField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        return random.choice([True, False])


class CharField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        words = lorem.sentence()
        return words[:self.field_instance.max_length]


class CommaSeparatedIntegerField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        numbers = ''
        while 1:
            next_int = ',%d' % random.randint(-200, 200)
            if len(numbers + next_int) > self.field_instance.max_length:
                break
            numbers += next_int
        return numbers


class DateField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        f = self.field_instance
        default = getattr(f, 'default', None)
        if getattr(f, 'auto_now', None) or getattr(f, 'auto_now_add', None): 
            return None
        if lower and upper:
            dt = upper - lower
            low, high = 0, dt.days
        else:
            low, high = -365, 365
            lower = date.today()
        return lower + timedelta(days=random.randint(low, high))


class DateTimeField(DateField):
    def get_random_value(self, lower=None, upper=None):
        f = self.field_instance
        default = getattr(f, 'default', None)
        if getattr(f, 'auto_now', None) or getattr(f, 'auto_now_add', None): 
            return None
        if lower and upper:
            dt = upper - lower
            low, high = 0, dt.days
        else:
            low, high = -365, 365
            lower = datetime.now()
        return lower + timedelta(days=random.randint(low, high))


class DecimalField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        if lower and upper:
            lower_int, lower_frac = [int(s) for s in str(lower).split('.')]
            upper_int, upper_frac = [int(s) for s in str(upper).split('.')]
        else:
            max_digits = self.field_instance.max_digits
            decimal_places = self.field_instance.decimal_places
            lower_frac = 0
            upper_frac = 10 * (decimal_places + 1) - 1
            lower_int = 0
            upper_int = 10 * (max_digits - decimal_places + 1) - 1
        return Decimal('%d.%d' % (
            random.randint(lower_int, upper_int), random.randint(lower_frac, upper_frac)
        ))


class EmailField(CharField):
    def get_random_value(self, lower=None, upper=None):
        return internet.email()


class FloatField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        if lower is None:
            lower = -1000
        if upper is None:
            upper = 1000
        return random.uniform(lower, upper)


class IntegerField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        if lower is None:
            lower = -1000
        if upper is None:
            upper = 1000
        return random.randint(lower, upper)


class BigIntegerField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        if not (lower and upper):
            lower, upper = -10000000000, 10000000000
        return random.randint(lower, upper)


class IPAddressField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        return internet.ip_address()


class NullBooleanField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        return random.choice([None, True, False])


class PositiveIntegerField(IntegerField):
    def get_random_value(self, lower=None, upper=None):
        if lower is None or lower < 0:
            lower = 0
        return super(PositiveIntegerField, self).get_random_value(lower, upper)


class PositiveSmallIntegerField(PositiveIntegerField):
    def get_random_value(self, lower=None, upper=None):
        if not upper or upper > 32767:
            upper = 32767 
        return super(PositiveSmallIntegerField, self).get_random_value(lower, upper)


class SlugField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        return slugify(lorem.sentence())[:self.field_instance.max_length]


class SmallIntegerField(IntegerField):
    def get_random_value(self, lower=None, upper=None):
        if not upper or upper > 32767:
            upper = 32767 
        if not lower or lower < -32768:
            lower = -32768
        return super(SmallIntegerField, self).get_random_value(lower, upper)


class TextField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        return '\n\n'.join(lorem.paragraphs(random.randint(2, 5)))


class TimeField(FakeField):
    def get_random_value(self, lower=None, upper=None):
        if lower and upper:
            dt = upper - lower
            return lower + timedelta(seconds=upper)
        return time(*[random.randint(0, n - 1) for n in (24, 60, 60)])
            

class URLField(CharField):
    def get_random_value(self, lower=None, upper=None):
        return 'http://www.' + internet.domain_name()
