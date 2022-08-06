FROM python:3.9.5-slim

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app/
#
#RUN pyinstaller --onefile main.py
#
#RUN rm main.py
#
#ENTRYPOINT ["./dist/main"]

ENTRYPOINT ["python3", "bot.py"]