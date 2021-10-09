import json
import re
import sys
import csv
import tqdm
import random
from gen_audio import get_audio
from text.cleaners import english_cleaners
from mutagen.mp3 import MP3


jfile = sys.argv[1] if len(sys.argv) > 1 else "train-v1.1.json"

voice_ids = [
    'Brian', 'Raveena', 'Ivy', 'Kendra', 'Kimberly',
    'Salli', 'Joey', 'Justin', 'Kevin', 'Matthew', 'Amy', 'Emma'
]

def sample_speaker():
    return voice_ids[random.randint(0, len(voice_ids)-1)]

js = json.load(open(jfile))
meta_head = ['id', 'speaker', 'duration', 'text', 'normalized_text']
csvfile = csv.writer(open('meta-'+jfile+'.csv', 'w'))
csvfile.writerow(meta_head)

#def write_meta(filename, meta_head, meta_data):
#    csvfile = csv.writer(open(filename, 'w'))
#    csvfile.writerow(meta_head)
#    for meta in meta_data:
#        csvfile.writerow(meta)

text = []

for i in tqdm.trange(len(js['data'])):
    for j in range(len(js['data'][i]['paragraphs'])):
        to_pop = set()
        #print(len(js['data'][i]['paragraphs'][j]['context']))
        para_word += len(js['data'][i]['paragraphs'][j]['context'])
        utterance = js['data'][i]['paragraphs'][j]['context']
        text.append(utterance)
        for q in range(len(js['data'][i]['paragraphs'][j]['qas'])):
            #print(len(js['data'][i]['paragraphs'][j]['qas'][q]['question']))
            q_word += len(js['data'][i]['paragraphs'][j]['qas'][q]['question'])
            utterance = js['data'][i]['paragraphs'][j]['qas'][q]['question']
            text.append(utterance)
gex = re.compile(r'\s([A-Z]\S*\.)\s[a-z]')
gex2 = re.compile(r'\s([A-Z]\.)\s')
#tokenizer = PunktSentenceTokenizer()
'''
abbre = {}
for t in text:
    fs = gex.findall(t)
    fs += gex2.findall(t)
    if len(fs):
        print(t)
        print(fs)
        for f in fs:
            abbre.setdefault(f, 0)
            abbre[f] += 1
print(abbre)
abbre = {}
dev_abbre = {'U.S.': 64, 'Jr.': 3, 'C.': 13, 'L.': 8, 'T.': 9, 'S.': 16, 'F.': 14, 'J.': 13, 'E.': 14, 'Ave.': 2, 'H.': 9, 'M.I.T.': 1, 'G.': 5, 'Y.': 31, 'X.': 1, 'P.': 6, 'R.': 5, 'U.': 4, 'D.C.': 1, 'B.': 15, 'L.A.': 2, 'Open....': 1, 'E.I.': 1, 'D.': 9, 'A.': 8, 'I.': 1, 'V.': 4, 'M.': 7, 'R.F.C.': 1, 'Inc.': 8, 'K.': 4, 'Rouen.': 1, 'Co.': 1, 'S.H.I.E.L.D.': 1, 'M.D.': 1, 'W.': 10, 'O.': 3, 'N.': 1, 'St.': 1, 'a.m.': 1, 'p.m.': 1, 'i.e.': 1, 'e.g.': 1, 'Mr.': 1, 'Mrs.': 1, 'Dr.': 1, 'ft.': 1, 'Ltd.': 1, 'Rev.': 1}
trn_abbre = {'B.S.': 3, 'B.A.': 2, 'B.': 85, 'M.': 111, 'C.S.C.': 2, 'F.': 74, 'U.': 17, 'H.': 84, 'D.': 68, 'J.': 131, 'E.': 76, 'I.': 53, 'P.': 33, 'U.S.': 739, 'W.': 75, 'Jr.': 43, 'Fulfilled...': 1, 'Z.': 4, 'B.I.C.': 1, 'C.': 81, 'K.': 19, 'R.': 74, 'V.': 16, 'S.': 56, 'N.': 22, 'Myriad.': 1, 'Inc.': 24, 'G.': 44, 'D.C.': 24, 'Bronx.': 1, 'L.': 45, 'I.D.': 2, 'Soon...': 1, 'A.P.C.': 1, 'Skt.': 1, 'T.': 36, 'A.': 81, 'U.E.': 1, 'Ph.D.': 4, 'M.Sc.': 2, 'Corp.': 4, 'Ltd.': 2, 'Trump...': 1, 'F.C.': 12, 'R.F.C.': 3, 'Heretic.': 1, 'Helix.': 1, 'Bros.': 14, 'U.N.': 10, 'O.': 16, 'Sr.': 8, 'E.T.': 10, 'H.R.': 1, 'N.S.A.': 1, 'J.C.B.': 1, 'E.g.': 4, 'B.mus.': 2, 'M.mus.': 2, 'Zamoyski.': 1, 'Sudan...': 1, 'Museum.': 1, 'S.p.A.': 1, 'Etc.': 1, 'L.A.': 1, 'U.K.': 6, 'H.P.': 1, 'A.O.': 1, "Binding'.": 1, 'Uhu-Theatre.': 1, 'N.S.': 1, 'Superiori...': 1, 'Hell...': 1, 'CC.OO.': 1, 'C.F.': 2, 'Co.': 9, 'C.S.': 1, 'Orat.': 1, 'Hist.': 1, 'B.C.': 3, 'M.S.': 1, 'N.L.': 2, 'Cardinals.': 1, 'N.Y.': 1, 'EIC.': 1, 'Unknown...': 1, 'Warn.': 1, 'Sch.': 3, 'Polanco.': 1, 'Provo...': 1, 'M.I.A.': 1, 'M.P.': 1, 'Somerset...': 1, 'St.': 2, 'T.K.': 2, 'D.A.T.S.': 1, 'I.T.': 1, 'Canada–U.S.': 1, 'Ave.': 1, 'BCE.': 1, 'C.E.': 2, 'F.E.A.R.': 1, 'Mag.': 1, 'R.E.M.': 1, 'X.': 1, 'Jones...': 1, 'Q.': 9, 'Assoc.': 1, 'J.D.': 3, 'Gov.': 1, 'Dept.': 1, 'Skyth.': 1, 'Canada-U.S.': 1, 'Blvd.': 2, 'Taierzhuang.': 1, 'Viva...': 1, 'Jesus.': 1, 'Braunstein"..': 1, 'Aventine.': 1, 'Tibur.': 1, 'DEC.': 1, 'Govts.': 1}
for k in dev_abbre:
    abbre[k] = dev_abbre[k]
for k in trn_abbre:
    abbre[k] = trn_abbre[k]
abbre.pop('Museum.')
addition = ['St.', "a.m.", "p.m.", "i.e.", "e.g.", "Mr.", "Mrs.", "Dr.", "ft.", "Ltd.", "Rev."]
for a in addition:
    abbre[a] = 1
'''
import json
#json.dump(abbre, open("abbrevs.json", 'w'))
abbre = json.load(open("abbrevs.json", 'r'))
#tokenizer._params.abbrev_types = set(abbre.keys())

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
        for a in abbre.keys():
            if sents[i][-len(a):] == a:
                merge_next = True
    return merged_sents
