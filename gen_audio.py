import time
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import glob
import csv
import sys

from_basedir = 'data'
datasets = ['snips']
#datasets = ['atis', 'fb_top', 'snips']
to_audio_dir = 'audio'

transcribe = boto3.client('transcribe', region_name='us-east-1')
polly = boto3.client('polly', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        return False

    return True


def get_audio(utterance, folder, filename, voice_id='Joanna'):
    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    #session = boto3.Session(profile_name="adminuser")
    #polly = session.client("polly")
    n_retries = 0
    max_retries = 5

    while n_retries < max_retries:
        try:
            # Request speech synthesis
            response = polly.synthesize_speech(Text=utterance, OutputFormat="mp3", VoiceId=voice_id, Engine='neural')

            # Access the audio stream from the response
            if "AudioStream" in response:
                # Note: Closing the stream is important because the service throttles on the
                # number of parallel connections. Here we are using contextlib.closing to
                # ensure the close method of the stream object will be called automatically
                # at the end of the with statement's scope.
                with open('{}/{}.lab'.format(folder, filename), "w") as fw:
                    fw.write(utterance)

                with closing(response["AudioStream"]) as stream:
                    output = '{}/{}.mp3'.format(folder, filename)

                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())

                    '''
                    if not upload_file(output, 'shangwel', object_name=None):
                        print("Could not upload audio to s3")
                        n_retries += 1
                        continue
                    '''

                    return True
            else:
                # The response didn't contain audio data, retry or exit gracefully
                print("Could not stream audio")
                print('voice_id=', voice_id)
                print(response)
                n_retries += 1
        except (IOError, BotoCoreError, ClientError) as error:
            # The service returned an error, retry or exit gracefully
            # Could not write to file, retry or exit gracefully
            print(error)
            print('voice_id=', voice_id)
            n_retries += 1

    return False

'''
n_processed_utterance = 0
n_skipped_utterance = 0
n_failed_utterance = 0

voice_ids = [
    'Brian', 'Aditi', 'Raveena', 'Ivy', 'Kendra', 'Kimberly',
    'Salli', 'Joey', 'Justin', 'Kevin', 'Matthew', 'Geraint', 'Nicole', 'Russell'
]
# 'Amy', 'Emma'

voice_ids = [
    'Brian', 'Raveena', 'Ivy', 'Kendra', 'Kimberly',
    'Salli', 'Joey', 'Justin', 'Kevin', 'Matthew', 'Amy', 'Emma'
]

for voice_id in voice_ids:
    print(voice_id)
    n_processed_utterance = 0
    n_skipped_utterance = 0
    n_failed_utterance = 0

    for dataset in datasets:
        for from_folder in glob.glob('{}/{}/fewshot_splits/*'.format(from_basedir, dataset)):
            split = os.path.basename(from_folder)
            to_folder = '{}_{}/{}/{}'.format(to_audio_dir, voice_id, dataset, split)
            os.makedirs(to_folder, exist_ok=True)

            for filename in glob.glob('{}/*'.format(from_folder)):
                with open(filename) as csvfile:
                    csvreader = csv.reader(csvfile, delimiter='\t')
                    header = None
                    for row in csvreader:
                        if not header:
                            header = row
                            utterance_idx = header.index('utterance')
                            uid_idx = header.index('u_id')
                        else:
                            if os.path.exists('{}/{}.mp3'.format(to_folder, row[uid_idx])):
                                n_skipped_utterance += 1
                                continue

                            success = get_audio(row[utterance_idx], to_folder, row[uid_idx], voice_id)
                            n_processed_utterance += 1
                            if not success:
                                print('failed utternace: ' + row[utterance_idx])
                                n_failed_utterance += 1


                        if n_processed_utterance and n_processed_utterance % 100 == 0:
                            print('n_processed_utterance: {}, n_failed_utterance: {}, n_skipped_utterance: {}'.format(
                                n_processed_utterance, n_failed_utterance, n_skipped_utterance))
'''

'''
transcribe = boto3.client('transcribe', region_name='us-east-1')
job_name = "test123fuck"
job_uri = "https://shangwel.s3.amazonaws.com/asr_test/hello.mp3"

transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='mp3',
    LanguageCode='en-US'
)

while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break

    print("Not ready yet...")
    time.sleep(5)

print(status)
'''
