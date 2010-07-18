import inspect

from faker.fixtures import fields


class FakeFieldNotFound(Exception):
    pass


class FakeModelMetaclass(type):
    def __new__(cls, name, bases, dct):
        meta = dct.pop('Meta', None)
        if meta is None:
            return super(FakeModelMetaclass, cls).__new__(cls, name, bases, dct)
        model = meta.model
        fake_fields = {}
        for model_field in model._meta.fields:
            if not model_field.auto_created:
                field_name = model_field.name
                override = dct.pop(field_name, None)
                if inspect.isclass(override) and issubclass(override, fields.FakeField):
                    fake_fields[field_name] = override(model_field)
                    continue
                field_type = model_field.__class__.__name__
                try:
                    fake_field_class = getattr(fields, field_type)
                except AttributeError:
                    field_type = model_field.get_internal_type()
                    try:
                        fake_field_class = getattr(fields, field_type)
                    except AttributeError:
                        raise FakeFieldNotFound(field_type)
                fake_fields[field_name] = fake_field_class(model_field, override)
        new_class = super(FakeModelMetaclass, cls).__new__(cls, name, bases, dct)
        new_class._meta = meta()
        new_class.requires = getattr(meta, 'requires', [])
        new_class.fake_fields = fake_fields
        return new_class


class BaseFakeModel(object):
    @classmethod
    def generate(cls, count=None):
        if count is None:
            count = cls._meta.count
        for i in range(count):
            cls._meta.model.objects.create(**cls._get_kwargs())

    @classmethod
    def _get_kwargs(cls):
        return dict([
            (field_name, field.get_value())
            for field_name, field in cls.fake_fields.items()
        ])


class FakeModel(BaseFakeModel):
    __metaclass__ = FakeModelMetaclass
