from pact import Consumer, Provider
import requests
import atexit

pact = Consumer('OrderConsumer').has_pact_with(
    Provider('OrderProvider'),
    port=1234
)

pact.start_service()
atexit.register(pact.stop_service)

def test_get_orders():
    expected = {
        "id": 101,
        "item": "Wireless Mouse",
        "price": 29.99
    }

    (pact
     .given('orders exist')
     .upon_receiving('a request for orders')
     .with_request('get', '/orders')
     .will_respond_with(200, body=expected))

    with pact:
        result = requests.get('http://localhost:1234/orders')
        assert result.json() == expected