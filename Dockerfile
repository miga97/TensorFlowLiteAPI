FROM jomjol/synology-opencv-tensorflow-lite

WORKDIR /
RUN mkdir /api
WORKDIR /api
RUN mkdir tmp
COPY . .

RUN pip uninstall opencv-python -y

RUN pip3 --no-cache-dir install \
    wget \
    fastapi \
    numpy \
    uvicorn

EXPOSE 80

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]