import json
from sys import argv
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips

from services.StorageService import StorageService
from services.IntelligenceService import IntelligenceService
from utils.create_clip import create_clip

# Load config
with open("config.json") as data:
    json_data = json.load(data)
    storage_bucket = json_data["storage_bucket"]

# We don't care about the name of the file.
args = argv
args.remove(args[0])

# Setup instances of the services.
Storage = StorageService(storage_bucket)
Intelligence = IntelligenceService()

if len(args) == 3:
    source = args[0]
    destination = args[1]
    sentence = args[2].split(" ")

    print("Attempting to create file at \"{}\" based on \"{}\" with sentence \"{}\"...".format(
        destination,
        source,
        sentence
    ))

    uploaded_file = Storage.upload(source, source)
    transcriptions = Intelligence.transcript(uploaded_file)
    original_video = VideoFileClip(source)

    clips = []
    words_found = []

    for transcription in transcriptions:
        for alternative in transcription.alternatives:
            words = alternative.words
            transcript = alternative.transcript
            confidence = alternative.confidence

            print("{}% confidence that transcript is \"{}\".".format(
                round(confidence * 100, 3),
                transcript
            ))

            for word in words:
                start = word.start_time
                end = word.end_time

                words_found.append({
                    "word": word.word,
                    "start": start.seconds + start.nanos * 1e-9,
                    "end": end.seconds + end.nanos * 1e-9
                })

    for word in words_found:
        the_word = word["word"]
        start = float(word["start"])
        end = float(word["end"])

        destination = "temp/{}".format(the_word)

        clip = create_clip(destination, original_video, start, end)

        clips.append({
            "word": the_word,
            "clip": clip
        })

        print("Done!")
else:
    print("You must supply a source, destination and sentence.")
    print("Example: python3 speech-control my-video.mp4 final.mp4 \"Hello World\"")
