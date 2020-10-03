FROM python:3.8.6-alpine
WORKDIR /delivery
ADD . /delivery
RUN pip install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
