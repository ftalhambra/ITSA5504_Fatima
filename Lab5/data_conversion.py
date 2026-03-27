"""
data_conversion.py
Reads customer.xml → converts to JSON (customer_from_xml.json)
Reads customer.json → converts to YAML (customer_from_json.yaml)
Prints the converted outputs for screenshots.
"""

import json
from xml.etree.ElementTree import fromstring

try:
    import yaml
except ImportError:
    yaml = None
    print("[WARN] PyYAML is not installed. JSON→YAML conversion will be skipped. Install with: pip install pyyaml")


def xml_to_dict(elem):
    children = list(elem)
    if not children:
        return elem.text

    tags = [c.tag for c in children]
    if len(set(tags)) == 1:
        return [xml_to_dict(c) for c in children]

    out = {}
    for c in children:
        val = xml_to_dict(c)
        if c.tag in out:
            if not isinstance(out[c.tag], list):
                out[c.tag] = [out[c.tag]]
            out[c.tag].append(val)
        else:
            out[c.tag] = val
    return out


def main():
    # XML → JSON
    with open("customer.xml", "r", encoding="utf-8") as f:
        xml_text = f.read()
    root = fromstring(xml_text)
    py_from_xml = xml_to_dict(root)

    with open("customer_from_xml.json", "w", encoding="utf-8") as f:
        json.dump(py_from_xml, f, indent=2, ensure_ascii=False)
    print("=== XML → JSON (from customer.xml) ===")
    print(json.dumps(py_from_xml, indent=2, ensure_ascii=False))

    # JSON → YAML
    with open("customer.json", "r", encoding="utf-8") as f:
        customer_json = json.load(f)

    if yaml:
        yaml_text = yaml.safe_dump(customer_json, sort_keys=False, allow_unicode=True)
        with open("customer_from_json.yaml", "w", encoding="utf-8") as f:
            f.write(yaml_text)
        print("\n=== JSON → YAML (from customer.json) ===")
        print(yaml_text)
    else:
        print("\n[INFO] Skipping JSON → YAML conversion (PyYAML not installed).")


if __name__ == "__main__":
    main()