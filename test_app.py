from app import app
from unittest import TestCase

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class ConversionTestCase(TestCase):
    # Unit Tests #
        
    def test_index(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)  #testing status code
            self.assertIn('Converting From:',html)  #testing index.html label
    
    def test_not_error(self):
        with app.test_client() as client:
            res = client.post('/convert', data={"input": "USD", "output": "EUR",'amount': "100"})
            html = res.get_data(as_text=True)
            
             #checks if error is not showing on html
            self.assertNotIn("Please Fill In All Boxes", html)
            
    def test_error(self):
        with app.test_client() as client:
            
            res = client.post('/convert', data={"input": "USD", "output": "",'amount': "100"})
            html = res.get_data(as_text=True)
    
             #checks if error is showing on html
            self.assertIn('<h5>', html)