from django.test import TestCase
from django.contrib.auth.models import User
from .models import Sensor, DataPoint
from uuid import UUID
from django.test import Client

def validate_uuid4(uuid_string):
    """
    Source: https://gist.github.com/ShawnMilo/7777304
    Validate that a UUID string is infact a valid uuid4. Luckily, the uuid module
    does the actual checking for us. It is vital that the 'version' kwarg be
    passed to the UUID() call, otherwise any 32-characterhex string is considered valid.
    """

    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        # If ValueError, then the string is not a valid hex code for a UUID.
        return False

    # If the uuid_string is a valid hex code, but an invalid uuid4,
    # the UUID.__init__ will convert it to a valid uuid4.
    # This is bad for validation purposes.
    return val.hex == uuid_string.replace('-','')

class SensorTestCase(TestCase):
    def setUp(self):
        """Generate a test user and log it in"""
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

    def test_new_sensor(self):
        """Make a test sensor and test defaults"""
        self.s1 = Sensor.objects.create(name="TestSensor1", owner=self.user, min_value=0, max_value=10)
        # Check Unit default
        self.assertEqual(self.s1.unit, '°C')
        # Check that valid API key was made
        self.assertTrue(validate_uuid4(str(self.s1.api_key)))
        # Check that min and max and malfunction values are set
        self.assertEqual(self.s1.min_value, 0)
        self.assertEqual(self.s1.max_value, 10)
        self.assertFalse(self.s1.malfunction)
        # Check that no DataPoints have been associated with the sensors
        self.assertEqual(self.s1.data.all().count(), 0)
        # Check the string representation
        self.assertEqual(str(self.s1), "TestSensor1")

class GUITestCase(TestCase):
    def setUp(self):
        """Generate a test user and test client"""
        self.user = User.objects.create_user(username='guitestuser', password='12345', first_name="Test", last_name="User")
        self.c = Client()

    def test_login(self):
        """Test logging in of the test user"""
        response = self.c.post('/accounts/login/', {'username': 'guitestuser', 'password': '12345'}, follow=True)
        # Ensure proper flow
        self.assertEqual(response.redirect_chain, [('/monitor', 302), ('/monitor/', 301)])
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        """Test what the user sees on first login"""
        response = self.c.post('/accounts/login/', {'username': 'guitestuser', 'password': '12345'}, follow=True)
        page = str(response.content)
        # Check for HTML header
        self.assertTrue("<!doctype html>" in page)
        # Check for tagline
        self.assertTrue("Air Quality Monitor" in page)
        # Check for text
        self.assertTrue("You are viewing all of the sensors in the User household" in page)
        # Ensure no sensors linked to this user
        self.assertTrue("No sensors associated with you" in page)

    def test_new_sensor(self):
        """Test adding a sensor via the GUI"""
        response = self.c.post('/accounts/login/', {'username': 'guitestuser', 'password': '12345'}, follow=True)
        response = self.c.post('/monitor/new/', {'name': 'TestSensor2', 'unit': '°F', 'min_value': 0, 'max_value': 100}, follow=True)
        page = str(response.content)
        # Check for HTML header
        self.assertTrue("<!doctype html>" in page)
        # Check for tagline
        self.assertTrue("Air Quality Monitor" in page)
        # Check for title
        self.assertTrue("<h1>TestSensor2</h1>" in page)
        # Ensure no data linked to this sensor
        self.assertTrue("No data associated with this sensor" in page)
        # Check that owner is correctly set
        sensor = Sensor.objects.get(name="TestSensor2")
        self.assertTrue(sensor.owner == self.user)

    def test_new_data(self):
        """Test adding data via the API and having it show in the GUI"""
        # Login, create sensor, and get its attributes
        response = self.c.post('/accounts/login/', {'username': 'guitestuser', 'password': '12345'}, follow=True)
        response = self.c.post('/monitor/new/', {'name': 'TestSensor3', 'unit': 'F', 'min_value': 0, 'max_value': 100}, follow=True)
        sensor = Sensor.objects.get(name="TestSensor3")

        # Call datapoint API and check response code
        response = self.c.get('/monitor/add/'+str(sensor.id), {'api_key': str(sensor.api_key), 'value': '50.55'}, follow=True)
        self.assertEqual(response.status_code, 201)

        # Get sensor detail page
        response = self.c.get('/monitor/view/'+str(sensor.id), follow=True)
        page = str(response.content)
        # Check for HTML header
        self.assertTrue("<!doctype html>" in page)
        # Check for tagline
        self.assertTrue("Air Quality Monitor" in page)
        # Check for title
        self.assertTrue("<h1>TestSensor3</h1>" in page)
        # Ensure data IS linked to this sensor
        self.assertFalse("No data associated with this sensor" in page)
        self.assertTrue("50.55 F" in page)
        # Ensure malfunction warning wasn't tripped
        self.assertFalse("which may indicate a malfunction" in page)

    def test_malfunction(self):
        """Test adding data via the API and tripping the malfunction warning"""
        # Login, create sensor, and get its attributes
        response = self.c.post('/accounts/login/', {'username': 'guitestuser', 'password': '12345'}, follow=True)
        response = self.c.post('/monitor/new/', {'name': 'TestSensor4', 'unit': 'F', 'min_value': 0, 'max_value': 100}, follow=True)
        sensor = Sensor.objects.get(name="TestSensor4")

        # Call datapoint API with too-high value and check response code
        response = self.c.get('/monitor/add/'+str(sensor.id), {'api_key': str(sensor.api_key), 'value': '120.66'}, follow=True)
        self.assertEqual(response.status_code, 201)

        # Get sensor detail page
        response = self.c.get('/monitor/view/'+str(sensor.id), follow=True)
        page = str(response.content)
        # Check for HTML header
        self.assertTrue("<!doctype html>" in page)
        # Check for tagline
        self.assertTrue("Air Quality Monitor" in page)
        # Check for title
        self.assertTrue("<h1>TestSensor4</h1>" in page)
        # Ensure data IS linked to this sensor
        self.assertFalse("No data associated with this sensor" in page)
        self.assertTrue("120.66 F" in page)
        # Ensure malfunction warning WAS tripped
        self.assertTrue("which may indicate a malfunction" in page)

    def test_del_sensor(self):
        """Test deletion of a sensor"""
        # Login, create sensor, and get its attributes
        response = self.c.post('/accounts/login/', {'username': 'guitestuser', 'password': '12345'}, follow=True)
        response = self.c.post('/monitor/new/', {'name': 'TestSensor5', 'unit': 'F', 'min_value': 0, 'max_value': 100}, follow=True)
        sensor = Sensor.objects.get(name="TestSensor5")

        # Get sensor detail page
        response = self.c.get('/monitor/view/'+str(sensor.id), follow=True)
        page = str(response.content)

        # Check for delete button in detail page
        self.assertTrue('Delete Sensor' in page)
        self.assertTrue('href="/monitor/del/{}/"'.format(sensor.id) in page)

        # Trigger the deletion
        response = self.c.get('/monitor/del/'+str(sensor.id), follow=True)
        page = str(response.content)
        self.assertTrue('<h1>Sensor "TestSensor5" has been deleted</h1>' in page)

        # Test that sensor is gone
        self.assertEqual(Sensor.objects.filter(name="TestSensor5").count(), 0)
