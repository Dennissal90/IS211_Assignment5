import csv
import queue as q

class Request:
    def __init__(self, request_time, process_time):
        self.timestamp = request_time
        self.process_time = process_time

    def wait_time(self, current_time):
        return current_time - self.timestamp

class Server:
    def __init__(self):
        self.current_request = None
        self.time_remaining = 0

    def tick(self):
        if self.current_request is not None:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_request = None

    def busy(self):
        return self.current_request is not None

    def start_next(self, new_request):
        self.current_request = new_request
        self.time_remaining = new_request.process_time

def load_requests(filename):
    requests = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                request_time, process_time = map(int, row[:2])
                requests.append(Request(request_time, process_time))
            except ValueError:
                print(f"Skipping invalid row: {row}")
    return requests

def simulate_single_server(requests):
    server = Server()
    queue = q.Queue()
    waiting_times = []
    current_time = 0

    for request in requests:
        queue.put(request)

    while not queue.empty():
        if not server.busy() and not queue.empty():
            next_request = queue.get()
            waiting_times.append(next_request.wait_time(current_time))
            server.start_next(next_request)

        server.tick()
        current_time += 1

    average_wait = sum(waiting_times) / len(waiting_times)
    print(f"Single Server: Average Wait {average_wait:.2f} secs with {len(waiting_times)} requests.")

def simulate_multiple_servers(requests, number_of_servers):
    servers = [Server() for _ in range(number_of_servers)]
    queue = q.Queue()
    waiting_times = []
    current_time = 0

    for request in requests:
        queue.put(request)

    while not queue.empty():
        for server in servers:
            if not server.busy() and not queue.empty():
                next_request = queue.get()
                waiting_times.append(next_request.wait_time(current_time))
                server.start_next(next_request)

        for server in servers:
            server.tick()

        current_time += 1

    average_wait = sum(waiting_times) / len(waiting_times)
    print(f"Multiple Servers: Average Wait {average_wait:.2f} secs with {len(waiting_times)} requests.")

def main():
    requests = load_requests('requests.csv')
    simulate_single_server(requests)
    simulate_multiple_servers(requests, 3)

if __name__ == "__main__":
    main()
