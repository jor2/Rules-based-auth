FROM python:3.6-alpine
WORKDIR /backend
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base
COPY requirements.txt /backend
COPY app.py /backend
COPY utils/utils.py /backend
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]