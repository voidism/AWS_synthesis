import json
import re
import sys
import csv
import tqdm
import random
from gen_audio import get_audio
from text.cleaners import english_cleaners
from mutagen.mp3 import MP3

abbre = json.load(open("abbrevs.json", 'r'))

voice_ids = [
    'Olivia', 'Brian', 'Amy', 'Emma', 'Ivy', 'Joanna', 'Kendra', 'Kimberly',
    'Salli', 'Joey', 'Justin', 'Kevin', 'Matthew'
]

jfile = sys.argv[1] if len(sys.argv) > 1 else "train-v1.1.json"
js = json.load(open(jfile))
meta_head = ['id', 'speaker', 'duration', 'text', 'normalized_text']
fw = open('meta-'+jfile+'.csv', 'w')
csvfile = csv.writer(fw)
csvfile.writerow(meta_head)
fw.flush()

def sample_speaker():
    return voice_ids[random.randint(0, len(voice_ids)-1)]

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

charnum = 0

for i in tqdm.trange(len(js['data'])):
    for j in range(len(js['data'][i]['paragraphs'])):
        utterances = js['data'][i]['paragraphs'][j]['context']
        SPK = sample_speaker()
        for k, utterance in enumerate(awesome_tokenize(utterances)):
            ID = "context-%d_%d_%d"%(i, j, k)
            TEXT = utterance
            NOR_TEXT = english_cleaners(TEXT)
            get_audio(NOR_TEXT, 'audios', ID, voice_id=SPK)
            DUR = MP3('{}/{}.mp3'.format('audios', ID)).info.length
            csvfile.writerow([ID,SPK,DUR,TEXT,NOR_TEXT])
            charnum += len(NOR_TEXT)
            fw.flush()
        for q in range(len(js['data'][i]['paragraphs'][j]['qas'])):
            utterance = js['data'][i]['paragraphs'][j]['qas'][q]['question']
            ID = "question-%d_%d_%d"%(i, j, q)
            SPK = sample_speaker()
            TEXT = utterance
            NOR_TEXT = english_cleaners(TEXT)
            get_audio(NOR_TEXT, 'audios', ID, voice_id=SPK)
            DUR = MP3('{}/{}.mp3'.format('audios', ID)).info.length
            csvfile.writerow([ID,SPK,DUR,TEXT,NOR_TEXT])
            charnum += len(NOR_TEXT)
            fw.flush()

print('Total Chars:', charnum)
