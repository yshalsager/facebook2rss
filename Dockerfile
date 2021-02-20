FROM ubuntu:20.04
 
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
	PYSETUP_PATH="/opt/facebook2rss" \
    VENV_PATH="/opt/facebook2rss/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
RUN export PATH=$PATH

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
		  python3.9\
		  python3-pip\
		  libglib2.0-0\
          libnss3\
          libnspr4\
          libatk1.0-0\
          libatk-bridge2.0-0\
          libcups2\
          libdbus-1-3\
          libxcb1\
          libdrm2\
          libxkbcommon0\
          libx11-6\
          libxcomposite1\
          libxdamage1\
          libxext6\
          libxfixes3\
          libxrandr2\
          libgbm1\
          libgtk-3-0\
          libpango-1.0-0\
          libcairo2\
          libgdk-pixbuf2.0-0\
          libasound2\
          libatspi2.0-0 \
		  libxshmfence1 \
		  libegl1 \
		  curl \
		  python3-venv \
		  && rm -rf /var/lib/apt/lists/*
	
WORKDIR $PYSETUP_PATH

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev
RUN playwright install chromium

COPY . .

#Fixing: https://bugs.launchpad.net/ubuntu/+source/tzdata/+bug/1899343
RUN echo "Etc/UTC" > /etc/timezone

EXPOSE 8080

RUN chmod +x start.sh
ENTRYPOINT ["./start.sh"]
