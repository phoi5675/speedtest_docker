# speedtest_docker

run network speedtest every 10 minutes


![image](./graph.png)


# How to run docker container
1. make logs folder in root of your local repository
1. build docker image
	
  ```shell
  docker build --rm -t netspdtest .
  ```
3. run docker container

  Script below is written based on windows. 
  ```shell
  docker run -d --restart=always \
  -v %cd%\logs:/logs -v %cd%\plot:/plot \
	--name netspdtest netspdtest
  ```

# How to plot network speed

If you use docker container, skip installing requirements.txt

- install requirements.txt

  ```shell
  pip3 install -r requirements.txt
  ```
- run plot.py
  
  ```shell
  python3 plot.py
  ```

# Plot options
```shell
# python3 plot.py --help
usage: plot.py [-h] [--verbose] [--csv] [--name NAME] [--method METHOD]

plot network speed graph based on speedtest.net result

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         verbose mode
  --csv                 save result as csv file
  --name NAME, -n NAME  csv file will be saved as this argument string(default: result.csv)
  --method METHOD       select plot method. options: daily_average, raw_graph
```