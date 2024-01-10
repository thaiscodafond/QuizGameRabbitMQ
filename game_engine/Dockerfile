FROM python:3.11-alpine

COPY ./requirement.txt ./requirement.txt

RUN pip install -r requirement.txt

COPY . .

CMD [ "python", "main.py" ]