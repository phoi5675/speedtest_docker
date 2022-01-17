import os
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

LOGS_DIR = '.\\logs\\' if os.name == 'nt' else './logs/'

local_format = "%H:%M"
KST = +9


def read_logs() -> list:
    files = os.listdir(LOGS_DIR)
    jsons = [json for json in files if json.__str__().__contains__("json")]

    return jsons


def read_jsons() -> list:
    _jsons: list = []
    for json_file in json_files:
        with open(LOGS_DIR + str(json_file), 'r') as j_file:
            _jsons.append(json.load(j_file))

    return _jsons


def convert_to_Mbit(bitrate: int) -> float:
    return float(bitrate) / (1000 * 1000 / 8)


def make_axis_elem(jsons:list, x_axis: list, y_axis_downspd: list, y_axis_upspd: list) -> None:
    for json in jsons:
        date: str = json['timestamp']

        from_date: datetime = datetime.strptime(
            date,
            "%Y-%m-%dT%H:%M:%SZ",
        )
        date_converted = from_date + timedelta(hours=KST)

        down_speed: int = int(json['download']['bandwidth'])
        up_speed: int = int(json['upload']['bandwidth'])
        # print('date : {0}, down : {1:.2f}Mbps, up : {2:.2f}Mbps'.format(
        #     date_converted.strftime(local_format), convert_to_Mbit(down_speed), convert_to_Mbit(up_speed)))

        x_axis.append(date_converted.strftime(local_format))
        y_axis_downspd.append(convert_to_Mbit(down_speed))
        y_axis_upspd.append((convert_to_Mbit(up_speed)))


if __name__ == '__main__':

    json_files: list = read_logs()
    json_files.sort()

    jsons: list = read_jsons()

    x_axis_timestamp: list = []
    y_axis_download_spd: list = []
    y_axis_upload_spd: list = []

    make_axis_elem(jsons, x_axis_timestamp, y_axis_download_spd, y_axis_upload_spd)

    plt.plot(x_axis_timestamp, y_axis_download_spd, x_axis_timestamp, y_axis_upload_spd)
    xlabels = x_axis_timestamp[::4]
    plt.xlabel('timestamp')
    plt.xticks(ticks=x_axis_timestamp, rotation=45)

    plt.locator_params(axis='x', nbins=len(xlabels))
    plt.ylabel('Network speed(in Mbps)')

    plt.show()
