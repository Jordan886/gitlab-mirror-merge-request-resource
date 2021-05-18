FROM python:3.8-alpine
WORKDIR /app
COPY src .
RUN mkdir -p /opt/resource && \
    for script in check in out; do ln -sv $(which $script) /opt/resource/; done
RUN chmod +x /opt/resource/out /opt/resource/in /opt/resource/check
