FROM python:latest



RUN git clone https://github.com/KartikeyaReddy24/ExtractingEmails.git

RUN pip install --upgrade pip

WORKDIR /ExtractingEmails

RUN python -m pip install -r requirements.txt

RUN python -m pip install googlesearch-python

RUN python -m pip install xlsxwriter

# COPY . /app

CMD ["python", "./ExtractEmails_v2.2.py"]
