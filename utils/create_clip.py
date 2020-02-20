from moviepy.video.io.VideoFileClip import VideoFileClip


def create_clip(destination: str, original_video: VideoFileClip, start: float, end: float, video_format="mp4"):
    try:
        clip = original_video.subclip(start, end)

        clip.set_duration(end - start)
        clip.write_videofile(
            "{}.{}".format(destination, video_format),
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            verbose=False,
            logger=None
        )

        return clip
    except IndexError:
        print("!! Error creating clip for {}".format(destination))
