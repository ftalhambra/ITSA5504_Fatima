"""
data_formats.py
Creates a sample customer record in JSON, YAML, and XML.
Prints all three and writes: customer.json, customer.yaml, customer.xml
"""

import json
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

try:
    import yaml  # pip install pyyaml
except ImportError:
    yaml = None
    print("[WARN] PyYAML is not installed. YAML output will be skipped. Install with: pip install pyyaml")


def dict_to_xml(root_tag: str, data: dict) -> Element:
    """Convert a (possibly nested) dict/list to an XML Element."""
    root = Element(root_tag)

    def _attach(elem, key, value):
        if isinstance(value, dict):
            child = SubElement(elem, key)
            for k, v in value.items():
                _attach(child, k, v)
        elif isinstance(value, list):
            container = SubElement(elem, key)
            for item in value:
                item_tag = "address" if key == "addresses" else "item"
                child = SubElement(container, item_tag)
                if isinstance(item, dict):
                    for k, v in item.items():
                        _attach(child, k, v)
                else:
                    child.text = "" if item is None else str(item)
        else:
            child = SubElement(elem, key)
            child.text = "" if value is None else str(value)

    for k, v in data.items():
        _attach(root, k, v)
    return root


def main():
    customer = {
        "customer_id": "CUST-1001",
        "first_name": "Amina",
        "last_name": "Rahman",
        "email": "amina.rahman@example.com",
        "phone": "+1-416-555-0197",
        "addresses": [
            {
                "type": "home",
                "line1": "123 Bloor St W",
                "city": "Toronto",
                "province": "ON",
                "postal_code": "M5S 1W7",
                "country": "CA",
            }
        ],
        "preferences": {"marketing_opt_in": True},
        "updated_at": "2026-02-10T15:23:11Z",
    }

    # JSON
    with open("customer.json", "w", encoding="utf-8") as f:
        json.dump(customer, f, indent=2, ensure_ascii=False)
    print("=== JSON ===")
    print(json.dumps(customer, indent=2, ensure_ascii=False))

    # YAML
    if yaml:
        with open("customer.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(customer, f, sort_keys=False, allow_unicode=True)
        print("\n=== YAML ===")
        print(yaml.safe_dump(customer, sort_keys=False, allow_unicode=True))
    else:
        print("\n[INFO] Skipping YAML output (PyYAML not installed).")

    # XML
    root = dict_to_xml("customer", customer)
    ElementTree(root).write("customer.xml", encoding="utf-8", xml_declaration=True)
    print("\n=== XML ===")
    print(tostring(root, encoding="unicode"))


if __name__ == "__main__":
    main()