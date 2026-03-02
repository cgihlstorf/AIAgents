## Task 1

For this exercise, I incorporate LLaVA into a LangGraph framework and ask it about the image `photo.jpg`, which is an image of trees surrounding
a lake on a sunny day, with mountains in the background. The conversation with the model can be found in the file `photo_convo.txt `. The model
does a good job describing and discussing the image. Code to run the model can be found in `run_vlm.py` and the LangGraph checkpoints can be 
found in `checkpoints.db`. An image of the LangGraph graph can be found in `lg_graph.png`. 


## Task 2

For this task, I record two simple videos of a stick figure crossing the screen, once with some sun and cloud shapes in the background and once with nothing in the background. Each video is approzimately 2 minutes long. I then break the videos down into image frames and, for each image, I ask the model if there is a person in the scene. [TODO]

