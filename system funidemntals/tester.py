import numpy as np

# Define MTBF and restoration time
mtbf = 500 # hours
restoration_time = 10 # hours

# Define the number of years
years = 20

# Calculate the number of hours in 20 years
total_hours = years * 365 * 24

# Generate a random number of failures for each server
failures = np.random.exponential(scale=mtbf, size=2 * int(total_hours / mtbf))

# Initialize dictionaries for failure and restoration times
failure_times = {'Server': [], 'Failure Time': []}
restoration_times = {'Server': [], 'Restoration Time': []}

# Loop through each failure to calculate the failure and restoration times
server = 1
failure_time = 0
restoration_time_count = 0
for i in range(len(failures)):
    failure_time += failures[i]
    if failure_time >= total_hours:
        break
    failure_times['Server'].append(server)
    failure_times['Failure Time'].append(failure_time)
    restoration_time_count += restoration_time
    restoration_times['Server'].append(server)
    restoration_times['Restoration Time'].append(failure_time + restoration_time_count)
    server = 2 if server == 1 else 1

# Convert the times from hours to years
#for i in range(len(failure_times['Failure Time'])):
 #   failure_times['Failure Time'][i] = failure_times['Failure Time'][i] / (365 * 24)
 #   restoration_times['Restoration Time'][i] = restoration_times['Restoration Time'][i] / (365 * 24)

print("Failure times:")
print(failure_times)

print("Restoration times:")
print(restoration_times)
