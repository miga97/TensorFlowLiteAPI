FROM jomjol/synology-opencv-tensorflow-lite

WORKDIR /
RUN mkdir /api
WORKDIR /api
RUN mkdir tmp
COPY . .

RUN python3 -m pip install --upgrade pip --no-cache-dir
RUN python3 -m pip install --upgrade Pillow --no-cache-dir

RUN pip3 --no-cache-dir install \
    wget \
    fastapi \
    numpy \
    uvicorn

EXPOSE 80

CMD ["uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "80"]