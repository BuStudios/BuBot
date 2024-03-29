# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

#this install all packages from the requirements.txt file
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Run the application.
CMD ["python3", "./main.py"]
# 👆 you need to use python3 otherwise it will not work