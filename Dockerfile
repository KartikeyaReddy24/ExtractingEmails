FROM ubuntu:latest


# FROM python:latest

RUN apt-get update

RUN apt-get install -y python3

RUN apt-get install -y git


RUN git clone https://github.com/KartikeyaReddy24/ExtractingEmails.git

WORKDIR /ExtractingEmails

RUN apt-get install -y python3-pip

RUN pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install googlesearch-python

RUN python3 -m pip install xlsxwriter

# COPY . /app

# RUN chmod 777 ExtractEmails_v2.2.py

# CMD ["python", "./ExtractEmails_v2.2.py"]

# CMD ["/ExtractEmails_v2.2.py"]

# ENTRYPOINT ["python"]

CMD [ "python3", "ExtractEmails_v2.5.py" ]








######################## OLD VERSION




# FROM python:latest



# RUN git clone https://github.com/KartikeyaReddy24/ExtractingEmails.git

# RUN pip install --upgrade pip

# WORKDIR /ExtractingEmails

# RUN python -m pip install -r requirements.txt

# RUN python -m pip install googlesearch-python

# RUN python -m pip install xlsxwriter

# # COPY . /app

# CMD ["python", "./ExtractEmails_v2.2.py"]
