FROM django

ADD . /

WORKDIR .

RUN pip install -r requirements.txt

CMD ["python3", "manage.py", "runserver"]
