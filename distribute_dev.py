import os
import csv
import sys
import tqdm
import shutil
r = list(csv.reader(open("meta-dev.csv")))

for i in tqdm.tqdm(r[1:]):
    if not os.path.exists("speakers_dev_audios/"+i[1]):
        os.makedirs("speakers_dev_audios/"+i[1])
    if os.path.exists("speakers_dev_audios/"+i[1]+"/"+i[0]+".mp3"):
        continue
    try:
        shutil.copy("dev_audios/"+i[0]+".mp3", "speakers_dev_audios/"+i[1]+"/"+i[0]+".mp3")
        shutil.copy("dev_audios/"+i[0]+".lab", "speakers_dev_audios/"+i[1]+"/"+i[0]+".lab")
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print("Fail:", i)
        #print(os.popen("ffmpeg -y -i dev_audios/"+i[0]+".mp3 wav_dev_audios/"+i[0]+".mp3").read())
        #shutil.copy("dev_audios/"+i[0]+".lab", "speakers_dev_audios/"+i[1]+"/"+i[0]+".lab")
        #shutil.copy("dev_audios/"+i[0]+".lab", "wav_dev_audios/"+i[0]+".lab")
        #print("Success!")
