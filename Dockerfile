FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8080

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV FLASK_APP=app/app.py

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "-p", "8000"]