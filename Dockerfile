# set base image (host OS)
FROM python:3.10.12

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

EXPOSE 8200

# command to run on container start
CMD [ "python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8200" ]