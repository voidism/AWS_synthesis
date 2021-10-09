for f in $1/*.mp3
do
	name="$(basename $f .mp3)"
	ffmpeg -i $f wav_$1/$name.wav > /dev/null 2>&1
	cp $1/$name.lab wav_$1/$name.lab
done
