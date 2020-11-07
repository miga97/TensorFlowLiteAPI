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

EXPOSE 8000

CMD ["cd /api && uvicorn", "test:app --reload"]