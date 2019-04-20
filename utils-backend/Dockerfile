FROM python:3.6-alpine
WORKDIR /utils-backend
COPY requirements.txt /utils-backend
COPY app.py /utils-backend
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]