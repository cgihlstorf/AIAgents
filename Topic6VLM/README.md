## Task 1

For this exercise, I incorporate LLaVA into a LangGraph framework and ask it about the image `photo.jpg`, which is an image of trees surrounding
a lake on a sunny day, with mountains in the background. The conversation with the model can be found in the file `photo_convo.txt `. The model
does a good job describing and discussing the image. Code to run the model can be found in `run_vlm.py` and the LangGraph checkpoints can be 
found in `checkpoints.db`. An image of the LangGraph graph can be found in `lg_graph.png`. 


## Task 2

For this task, I record two simple videos of a stick figure crossing the screen, one with some sun and cloud shapes in the background (which I call the "nature background") and once with nothing in the background. I varied the background in each video to determine whether this would have an impact on model performance. Each video is approximately 2 minutes long. I then break the videos down into image frames and, for each image, I ask the LLaVA model if there is a person in the scene. I then go through the model responses for each image to determine whether the model correctly identified when a person was in the image.

### Table of Contents

- `frames_blank_background` contains image frames for the video with the blank background.
- `frames_nature_background` contains image frames for the video with the sun and cloud shapes in the background.
- `checkpoints.db` holds the LangGraph checkpoints for the code used to run the model
- `get_video_frames.py` contains code to transform a video into individual image frames
- `lg_graph.png` contains an image of the graph used to run the chat interface with the LLaVA model
- `llava_responses_blank_background.txt` contains the model responses for each image in the video with the blank background
- `llava_responses_nature_background.txt` contains the model responses for each image in the video with the nature background
- `person_frame_video.mp4` is the video with the nature background
- `run_vllm_video.py` is the code I use to run the LLaVA model
- `video_frame_blank.mp4` is the video with the blank background


### Results

- Frames that include a person (blank background): frame 43, frame 44
- Frames that LLaVA states include a person (blank background): frame 33
- Frames that include a person (nature background): frame 29, frame 30
- Frames that LLaVA states include a person (nature background): frame 5, frame 55

For both videos, the model fails to detect the person at the right time. Interestingly, the model states at least once for each video that there is a person in images where there is in fact no person. For the images that contain a person, the model fails to recognize the person. This is likely due to the cartoon-ish style of the scenes, where the model might not be able to distnguish a stick figure of a person because it was trained on real videos with real people.






