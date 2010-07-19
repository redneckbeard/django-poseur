Generating fixtures
===================

Getting started
---------------

Assume that we have a model that looks something like this::

    class Person(models.Model):
        first_name = models.CharField(max_length=20)
        last_name = models.CharField(max_length=20)
        weight = models.DecimalField(max_digits=5, decimal_places=2)
        birthday = models.DateField()

If you want to use poseur to create a bunch of instances of this model, you create a ``poseur.fixtures.FakeModel`` subclass.

::

    # fixtures.py

    class FakePerson(FakeModel):
        class Meta:
            model = Person
            count = 10

This is the simplest possible case.  The inner ``Meta`` class requires that you define a model and a count (the number of instances that will be generated in one pass).  Everything else is optional.  Poseur will generate random values for all the declared fields for each instance. However, it's possible that we may want to be a bit more specific.

::

    class FakePerson(FakeModel):
        first_name = faker.name.first_name
        last_name = "Johnson"
        weight = ("100.00", "200.00")

        class Meta:
            model = Foo
            count = 10

Let's take a look at what's happening here.

- We are providing a value for ``first_name`` with a callable.  ``faker.name.first_name`` will get called every time an instance is created.  (faker is the underlying library for much of what poseur does, and its functions are particularly useful here.)
- We are supplying a string literal for ``last_name``, which will be used for all instances created.
- We are using a tuple for ``weight``, which indicates to poseur the upper and lower bounds for random value generation.
- We are still leaving the value of ``birthday`` entirely up to poseur.

Now that we have a ``FakeModel`` subclass, we have two options for creating our data:

- Passing the import path to the ``fixtures`` module to ``poseur.fixtures.load_fixtures``.

  ::

      >>> from poseur.fixtures import load_fixtures
      >>> load_fixtures('myapp.fixtures')
      10 instances of `Foo' generated.

- Calling ``generate`` on a ``FakeModel`` subclass.  Generate takes one argument, ``count``.
  
  ::

        >>> FakePerson.generate(count=5)
        5 instances of `Foo' generated.

You can use these methods in a ``setUp`` method for your test suite, or you can just run them or dump the data to JSON.
