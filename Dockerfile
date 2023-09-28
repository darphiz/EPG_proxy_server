FROM python:3.11.5
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
# Create app log directory
RUN mkdir -p /var/log/app
# create app log file
RUN touch /var/log/app/app.log

COPY . /app/
EXPOSE 8080
CMD ["gunicorn", "-c", "guni.py", "--bind", "0.0.0.0:8080", "app:app"]