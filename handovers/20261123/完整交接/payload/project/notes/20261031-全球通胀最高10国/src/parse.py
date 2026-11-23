import json
def load(i):
    d=json.load(open(f'weo_{i}.json'));s=d['data']['structures'][0]
    cs=[v['id'] for v in s['dimensions']['series'][0]['values']]
    tp=[v['value'] for v in s['dimensions']['observation'][0]['values']]
    out={}
    for k,ser in d['data']['dataSets'][0]['series'].items():
        c=cs[int(k.split(':')[0])]
        out[c]={tp[int(o)]:(float(v[0]) if v[0] not in (None,'') else None) for o,v in ser.get('observations',{}).items()}
    return out,s
