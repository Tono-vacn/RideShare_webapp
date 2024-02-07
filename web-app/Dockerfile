FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apt-get update && apt-get install -yq --no-install-recommends libcairo2-dev && apt-get clean
RUN pip install -r requirements.txt
RUN pip install --upgrade six urllib3 requests
ADD . /code/
RUN chmod o+x initserver.sh
RUN chmod o+x runserver.sh
RUN chown nobody:nogroup /code/token.json
RUN chmod 777 /code/token.json 