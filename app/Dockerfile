FROM python:3.8.5
WORKDIR /usr/src/app
COPY requirements.txt .

ENV PYTHONUNBUFFERED 1
ENV LIBRDKAFKA_VERSION v1.8.2
RUN \
    echo Installing librdkafka && \
    mkdir -p /usr/src/librdkafka && \
    cd /usr/src/librdkafka && \
    curl -LfsS https://github.com/edenhill/librdkafka/archive/${LIBRDKAFKA_VERSION}.tar.gz | \
    tar xvzf - --strip-components=1 && \
    ./configure --prefix=/usr --disable-lz4-ext && \
    make -j && \
    make install && \
    cd / && \
    rm -rf /usr/src/librdkafka

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN chmod +x utils/wait-for-it.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]