#!/usr/bin/env python3

import json
from chemdataextractor import Document, model


def worker(file, attr=['Compound']):
    output = file.split('.')[0] + '.json'
    doc = Document.from_file(file)
    doc.models = [model.__dict__[i] for i in attr]

    with open(output, 'a+') as f:
        f.write(json.dumps(doc.records.serialize()))
