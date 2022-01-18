FROM ubuntu:20.04

# Set timezone to make run cron based on GMT+9.
ENV TZ="Asia/Seoul"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Change apt list to mirror in Korea.
RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

# Install packages.
RUN export DEBIAN_FRONTEND=noninteractive

RUN apt-get update

RUN apt-get install -y \
	curl vim cron

# Install speedtest
RUN curl -s https://install.speedtest.net/app/cli/install.deb.sh | bash
RUN apt-get install speedtest

# Install cron
COPY ./script.sh /script.sh
RUN chmod 0644 /script.sh

RUN printf '%s\n' \
	'*/10 * * * * root sh /script.sh' \
	'#Empty line' > /etc/cron.d/cron_networktest

RUN chmod 0644 /etc/cron.d/cron_networktest
RUN crontab /etc/cron.d/cron_networktest

RUN mkdir -m 0755 /logs

# Install python
RUN apt-get install -y python3 python3-pip python3-dev
RUN pip3 install --upgrade pip

COPY ./plot/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
RUN rm requirements.txt

CMD ["cron", "-f"]