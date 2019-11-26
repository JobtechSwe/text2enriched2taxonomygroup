FROM alpine:3.10

EXPOSE 8081

RUN apk update && apk upgrade && \
    apk add --no-cache --update \
        uwsgi-python3 \
        python3-dev \
        nginx \
        git \
        curl \
        tzdata \
        gcc \
        musl-dev && \
    rm -rfv /var/cache/apk/*


ENV TZ=Europe/Stockholm

COPY . /app

RUN date +"%Y-%m-%dT%H:%M:%S %Z" && \
    mkdir -p /var/run/nginx && \
    chmod -R 777 /var/run/nginx && \
    mkdir -p /var/run/supervisord /var/log/supervisord && \
    chmod -R 777 /var/run/supervisord && \
    chmod -R 775 /app && \
    chmod -R 777 /usr/sbin && \
    chmod -R 775 /usr/lib/python* && \
    chmod -R 775 /var/lib/nginx && \
    chmod -R 777 /var/log/* && \
    chmod -f -R 777 /var/lib/nginx/tmp && \
    chmod -f -R 777 /var/tmp/nginx || :

WORKDIR /app

RUN python3 -m pip install --upgrade pip setuptools
RUN python3 -m pip install supervisor

# runs unit tests with @pytest.mark.unit annotation only
RUN pip3 install --no-cache-dir -r requirements.txt && \
    python3 setup.py install


USER 10000
CMD ["/usr/bin/supervisord", "-n", "-c", "/app/supervisord.conf"]
