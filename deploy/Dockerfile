FROM python:3.9.6-slim-buster

RUN pip install poetry==1.1.13

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Update pip
RUN python -m pip install --upgrade pip

# Installing requirements
RUN poetry install

# Install pytz
RUN pip install pytz
RUN pip install aerich

# Copying actuall application
COPY . /app/src/
RUN poetry install

RUN ls -la

CMD ["/usr/local/bin/python", "-m", "YandexApi"]
