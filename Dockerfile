FROM jomjol/synology-opencv-tensorflow-lite

WORKDIR /
RUN mkdir /api
WORKDIR /api
COPY . .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade Pillow

RUN pip3 --no-cache-dir install \
    wget \
    fastapi \
    numpy \
    uvicorn

EXPOSE 80

CMD ["uvicorn", "test:app", "--reload", "--host", "0.0.0.0", "--port", "80"]