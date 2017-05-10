#!/usr/bin/env python3


def main():
    import json
    import re
    import sys
    import yaml

    tr = str.maketrans("qwertyuiop[]asdfghjkl;'zxcvbnm,.`", "йцукенгшщзхъфывапролджэячсмитьбюё")
    replacer = lambda m: m.group().translate(tr)
    new_doc = [ ]

    def process(f):
        doc = re.sub(r"(^|,)\s*//.*", r"\g<1>", f.read(), flags=re.M)
        doc = re.sub(r"/\*[\s\S]*\*/", "", doc)
        doc = yaml.load(doc.expandtabs(4))
        assert isinstance(doc, list)
        for item in doc:
            keys = item.get("keys")
            if keys is not None:
                new_keys = [re.sub(r"\+[a-z]\b|\+[][;',.`]", replacer, key) for key in keys]
                if new_keys != keys:
                    item["keys"] = new_keys
                    new_doc.append(item)

    if len(sys.argv) <= 1:
        process(sys.stdin)
    else:
        for filename in sys.argv[1:]:
            if filename == '-':
                process(sys.stdin)
            else:
                with open(filename, encoding="utf-8-sig") as f:
                    process(f)

    write = sys.stdout.write
    write("[\n")
    for item in new_doc:
        write("    ")
        json.dump(item, sys.stdout, ensure_ascii=False, sort_keys=True, check_circular=False)
        write(",\n")
    write("]\n")


if __name__ == "__main__":
    main()
