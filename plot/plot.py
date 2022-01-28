import os
import json
import matplotlib.pyplot as plt
import argparse
import csv
from datetime import datetime, timedelta
from scipy.ndimage import gaussian_filter1d

LOGS_DIR = '..\\logs\\' if os.name == 'nt' else '../logs/'

local_format = "%m-%d-%H:%M"
KST = +9

parser = argparse.ArgumentParser(description='plot network speed graph based on speedtest.net result')
args = None


def make_parser() -> argparse.Namespace:
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='verbose mode')
    parser.add_argument('--csv', action='store_true',
                        help='save result as csv file')
    parser.add_argument('--name', '-n', type=str, default='result.csv',
                        help='csv file will be saved as this argument string(default: result.csv)')

    return parser.parse_args()


def save_as_file(date: list, up_speed: list, down_speed: list) -> None:
    filename = args.name if '.csv' in args.name else args.name + '.csv'

    with open(filename, 'w', newline='') as file_writer:
        csv_writer = csv.writer(file_writer)

        # write header
        csv_writer.writerow(['date', 'upload_speed(Mbps)', 'download_speed(Mbps)'])
        for (d, up, down) in zip(date, up_speed, down_speed):
            csv_writer.writerow([d, up, down])


def read_logs() -> list:
    files = os.listdir(LOGS_DIR)
    _jsons = [_json for _json in files if _json.__str__().__contains__("json")]

    return _jsons


def read_jsons() -> list:
    _jsons: list = []
    for json_file in json_files:
        try:
            with open(LOGS_DIR + str(json_file), 'r') as j_file:
                _jsons.append(json.load(j_file))
        except Exception as ex:
            if args.verbose:
                print('fail to read json file!' + str(ex))

    return _jsons


def convert_to_Mbit(bitrate: int) -> float:
    return float(bitrate) / (1000 * 1000 / 8)


def make_axis_elem(_jsons:list, x_axis: list, y_axis_downspd: list, y_axis_upspd: list) -> None:
    for _json in _jsons:
        try:
            date: str = _json['timestamp']

            from_date: datetime = datetime.strptime(
                date,
                "%Y-%m-%dT%H:%M:%SZ",
            )
            date_converted = from_date + timedelta(hours=KST)

            down_speed: int = int(_json['download']['bandwidth'])
            up_speed: int = int(_json['upload']['bandwidth'])

            if args.verbose:
                print('time : {0}, down : {1:.2f}Mbps, up : {2:.2f}Mbps'.format(
                    date_converted.strftime(local_format), convert_to_Mbit(down_speed), convert_to_Mbit(up_speed)))

            x_axis.append(date_converted.strftime(local_format))
            y_axis_downspd.append(convert_to_Mbit(down_speed))
            y_axis_upspd.append((convert_to_Mbit(up_speed)))
        except Exception as ex:
            if args.verbose:
                print('fail to read data! ' + str(ex))


if __name__ == '__main__':
    args = make_parser()

    json_files: list = read_logs()
    json_files.sort()

    jsons: list = read_jsons()

    x_axis_timestamp: list = []
    y_axis_download_spd: list = []
    y_axis_upload_spd: list = []

    make_axis_elem(jsons, x_axis_timestamp, y_axis_download_spd, y_axis_upload_spd)

    if args.csv:
        save_as_file(date=x_axis_timestamp, up_speed=y_axis_upload_spd, down_speed=y_axis_download_spd)

    # plot graph
    y_download_smoothed = gaussian_filter1d(y_axis_download_spd, sigma=0.8)
    y_upload_smoothed = gaussian_filter1d(y_axis_upload_spd, sigma=0.8)

    plt.title('Network speed test')
    plt.plot(x_axis_timestamp, y_download_smoothed,
             linewidth='2', label='Download speed')
    plt.plot(x_axis_timestamp, y_upload_smoothed,
             linewidth='2', label='Upload speed')
    plt.legend(loc='upper left')

    xlabels_interval = int(len(x_axis_timestamp) / 15)
    xlabels = x_axis_timestamp[::xlabels_interval]
    plt.xlabel('timestamp')
    plt.xticks(ticks=x_axis_timestamp, rotation=45, fontsize=5)

    plt.locator_params(axis='x', nbins=len(xlabels))
    plt.ylabel('speed(Mbps)')

    ylabels = [mbps for mbps in range(0, 280, 15)]
    plt.yticks(ticks=ylabels, fontsize=5)

    plt.savefig('./graph.png', dpi=300)
