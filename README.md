# Video Mashup

A simple Python CLI tool for re-editing videos based on a given phrase. It uses Google's Video Intelligence API to determine the words in a video.

## Dependencies
- [Google Cloud Vision Intelligence](https://pypi.org/project/google-cloud-videointelligence/)
- [Google Cloud Storage](https://pypi.org/project/google-cloud-storage/)
- [MoviePy](https://pypi.org/project/moviepy/)

## Setup
1. Clone this repository and navigate into it
2. Install the dependencies
3. Create a GCP project and enable:
    - Video Intelligence API
    - Cloud Storage
4. Create a service account on GCP that has access to these services
5. Run `export GOOGLE_APPLICATION_CREDENTIALS=path/to/service/account.json`

## Usage

`python3 video-mashup <source> <destination> <sentence>`

### Arguments
- `source` - The path to the video you want to mash up
- `destination` - The path where the mashed up video will be saved
- `sentence` - The sentence that should be said in the mash up (wrap it in quotes)

### Example

Running `python3 video-mashup ./my-video.mp4 ./final.mp4 "hello friends"` will:
- Using the video located at `./my-video.mp4`
- And the sentence `"hello friends"`
- Will create a video saved at `./final.mp4`