# speedtest_docker
run network speedtest every 10 minutes

# How to run
1. make logs folder in root of your local repository
1. build docker image
```shell
docker build --rm -t netspdtest .
```
1. run docker container
Script below is written based on windows. 
```shell
docker run -d --restart=always -v %cd%\logs:/logs \
	--name netspdtest netspdtest
```