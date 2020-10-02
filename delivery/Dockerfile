FROM python:3.8.6-alpine
WORKDIR /delivery
ADD . /delivery
RUN pip install -r requirements.txt
CMD ["gunicorn", "app:app"]