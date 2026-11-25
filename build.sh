#!/bin/bash
# Rebuild new/index.html from new/template.html + _data/listings.json
cd "$(dirname "$0")" && python3 -I - <<'PY'
import json
L=json.load(open('_data/listings.json')); t=open('new/template.html').read()
t=t.replace('%%LISTINGS%%',json.dumps(L)).replace('%%NREV%%','1,852').replace('%%AVG%%','4.82').replace('%%FIVE%%','90').replace('%%NHOMES%%',str(len(L)))
open('new/index.html','w').write(t)
PY
