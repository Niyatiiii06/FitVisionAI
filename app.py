from src.video_reader import VideoReader


def main():

    reader = VideoReader("data/videos/squat.mp4")

    frame = reader.read_frame()

    if frame is not None:
        print("Frame Shape:", frame.shape)

    reader.release()


if __name__ == "__main__":
    main()