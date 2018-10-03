import csv
import json
from subprocess import PIPE, Popen
import threading
import time

global_counter = 0


def load_csv(filename=''):
    with open(filename, 'r') as csv_file:
        urls = list(csv.reader(csv_file))
        # retrieving first and last 100 urls from list
        main_urls = urls[:100] + urls[-100:]
        return [main_url[1] for main_url in main_urls]


def execute_command(args, urls, command_output_list, lock):
    global global_counter

    while global_counter < len(urls):
        lock.acquire()
        current_index = global_counter
        global_counter += 1
        lock.release()
        p = Popen(args + [urls[current_index]], stdout=PIPE)
        command_output_list[current_index]['target'] = urls[current_index]
        command_output_list[current_index]['output'] = (p.communicate()[0]).decode('ascii')


def command_to_file(command_name='', filename='', urls=[], n_threads=4):
    # reset global_counter
    global global_counter
    global_counter = 0
    lock = threading.Lock()
    threads = []
    command_output_list = [{} for _ in range(len(urls))]
    args = []

    if command_name == 'ping':
        args = ['ping', '-c', '10']
    elif command_name == 'traceroute':
        args = ['traceroute', '-m', '30']

    for _ in range(n_threads):
        threads.append(threading.Thread(target=execute_command, args=(args, urls, command_output_list, lock)))
        threads[-1].start()

    for thread in threads:
        thread.join()

    output_label = ''
    if command_name == 'ping':
        output_label = 'pings'
    elif command_name == 'traceroute':
        output_label = 'traces'

    data = {'date': '20180928',
            'system': 'MacOS',
            output_label: command_output_list}

    # Writing to JSON file
    with open(filename, "w") as write_file:
        json.dump(data, write_file)


def main():
    start_time = time.time()
    start_clock = time.clock()

    csv_filename = 'top-1m.csv'
    print('Loading urls from {}...'.format(csv_filename))
    urls = load_csv(csv_filename)
    print('URLs:', urls)
    print('Elapsed time: {} seconds and {} computing seconds'.format(time.time() - start_time, time.clock() - start_clock))

    print('Starting ping procedure...')    
    command_to_file('ping', 'ping.json', urls)
    print('Done.')    
    print('Elapsed time: {} seconds and {} computing seconds'.format(time.time() - start_time, time.clock() - start_clock))
        

    print('Starting traceroute procedure...')
    command_to_file('traceroute', 'traceroute.json', urls)
    print('Done.')
    print('Elapsed time: {} seconds and {} computing seconds'.format(time.time() - start_time, time.clock() - start_clock))


if __name__ == "__main__":
    main()

