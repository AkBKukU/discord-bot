FROM python:3.8.3

WORKDIR /bot

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./AkBBot.py"]