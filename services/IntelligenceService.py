from google.cloud import videointelligence


class IntelligenceService:
    def __init__(self, language="en-US"):
        self.client = videointelligence.VideoIntelligenceServiceClient()
        self.features = [videointelligence.enums.Feature.SPEECH_TRANSCRIPTION]
        self.config = videointelligence.types.SpeechTranscriptionConfig(
            language_code=language,
            enable_automatic_punctuation=True
        )
        self.context = videointelligence.types.VideoContext(
            speech_transcription_config=self.config
        )

    def transcript(self, video, timeout=600):
        operation = self.client.annotate_video(
            video,
            features=self.features,
            video_context=self.context
        )

        result = operation.result(timeout=timeout)
        annotation_results = result.annotation_results[0]
        speech_transcriptions = annotation_results.speech_transcriptions

        return speech_transcriptions
