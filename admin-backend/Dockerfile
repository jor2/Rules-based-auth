FROM python:3.6-alpine
WORKDIR /admin-backend
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base
COPY requirements.txt /admin-backend
COPY app.py /admin-backend
COPY utils/utils.py /admin-backend
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]