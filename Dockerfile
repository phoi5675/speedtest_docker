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
	'*/30 * * * * root sh /script.sh' \
	'#Empty line' > /etc/cron.d/cron_networktest

RUN chmod 0644 /etc/cron.d/cron_networktest
RUN crontab /etc/cron.d/cron_networktest

RUN mkdir -m 0755 /logs

CMD ["cron", "-f"]