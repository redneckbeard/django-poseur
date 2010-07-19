Wish list
=========

Poseur is currently very much alpha software.  It pretty much does all of what I need it to do, but I recognize that's probably not enough for a lot of people.  Here are a few items that have crossed my mind:

- Provide some sort of option in the ``Meta`` class for models with foreign key relationships that will evenly distribute the relations among the available objects (cycling through them rather than randomly selecting them each time)
- Provide a "best-guess" mechanism for dealing with the wealth of fields in ``django.contrib.localflavor``.  I guess this would involve writing something that would parse a regular expression and simplify it down to something that could be fed to ``faker.utils.bothify``.  The caveat here is that it would only work for those fields that are subclasses of ``RegexField``, but if done right it could ease the pain of defining values for a good number of these fields.
