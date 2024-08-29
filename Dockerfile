# Base image
FROM python:3.11-slim
#FROM python:3.9

#Copy requirements
COPY requirements.txt /app/requirements.txt

#Upgrade pip
#RUN pip3 install --upgrade pip

# Copy files
COPY ./*.py /app/

# Set working directory
WORKDIR /app

# Install dependecies
RUN pip3 install --progress-bar off  -r requirements.txt


# Run the application
EXPOSE 8080
CMD ["gunicorn","--config", "gunicorn_config.py", "wsgi:application"]
