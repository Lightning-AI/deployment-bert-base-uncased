FROM python:3.10-slim

####### Add your own installation commands here #######
# RUN pip install some-package
# RUN wget https://path/to/some/data/or/weights
# RUN apt-get update && apt-get install -y <package-name>

WORKDIR /app
COPY . /app

# Install litserve and requirements
RUN pip install --no-cache-dir litserve==0.2.3
EXPOSE 8000
CMD ["python", "/app/server.py"]
