import random
import math
from typing import List
 
class Event:
    def __init__(self, type: int, time: float):
        self.type = type
        self.time = time

def generate_service_time(avg_service_time: float) -> float:
    rand = random.uniform(0, 1)
    gen_service_time = -(avg_service_time) * math.log(rand) 
    return gen_service_time 

def generate_interarr_time(avg_arrival_rate: float) -> float:
    rand = random.uniform(0, 1)
    gen_interarr_time = -(1.0 / avg_arrival_rate) * math.log(rand) 
    return gen_interarr_time 

def schedule_event(type: int, time_unit: float, event_queue: List[Event]) -> None:
    if len(event_queue) == 0 or time_unit < event_queue[0].time:
        event_queue.insert(0, Event(type, time_unit))
    elif time_unit >= event_queue[-1].time:
        event_queue.append(Event(type, time_unit))
    else:
        for i, event in enumerate(event_queue):
            if time_unit < event.time:
                event_queue.insert(i, Event(type, time_unit))
                break

def run(avg_arrival_rate: float, avg_service_time: float) -> None:
    event_queue = []

    total_processes = 10000
    ARR = 0
    DEP = 1

    #Variables for running the simulation
    server_idle = True
    num_of_processes = 0
    ready_queue_count = 0
    clock = 0
    t = clock + generate_interarr_time(avg_arrival_rate)
    a = 0
    s = 0

    #Variables for calculating metrics
    turnaround = 0
    throughput = 0
    cpu_util = 0
    avg_num_in_sys = 0
    actual_avg_service_time = 0
    actual_avg_arrival_rate = 0
    avg_num_in_queue = 0
    last_departure = 0
    total_service_time = 0

    schedule_event(ARR, t, event_queue)

    while num_of_processes < total_processes:
        e = event_queue.pop(0)
        clock = e.time

        if e.type == ARR:
            if server_idle:
                server_idle = False
                s = generate_service_time(avg_service_time)
                schedule_event(DEP, clock + s, event_queue)
                total_service_time += s   
                num_of_processes += 1
            else:
                ready_queue_count += 1

            a = generate_interarr_time(avg_arrival_rate)
            schedule_event(ARR, clock + a, event_queue)

        elif e.type == DEP:
            if ready_queue_count == 0:
                server_idle = True
            else:
                ready_queue_count -= 1
                s = generate_service_time(avg_service_time)
                schedule_event(DEP, clock + s, event_queue)
                total_service_time += s
                num_of_processes += 1

        else:
            raise ValueError("Invalid event type.")

    for i in event_queue:
        if i.type == DEP:
            last_departure = i.time
            break

    #Metric calculations
    throughput = total_processes / last_departure
    actual_avg_service_time = total_service_time / total_processes
    cpu_util = total_service_time / last_departure
    avg_num_in_sys = cpu_util / (1 - cpu_util)
    avg_num_in_queue = avg_num_in_sys - cpu_util
    actual_avg_arrival_rate = cpu_util / actual_avg_service_time
    turnaround = avg_num_in_sys/ actual_avg_arrival_rate

    print("The last departure was at: " + str(last_departure))
    print("Metrics for an average arrival rate of " + str(avg_arrival_rate) + " per second:")
    print("Average turnaround time: " + str(turnaround) + " seconds")
    print("Total throughput: " + str(throughput) + " processes/second")
    print("CPU utilization: " + str(cpu_util * 100) + "%")
    print("Average number of processes in the ready queue: " + str(avg_num_in_queue) + " processes\n")

def main():

    '''
    print('Enter the average arrival rate (lambda) for this run: ')
    average_arrival_rate = float(input()) # Convert input to float
    print('Enter the average service time (Ts) for this run: ')
    average_service_time = float(input()) # Convert input to float
    print("running simulation ...")
    run(average_arrival_rate, average_service_time)
    '''

    for i in range (10,32):
        run (i,.04)

main()

