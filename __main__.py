import json
from sys import argv
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips

from services.StorageService import StorageService
from services.IntelligenceService import IntelligenceService
from utils.create_clip import create_clip
from helpers.strip_punctuation import strip_punctuation

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

    try:
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
            the_word = str(word["word"]).lower()
            start = float(word["start"])
            end = float(word["end"])

            the_word = strip_punctuation(the_word)
            clip_destination = "temp/{}".format(the_word)

            clip = create_clip(clip_destination, original_video, start, end)

            clips.append({
                "word": the_word,
                "clip": clip
            })
    except IndexError:
        # This try/except block is only here so that all the videos are generated
        # before we try to concatenate them. I can't think of a better way to deal
        # with this right now.

        print("Index Error!")

    required_videos = []

    for given_word in sentence:
        for clip in clips:
            print("{} {}".format(given_word, clip["word"]))
            if clip["word"] == given_word:
                required_videos.append(clip["clip"])

    final_video = concatenate_videoclips(required_videos)

    final_video.write_videofile(
        destination,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True
    )

    # Clear out the temp directory
    print("Done!")
else:
    print("You must supply a source, destination and sentence.")
    print("Example: python3 speech-control my-video.mp4 final.mp4 \"Hello World\"")
