FROM thomasweise/docker-texlive-full

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update -y && apt-get install -y python3-pip python3-venv

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt >requirements.txt

RUN pip install -r requirements.txt

COPY . .

WORKDIR /workdir

ENTRYPOINT ["python", "/app/multable/main.py", "--output", "/workdir/multable.pdf"]
