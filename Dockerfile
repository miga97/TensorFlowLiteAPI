FROM python:3.7-slim

WORKDIR /

COPY ./wheels ./wheels
RUN pip install --no-cache-dir ./wheels/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_x86_64.whl
RUN rm -r ./wheels

RUN pip3 --no-cache-dir install \
    Pillow \
    wget \
    fastapi \
    uvicorn

RUN mkdir /api
WORKDIR /api
RUN mkdir tmp
COPY . .
RUN rm -r ./wheels

EXPOSE 80

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]