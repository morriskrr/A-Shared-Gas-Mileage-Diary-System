FROM python:3.9-slim-buster

# set the working directory
WORKDIR /client

RUN apt update && \
    apt install -y --no-install-recommends libgl1-mesa-glx libglib2.0-0 libxcb-xinerama0 qt5-default && \
    rm -rf /var/lists/apt/lists/*

# copy the requirements file and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the application files
COPY . .
ENV QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms/
# run the client script
CMD ["python", "SharedGasMileageDiary.py"]