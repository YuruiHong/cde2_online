#!/usr/bin/env python3

import sys
import json
from chemdataextractor import Document, model

file = sys.argv[1]
output = file.split('.')[0] + '.json'
doc = Document.from_file(file)
doc.models = [model.MeltingPoint]

# print the extracted data to json

with open(output, 'a+') as f:
    f.write(json.dumps(doc.records.serialize()))
