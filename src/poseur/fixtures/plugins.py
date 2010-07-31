import nose
from nose.plugins import Plugin
from poseur.fixtures import load_fixtures


def get_test_case_class(nose_test):
    """
    Extracts the class from the nose tests that depends on whether it's a
    method test case or a function test case.
    """
    if isinstance(nose_test.test, nose.case.MethodTestCase):
        return nose_test.test.test.im_class
    else:
        return nose_test.test.__class__


class PoseurFixturesPlugin(Plugin):
    """
    Loads fixtures defined in the attribute `poseur_fixtures`. 
    Does not tear them down automatically.
    """
    activation_parameter = "--with-poseur-fixtures"
    name = "poseur-fixtures"

    def startTest(self, test):
        """
        When preparing the database, check for the `poseur_fixtures`
        attribute and load those.
        """
        test_case = get_test_case_class(test)
        fixtures = getattr(test_case, "poseur_fixtures", [])
        for fixture in fixtures:
            load_fixtures(fixture)
