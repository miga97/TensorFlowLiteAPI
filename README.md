TensorFlowLiteAPI

API for Image Classification based on https://lobe.ai

use your own model by binding the folder /api/models from docker

base image: https://github.com/jomjol/docker-synology-opencv-tensorflow-lite

TensorFLowLite without support the avx extension
can run on synology with intel processor

http://127.0.0.1:8000/redoc - api docs

http://127.0.0.1:8000/process - api

uvicorn server:app --reload - start server


basic functionality:

GET /process
  query parameters:  
-  [Optional] model - name of the folder that contains the model
-  [Required] url - the URL of the image to be processed
-  [Optional] token - in case a token is needed in order to access the image

Output - JSON:
-  url - the URL that was processed
-  name - the temporary name of the processed file
-  result:
    - Prediction - the result of the process
    - Confidences - accuracy of the result in float32
