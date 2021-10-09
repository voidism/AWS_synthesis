import os
import csv
import sys
import tqdm
import shutil
r = list(csv.reader(open("meta-train.csv")))

for i in tqdm.tqdm(r[1:]):
    if not os.path.exists("speakers_train_audios/"+i[1]):
        os.makedirs("speakers_train_audios/"+i[1])
    if os.path.exists("speakers_train_audios/"+i[1]+"/"+i[0]+".mp3"):
        continue
    try:
        shutil.copy("train_audios/"+i[0]+".mp3", "speakers_train_audios/"+i[1]+"/"+i[0]+".mp3")
        shutil.copy("train_audios/"+i[0]+".lab", "speakers_train_audios/"+i[1]+"/"+i[0]+".lab")
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print("Fail:", i)
        #print(os.popen("ffmpeg -y -i train_audios/"+i[0]+".mp3 wav_train_audios/"+i[0]+".mp3").read())
        #shutil.copy("train_audios/"+i[0]+".lab", "speakers_train_audios/"+i[1]+"/"+i[0]+".lab")
        #shutil.copy("train_audios/"+i[0]+".lab", "wav_train_audios/"+i[0]+".lab")
        #print("Success!")
