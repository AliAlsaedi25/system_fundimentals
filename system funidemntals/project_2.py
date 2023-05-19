import random
import math
from typing import List
import sys

random.seed()

class Event:
    def __init__(self, type, time, cpu, raw_time = None):
        self.type = type
        self.time = time
        self.cpu = cpu
        self.raw_time = raw_time

def generate_service_time(avg_service_time):
    rand = random.uniform(0, 1)
    gen_service_time = -(avg_service_time) * math.log(rand) 
    return gen_service_time 

def generate_interarr_time(avg_arrival_rate):
    rand = random.uniform(0, 1)
    gen_interarr_time = -(1.0 / avg_arrival_rate) * math.log(rand) 
    return gen_interarr_time 

def schedule_event(type, time_unit, cpu, event_queue: List[Event]):
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


def run_scenario_1 (avg_arrival_rate, avg_service_time, num_cpus):
    total_processes = 10000

    # Initialize simulation state
    event_queue = []
    clock = 0
    process_iter = 1
    cpu_tracker = [{"cpu_id": i, "ready_queue": [], "ready_queue_num_processes_list": [], "is_idle": 1, "proc_id": None, "arr_time": 0, "serv_time": 0} for i in range(num_cpus)]
    turn_around_times = []

    # Generate initial arrival event
    new_event = Event("ARR", generate_interarr_time(avg_arrival_rate), process_iter)
    priority_event_scheduler(event_queue, new_event)

    # Main simulation loop
    while process_iter <= total_processes:
        # Retrieve next event from event queue and update clock
        event = event_queue.pop(0)
        clock = event.time

        if event.type == "ARR":
            # Process arrival event
            chosen_cpu = random.randint(0, num_cpus - 1)
            cpu = cpu_tracker[chosen_cpu]

            if cpu["is_idle"]:
                # Assign process to idle CPU and schedule its departure event
                cpu["is_idle"] = False
                cpu["proc_id"] = event.cpu
                cpu["arr_time"] = event.time
                new_service_time = generate_service_time(avg_service_time)
                new_event = Event("DEP", clock + new_service_time, event.cpu, new_service_time)
                priority_event_scheduler(event_queue, new_event)
            else:
                # Add process to ready queue of chosen CPU
                cpu["ready_queue"].append(event)

            # Schedule next arrival event and update process count
            process_iter += 1
            new_event = Event("ARR", clock + generate_interarr_time(avg_arrival_rate), process_iter)
            priority_event_scheduler(event_queue, new_event)

        elif event.type == "DEP":
            # Process departure event
            for cpu in cpu_tracker:
                if cpu["proc_id"] == event.cpu:
                    # Free CPU and record process metrics
                    cpu["is_idle"] = True
                    cpu["serv_time"] += event.raw_time
                    turn_around_times.append(event.time - cpu["arr_time"])

                    # Check if there are processes waiting in the ready queue
                    if cpu["ready_queue"]:
                        # Assign next process in queue to CPU and schedule its departure event
                        ready_event = cpu["ready_queue"].pop(0)
                        cpu["is_idle"] = False
                        cpu["proc_id"] = ready_event.cpu
                        cpu["arr_time"] = ready_event.time
                        new_service_time = generate_service_time(avg_service_time)
                        new_event = Event("DEP", clock + new_service_time, ready_event.cpu, new_service_time)
                        priority_event_scheduler(event_queue, new_event)
                    break

        # Record size of each CPU's ready queue
        for cpu in cpu_tracker:
            cpu["ready_queue_num_processes_list"].append(len(cpu["ready_queue"]))

    turnaround = sum(turn_around_times)/len(turn_around_times)
    avg_num_in_queue = sum(cpu['ready_queue_num_processes_list'])/len(cpu['ready_queue_num_processes_list'])
    completed_process = len(turn_around_times)
    throughput = completed_process/clock

    
    print(f"The last departure was at {round(clock,2)}")
    print("Metrics for an average arrival rate of " + str(avg_arrival_rate) + " per second:")
    print(f"Average Turnaround Time: " + str(turnaround) + " seconds")
    print("Total throughput: " + str(throughput) + " processes/second")
    print("CPU Utilization(s)")
    for i, cpu in enumerate(cpu_tracker):
        cpu_util = cpu["serv_time"] / clock * 100
        cpu_util = round(cpu_util,2)
        print("CPU utilization: " + str(cpu_util) + "%")
   
    print("Average number of processes in the ready queue: " + str(avg_num_in_queue) + " processes\n")



