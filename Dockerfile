FROM jomjol/synology-opencv-tensorflow-lite

RUN pip3 --no-cache-dir install \
    PIL \
    wget \
    fastapi \
    numpy \
    uvicorn

CMD ["uvicorn", "server:app"]