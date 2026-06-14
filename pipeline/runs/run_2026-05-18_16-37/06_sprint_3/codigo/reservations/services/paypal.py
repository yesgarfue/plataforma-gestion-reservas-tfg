import requests
from django.conf import settings
from decimal import Decimal

class PayPalService:
    """Servicio para integración con PayPal Sandbox"""
    
    def __init__(self):
        self.sandbox_mode = settings.PAYPAL_SANDBOX_MODE
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.base_url = 'https://api.sandbox.paypal.com' if self.sandbox_mode else 'https://api.paypal.com'
    
    def get_access_token(self):
        """Obtiene un token de acceso de PayPal"""
        url = f'{self.base_url}/v1/oauth2/token'
        auth = (self.client_id, self.client_secret)
        headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
        data = {'grant_type': 'client_credentials'}
        
        try:
            response = requests.post(url, auth=auth, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.RequestException as e:
            raise Exception(f'Error al obtener token de PayPal: {str(e)}')
    
    def create_payment(self, reserva_id, importe, return_url, cancel_url):
        """Crea un pago en PayPal"""
        access_token = self.get_access_token()
        url = f'{self.base_url}/v1/payments/payment'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        payload = {
            'intent': 'sale',
            'payer': {'payment_method': 'paypal'},
            'transactions': [
                {
                    'amount': {
                        'total': str(importe),
                        'currency': 'EUR',
                        'details': {'subtotal': str(importe)}
                    },
                    'description': f'Reserva #{reserva_id}'
                }
            ],
            'redirect_urls': {
                'return_url': return_url,
                'cancel_url': cancel_url
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f'Error al crear pago en PayPal: {str(e)}')
    
    def execute_payment(self, payment_id, payer_id):
        """Ejecuta un pago en PayPal"""
        access_token = self.get_access_token()
        url = f'{self.base_url}/v1/payments/payment/{payment_id}/execute'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        payload = {'payer_id': payer_id}
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f'Error al ejecutar pago en PayPal: {str(e)}')