def run_scenario_2(avg_arrival_rate, avg_service_time, num_cpus):

    total_processes = 10000

    event_queue = []
    ready_queue = []
    clock = 0
    process_iter = 1
    cpu_tracker = [{'cpu_id': i, 'is_idle': True, 'proc_id': None, 'arr_time': 0, 'serv_time': 0}
                   for i in range(num_cpus)]

    # metrics
    turn_around_times = []
    ready_queue_num_processes_list = []

    # initial event
    new_event = Event('ARR', generate_interarr_time(avg_arrival_rate), process_iter)
    priority_event_scheduler(event_queue, new_event)

    while process_iter <= total_processes:
        event = event_queue.pop(0)
        clock = event.time

        if event.type == 'ARR':
            idle_cpus = [cpu for cpu in cpu_tracker if cpu['is_idle']]

            if idle_cpus:
                cpu = idle_cpus[0]
                cpu['is_idle'] = False
                cpu['proc_id'] = event.cpu
                cpu['arr_time'] = event.time
                new_service_time = generate_service_time(avg_service_time)
                new_event = Event('DEP', clock + new_service_time, event.cpu, new_service_time)
                priority_event_scheduler(event_queue, new_event)
                process_iter += 1
            else:
                ready_queue.append(event)

            new_event = Event('ARR', clock + generate_interarr_time(avg_arrival_rate), process_iter)
            priority_event_scheduler(event_queue, new_event)
        elif event.type == 'DEP':
            not_idle_cpus = [cpu for cpu in cpu_tracker if not cpu['is_idle']]

            for cpu in not_idle_cpus:
                if cpu['proc_id'] == event.cpu:
                    cpu['is_idle'] = True
                    cpu['serv_time'] += event.raw_time
                    turn_around_times.append(event.time - cpu['arr_time'])
                    break

            if ready_queue and any(cpu['is_idle'] for cpu in cpu_tracker):
                ready_event = ready_queue.pop(0)
                cpu = next(cpu for cpu in cpu_tracker if cpu['is_idle'])
                cpu['is_idle'] = False
                cpu['proc_id'] = ready_event.cpu
                cpu['arr_time'] = ready_event.time
                new_service_time = generate_service_time(avg_service_time)
                new_event = Event('DEP', clock + new_service_time, ready_event.cpu, new_service_time)
                priority_event_scheduler(event_queue, new_event)
                process_iter += 1

        ready_queue_num_processes_list.append(len(ready_queue))


    turnaround = sum(turn_around_times)/len(turn_around_times)
    avg_num_in_queue = sum(ready_queue_num_processes_list)/len(ready_queue_num_processes_list)
    completed_process = len(turn_around_times)
    throughput = completed_process/clock

    
    print(f"The last departure was at {round(clock,2)}")
    print("Metrics for an average arrival rate of " + str(avg_arrival_rate) + " per second:")
    print(f"Average Turnaround Time: " + str(turnaround) + " seconds")
    print("Total throughput: " + str(throughput) + " processes/second")
    print("CPU Utilization(s)")
    for i, cpu in enumerate(cpu_tracker):
        cpu_util = cpu["serv_time"] / clock * 100
        cpu_util = round(cpu_util,2)
        print("CPU utilization: " + str(cpu_util) + "%")
   
    print("Average number of processes in the ready queue: " + str(avg_num_in_queue) + " processes\n")


if __name__ == "__main__":
    
    if len(sys.argv) != 5:
        print("Usage: python3 problem1.py <avg_arrival_rate> <avg_service_time> <scenario> <num_cpus>")
        sys.exit(1)

    avg_arrival_rate = float(sys.argv[1]) 
    avg_service_time = float(sys.argv[2]) 
    scenario_choice = int(sys.argv[3]) 
    num_cpus = int(sys.argv[4])
    
    if scenario_choice == 1:
        run_scenario_1(avg_arrival_rate, avg_service_time, num_cpus)
    elif scenario_choice == 2:
        run_scenario_2(avg_arrival_rate, avg_service_time, num_cpus)
    else:
        print("SCENARIO CHOICE MUST BE EITHER 1 OR 2")
        sys.exit(1)

#all done 
