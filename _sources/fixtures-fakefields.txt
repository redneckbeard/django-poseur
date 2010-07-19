Creating your own ``FakeField``\ s
==================================

If you have a custom field that you don't want to use the behavior of ``get_internal_type``, you can easily write a ``FakeField`` subclass to do the job.  Here's an example::

    import faker
    from poseur.fixtures import FakeField

    class FakeUSPhoneField(FakeField):
        def get_random_value(self, lower=None, upper=None):
            return faker.utils.numerify("###-###-####")

As you can see, there are only two steps:

1. Subclass ``FakeField``;
2. Override the instance method ``get_random_value``.  Not doing so will result in an ``NotImplementedError`` being raised.

.. method:: get_random_value(self, lower=None, upper=None)

    Should return a random value that validates for this field type.  The parameters ``lower`` and ``upper`` only apply to field types where a range can sensibly be implemented (numeric types, date-based types, possibly a field that pulls from a finite list of words in alphabetically order, etc.).  If these don't make sense for your field, it's safe to ignore them.


