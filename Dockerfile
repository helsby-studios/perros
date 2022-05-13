FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-deps --no-cache-dir

EXPOSE 80

CMD [ "python", "bot.py" ]