Template access to faker
========================

You can load faker as a Django template tag library.  Just add ``poseur`` to your ``INSTALLED_APPS``.  You'll then be able to load the entire faker API into a context variable.

::

    {% load faker_tags %}
    {% get_faker %}
    <p>Phone number: {{ faker.phone_number.phone_number }}<br />
       Zip code: {{ faker.address.zip_code }}
    </p>

