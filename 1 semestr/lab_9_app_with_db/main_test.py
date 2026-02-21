import unittest
from tests.test_get_currencies import TestGetCurrencies, TestIOStreamWrite, TestLogWrite
from tests.test_models import TestAuthor, TestApp, TestUser, TestCurrency, TestSubscriptions
from tests.test_controllers import TestUserController, TestCurrencyController
from tests.test_page_render import TestPageRender

if __name__ == '__main__':
    unittest.main()