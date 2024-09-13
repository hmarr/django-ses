from django.test import TestCase

from django_ses import models, settings, signals
from tests.mocks import get_mock_bounce, get_mock_complaint


class SignalsTestCase(TestCase):
    """
    Test the signals handlers.
    """
    def test_bounce_handler(self):
        count = models.BlacklistedEmail.objects.all().count()
        self.assertEqual(count, 0)

        mail_obj, bounce_obj, notification = get_mock_bounce("eventType")

        # It shouldn't insert the email in the blacklist if the feature hasn't
        # been enabled
        signals.bounce_handler(None, mail_obj, bounce_obj, notification)
        count = models.BlacklistedEmail.objects.all().count()
        self.assertEqual(count, 0)

        # ... but after enabling the feature...
        settings.AWS_SES_ENABLE_BOUNCE_BLACKLIST = True

        # ... it should inser the email in the blacklist
        signals.bounce_handler(None, mail_obj, bounce_obj, notification)
        count = models.BlacklistedEmail.objects.all().count()
        self.assertEqual(count, 1)

    def test_complaint_handler(self):
        count = models.BlacklistedEmail.objects.all().count()
        self.assertEqual(count, 0)

        mail_obj, complaint_obj, notification = get_mock_complaint("eventType")

        # It shouldn't insert the email in the blacklist if the feature hasn't
        # been enabled
        signals.complaint_handler(None, mail_obj, complaint_obj, notification)
        count = models.BlacklistedEmail.objects.all().count()
        self.assertEqual(count, 0)

        # ... but after enabling the feature...
        settings.AWS_SES_ENABLE_COMPLAINT_BLACKLIST = True

        # ... it should inser the email in the blacklist
        signals.complaint_handler(None, mail_obj, complaint_obj, notification)
        count = models.BlacklistedEmail.objects.all().count()
        self.assertEqual(count, 1)
