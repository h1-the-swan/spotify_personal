FROM python:3.8

WORKDIR /usr/local/src

COPY requirements-dev.txt .

COPY . .

RUN pip install -r requirements-dev.txt

EXPOSE 8870

ENTRYPOINT ["jupyter"]
CMD [ "notebook", "--no-browser", "--allow-root", "--ip", "0.0.0.0", "--port", "8870" ]
