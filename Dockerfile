FROM python:3.6.7
COPY app /app
WORKDIR app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD nameko run --config config.yml service