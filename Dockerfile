FROM dotriver/alpine-s6

RUN apk --no-cache add python3 py3-pip

RUN pip3 install \
    prometheus_client


ADD conf/ /

RUN set -x \
    && chmod +x /etc/s6/services/*/*
