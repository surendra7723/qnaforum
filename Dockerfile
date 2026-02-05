FROM python:3.12

#Set environment variables
ENV DONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory 
WORKDIR /qnaforum

# Install dependencies
COPY Pipfile.lock /qnaforum/

# Copy Project
COPY . /qnaforum/
