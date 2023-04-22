import random
import math
from typing import List

random.seed()

class Event:
    def __init__(self, type: int, time: float, cpu: int, raw_time = None):
        self.type = type
        self.time = time
        self.cpu = cpu
        self.raw_time = raw_time

def generate_service_time(avg_service_time: float) -> float:
    rand = random.uniform(0, 1)
    gen_service_time = -(avg_service_time) * math.log(rand) 
    return gen_service_time 

def generate_interarr_time(avg_arrival_rate: float) -> float:
    rand = random.uniform(0, 1)
    gen_interarr_time = -(1.0 / avg_arrival_rate) * math.log(rand) 
    return gen_interarr_time 

def schedule_event(type: int, time_unit: float, cpu: int, event_queue: List[Event]) -> None:
    if len(event_queue) == 0 or time_unit < event_queue[0].time:
        event_queue.insert(0, Event(type, time_unit, cpu))
    elif time_unit >= event_queue[-1].time:
        event_queue.append(Event(type, time_unit, cpu))
    else:
        for i, event in enumerate(event_queue):
            if time_unit < event.time:
                event_queue.insert(i, Event(type, time_unit, cpu))
                break

def priority_event_scheduler(event_queue, new_event):
    for i, event in enumerate(event_queue):
        if new_event.time <= event.time:
            event_queue.insert(i, new_event)
            return
    event_queue.append(new_event)


def run_scenario_1(avg_arrival_rate: float, avg_service_time: float, num_cpus: int) -> None:
    event_queue = [[] for _ in range(num_cpus)]  # create a separate event queue for each CPU
    total_processes = 10000
    ARR = 0
    DEP = 1

    #Variables for running the simulation
    server_idle = [True] * num_cpus
    num_of_processes = [0] * num_cpus
    ready_queue_count = [0] * num_cpus
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

    # Schedule initial arrival event for each CPU
    for i in range(num_cpus):
        schedule_event(ARR, t, num_cpus, event_queue[i])

    while num_of_processes[0] < total_processes:  # check if first CPU has reached the total number of processes
        chosen_cpu = random.randint(0, num_cpus - 1)  # randomly choose a CPU
        e = event_queue[chosen_cpu].pop(0)
        clock = e.time

        if e.type == ARR:
            if server_idle[chosen_cpu]:
                server_idle[chosen_cpu] = False
                s = generate_service_time(avg_service_time)
                schedule_event(DEP, clock + s, num_cpus, event_queue[chosen_cpu])
                total_service_time += s   
                num_of_processes[chosen_cpu] += 1
            else:
                ready_queue_count[chosen_cpu] += 1

            a = generate_interarr_time(avg_arrival_rate)
            schedule_event(ARR, clock + a, num_cpus, event_queue[chosen_cpu])

        elif e.type == DEP:
            if ready_queue_count[chosen_cpu] == 0:
                server_idle[chosen_cpu] = True
            else:
                ready_queue_count[chosen_cpu] -= 1
                s = generate_service_time(avg_service_time)
                schedule_event(DEP, clock + s, num_cpus, event_queue[chosen_cpu])
                total_service_time += s
                num_of_processes[chosen_cpu] += 1

        else:
            raise ValueError("Invalid event type.")

    # Find the last departure time across all CPUs
    for i in range(num_cpus):
        for event in event_queue[i]:
            if event.type == DEP and event.time > last_departure:
                last_departure = event.time

    #Metric calculations
    throughput = total_processes / last_departure
    actual_avg_service_time = total_service_time / total_processes
    cpu_util = total_service_time / last_departure
    avg_num_in_sys = cpu_util / (1 - cpu_util)
    avg_num_in_queue = avg_num_in_sys - cpu_util
    actual_avg_arrival_rate = cpu_util / actual_avg_service_time
    turnaround = avg_num_in_sys / actual_avg_arrival_rate

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
    print("enter the number of CPU's to use :")
    num_cpus = int(input())
    print("running simulation ...")
    ''' 
    #run_scenario_1(10,0.02,5)
    #apple
    
    
    '''

    for i in range (10,32):
        run (i,.04)
    '''

main()