'''

for t in text:
    if '. ' in t:
        print(awesome_tokenize(t))
        sents = [(x+'.') for x in t.split('. ')]
        sents[-1] = sents[-1][:-1]
        for i in range(len(sents)):
            for a in abbre.keys():
                if sents[i][-len(a):] == a:
                    print('--')
                    print(sents[i])
                    print(sents[i+1] if i != len(sents)-1 else '[end]')

exit(0)
'''
charnum = 0
for i in tqdm.trange(len(js['data'])):
    for j in range(len(js['data'][i]['paragraphs'])):
        #to_pop = set()
        #print(len(js['data'][i]['paragraphs'][j]['context']))
        #para_word += len(js['data'][i]['paragraphs'][j]['context'])
        utterances = js['data'][i]['paragraphs'][j]['context']
        for k, utterance in enumerate(awesome_tokenize(utterances)):
            ID = "context-%d_%d_%d"%(i, j, k)
            SPK = sample_speaker()
            TEXT = utterance
            NOR_TEXT = english_cleaners(TEXT)
            get_audio(NOR_TEXT, 'audios', ID, voice_id=SPK)
            DUR = MP3('{}/{}.mp3'.format('audios', ID)).info.length
            csvfile.writerow([ID,SPK,DUR,TEXT,NOR_TEXT])
            charnum += len(TEXT)
        for q in range(len(js['data'][i]['paragraphs'][j]['qas'])):
            #print(len(js['data'][i]['paragraphs'][j]['qas'][q]['question']))
            utterance = js['data'][i]['paragraphs'][j]['qas'][q]['question']
            ID = "question-%d_%d_%d"%(i, j, q)
            SPK = sample_speaker()
            TEXT = utterance
            NOR_TEXT = english_cleaners(TEXT)
            get_audio(NOR_TEXT, 'audios', ID, voice_id=SPK)
            DUR = MP3('{}/{}.mp3'.format('audios', ID)).info.length
            csvfile.writerow([ID,SPK,DUR,TEXT,NOR_TEXT])
            charnum += len(TEXT)
            #write_meta('meta-'+jfile+'.csv', meta_head, meta_data)
            #exit(0)

#exit(0)
print('Total Chars:', charnum)
#print("para:", para_word, "question:", q_word)
#print('money:', 16.0 * float(para_word) / 1000000.0)
#print('money:', 16.0 * float(q_word) / 1000000.0)
#json.dump(q_dict, open(sys.argv[2], 'w'))
#json.dump(js, open(sys.argv[1]+".excluded", 'w'))
#if len(sys.argv)>3:
#    json.dump(st_dict, open(sys.argv[3], 'w'))


