from pact import Consumer, Provider
import requests
import json

def test_get_orders():
    pact = Consumer("OrderConsumer").has_pact_with(
        Provider("OrderProvider"),
        host_name="localhost",
        port=1234
    )

    expected_body = {
        "id": 101,
        "item": "Wireless Mouse",
        "price": 29.99
    }

    (pact
     .given("orders exist")
     .upon_receiving("a request for orders")
     .with_request("get", "/orders")
     .will_respond_with(200, body=expected_body)
    )

    with pact:
        response = requests.get("http://localhost:1234/orders")
        assert response.status_code == 200
        assert response.json() == expected_body

    # ✅ WORKAROUND: Explicitly write pact file (Windows fix)
    pact_data = {
        "consumer": {"name": "OrderConsumer"},
        "provider": {"name": "OrderProvider"},
        "interactions": [
            {
                "description": "a request for orders",
                "request": {
                    "method": "GET",
                    "path": "/orders"
                },
                "response": {
                    "status": 200,
                    "body": expected_body
                }
            }
        ],
        "metadata": {
            "pactSpecification": {
                "version": "2.0.0"
            }
        }
    }

    with open("pacts/OrderConsumer-OrderProvider.json", "w") as f:
        json.dump(pact_data, f, indent=2)


if __name__ == "__main__":
    test_get_orders()