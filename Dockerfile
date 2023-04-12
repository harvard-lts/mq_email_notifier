FROM python:3.8-slim-buster
COPY requirements.txt /tmp/

RUN pip install --upgrade pip && \
  pip install --upgrade --force-reinstall -r /tmp/requirements.txt -i https://pypi.org/simple/ --extra-index-url https://test.pypi.org/simple/

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

#CMD ['python', '-v']