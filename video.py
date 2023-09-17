import streamlit as st
import os
from moviepy.editor import VideoFileClip
import whisper

def main():
    st.title("Video Audio Extraction App")

    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
    model = whisper.load_model("small")

    if uploaded_file is not None:
        # Display the video
        st.video(uploaded_file)

        # Extract audio from the uploaded video
        audio_file = extract_audio(uploaded_file)

        if audio_file:
            st.success(f"Audio extracted successfully! You can download the MP3 file below.")
            st.audio(audio_file, format="audio/mp3")
            result = model.transcribe(audio_file, language="en")
            st.write(result["text"])

def extract_audio(uploaded_file):
    try:
        video_file_path = save_uploaded_file(uploaded_file)
        audio_file_path = video_file_path.replace('temp', 'audio')
        audio_file_path = audio_file_path.replace('.mp4', '.mp3')

        # Using MoviePy to extract audio
        video_clip = VideoFileClip(video_file_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_file_path)

        return audio_file_path

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def save_uploaded_file(uploaded_file):
    # Create a temporary directory to store uploaded files
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    return file_path

if __name__ == "__main__":
    main()
