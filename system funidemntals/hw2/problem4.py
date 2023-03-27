import numpy
def part_a():

    mtbf = 500
    repair_time = 10
    years = 20

    total_hours_in_x_years = years * 365 * 24

    #get a random number of falirures for each server using random and an exponential function from the numpy library
    failures = numpy.random.exponential(scale=mtbf, size=2 * int(total_hours_in_x_years/mtbf))

    #using dictionaries to keep track of repair times and failure times 
    failure_times_log = {'Server': [], 'Failure Time':[]}
    repair_times_log = {'Server': [], 'Reapair TIme':[]}

    #go through each failure to calculate the when the failure and the repair take place
    server = 1
    failure_time = 0
    repair_time_tracker = 0
    for i in range(len(failures)):
        failure_time += failures[i]

        if failure_time >= total_hours_in_x_years:
            break

        failure_times_log['Server'].append(server)
        failure_times_log['Failure Time'].append(failure_time)
        repair_time_tracker += repair_time
        repair_times_log['Server'].append(server)
        repair_times_log['Reapair TIme'].append(failure_time + repair_time_tracker)


        if server == 1:
            server = 2
        else:
            server = 1

        print('server: ')
        print(failure_times_log['Server'][i])
        print("fail time at year: ")
        print(round(int(failure_times_log['Failure Time'][i])/(360*24),1))
        print('server: ')
        print(repair_times_log['Server'][i])
        print("repair time at year: ")
        print(round(int(repair_times_log['Reapair TIme'][i])/(360*24),1))

        



def part_b ():

    mtbf = 500
    years = 20
    repair_time = 10
    iterations = input('how many interations would you like to go through: ' )
    iterations = int(iterations)
    
    # Total hours in simulation period
    total_hours_in_x_years = years * 365 * 24

    # Set random seed for reproducibility
    numpy.random.seed()

    # Keep track of system failure times across all simulations
    system_failure_times = []

    for i in range(iterations):
        # Generate a list of failure times using an exponential distribution with the specified MTBF
        failures = numpy.random.exponential(scale=mtbf, size=2 * int(total_hours_in_x_years/mtbf))

        # Using dictionaries to keep track of repair times and failure times 
        failure_times_log = {'Server': [], 'Failure Time':[]}
        repair_times_log = {'Server': [], 'Repair Time':[]}

        # Go through each failure to calculate the when the failure and the repair take place
        server = 1
        failure_time = 0
        repair_time_tracker = 0
        for j in range(len(failures)):
            failure_time += failures[j]
            if failure_time >= total_hours_in_x_years:
                break
            failure_times_log['Server'].append(server)
            failure_times_log['Failure Time'].append(failure_time)
            repair_time_tracker += repair_time
            repair_times_log['Server'].append(server)
            repair_times_log['Repair Time'].append(failure_time + repair_time_tracker)

            # If both servers fail within the repair time, record the system failure time
            if len(repair_times_log['Repair Time']) >= 2 and repair_times_log['Repair Time'][-2] > failure_time:
                system_failure_times.append(failure_time)
                break

            # Switch to the other server
            if server == 1:
                server = 2
            else:
                server = 1

    # Calculate the average system failure time across all simulations
    avg_system_failure_time = sum(system_failure_times) / len(system_failure_times)

    print ( 'the average time until failure for the number of iterations you provided was: ')
    print (avg_system_failure_time)

part_a()
part_b()

#all done