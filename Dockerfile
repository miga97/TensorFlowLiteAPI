FROM jomjol/synology-opencv-tensorflow-lite

WORKDIR /
RUN mkdir /api
WORKDIR /api
COPY . .

RUN pip3 --no-cache-dir install \
    PIL \
    wget \
    fastapi \
    numpy \
    uvicorn

EXPOSE 8000

CMD ["cd /api/server && uvicorn", "test:app --reload"]