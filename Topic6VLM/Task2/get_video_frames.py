import cv2

def get_frames(video_file_path:str):

    cap = cv2.VideoCapture(video_file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps * 2)  # frame interval for ~2 seconds

    frames = []
    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_num % interval == 0:
            frames.append(frame)
        frame_num += 1

    cap.release()

    for i, frame in enumerate(frames):
        cv2.imwrite(f"frames/frame_{i:04d}.jpg", frame)



if __name__ == "__main__":
    video_file_path = "person_frame_video.mp4"
    get_frames(video_file_path)