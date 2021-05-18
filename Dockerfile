FROM python:3.8-alpine
RUN pip3 install requests
WORKDIR /app
COPY src .
RUN mkdir -p /opt/resource && \
    for script in check in out; do ln -sv /app/$script.py /opt/resource/$script && chmod +x $script.py; done
