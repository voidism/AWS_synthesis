import json

_abbre = json.load(open("abbrevs.json", 'r'))

def awesome_tokenize(paragraph):
    sents = [(x+'.') for x in paragraph.split('. ')]
    sents[-1] = sents[-1][:-1]
    merged_sents = []
    merge_next = False
    for i in range(len(sents)):
        if sents[i] in ['.', '']:
            merge_next = False
            continue
        if merge_next:
            merged_sents[-1] += ' ' + sents[i]
        else:
            merged_sents.append(sents[i])
        merge_next = False
        for a in _abbre.keys():
            if sents[i][-len(a):] == a:
                merge_next = True
    return merged_sents


