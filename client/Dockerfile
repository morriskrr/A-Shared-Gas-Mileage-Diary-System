FROM python:3.9-slim-buster

# set the working directory
WORKDIR /client

# copy the requirements file and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the application files
COPY . .

# run the client script
CMD ["python", "client.py"]