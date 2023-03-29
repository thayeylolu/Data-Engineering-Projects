FROM python:3.7-slim
COPY ./requirements.txt /Flask\ CRUD\ App\ with\ Aurora\ Serverless\ and\ Docker/requirements.txt
WORKDIR  /Flask\ CRUD\ App\ with\ Aurora\ Serverless\ and\ Docker
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8081
ENTRYPOINT ['python']
CMD ['-u', 'app.py']

