import random

arrival_rate = 2.0 
process = 1000
arrival_and_service = []

def problem_3():
    
    service_time = 1.0 #according to exponential distribution
    arrival_time = 0
    actual_arrival_time = 0
    actual_service_time = 0

    for id in range(1, process+1):
        # Poission Distribution Summation of Arrival Times
        arrival_time += random.expovariate(arrival_rate)

        # Exponential Distribution of Service Times
        service_time = random.expovariate(1/service_time)
        
        #putting the data in the array 
        step = (id, arrival_rate, service_time)
        arrival_and_service.append(step)
        
        #print the data in the given format current process, arrival time and srvice time 
        current_step = (id, arrival_time, service_time)
        print(current_step)

    # find the Actual Average Arrival Time
    actual_arrival_time = process/arrival_time
    # find the Actual Average Service Time
    for i in range(len(arrival_and_service)):
        actual_service_time += arrival_and_service[i][2]
    actual_service_time /= process

    print("Average Actual Arrival Time in secs: " + str(actual_arrival_time))
    print("Average Actual Service Time in secs: " + str(actual_service_time))
    
problem_3()

#all don