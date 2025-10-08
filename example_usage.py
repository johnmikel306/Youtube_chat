import os
from src.app import YouTubeQA

def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Set GROQ_API_KEY environment variable")
        return

    qa = YouTubeQA(api_key)

    video_url = input("YouTube URL: ")
    print("Loading video...")

    if not qa.load_video(video_url):
        print("Failed to load video")
        return

    print("Video loaded! Ask questions (type 'quit' to exit):\n")

    while True:
        question = input("Q: ")
        if question.lower() == 'quit':
            break

        try:
            answer = qa.ask(question)
            print(f"A: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()

