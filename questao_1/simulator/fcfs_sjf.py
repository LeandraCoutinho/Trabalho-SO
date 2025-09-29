import copy

def fcfs(processes):
    # Cria uma cópia para não modificar a lista original
    process_list = sorted(copy.deepcopy(processes), key=lambda p: p.arrival_time)
    
    current_time = 0
    completed_processes = []

    for process in process_list:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        
        process.waiting_time = current_time - process.arrival_time
        
        current_time += process.burst_time
        
        process.completion_time = current_time
        process.turnaround_time = process.completion_time - process.arrival_time
        
        completed_processes.append(process)
        
    return completed_processes


def sjf(processes):
    process_list = copy.deepcopy(processes)
    
    current_time = 0
    completed_processes = []
    
    num_processes = len(process_list)

    while len(completed_processes) < num_processes:
        ready_queue = [p for p in process_list if p.arrival_time <= current_time and p not in completed_processes]
        
        if not ready_queue:
            remaining_processes = [p for p in process_list if p not in completed_processes]
            current_time = min(p.arrival_time for p in remaining_processes)
            continue

        process_to_execute = min(ready_queue, key=lambda p: p.burst_time)
        
        process_to_execute.waiting_time = current_time - process_to_execute.arrival_time
        
        current_time += process_to_execute.burst_time
        
        process_to_execute.completion_time = current_time
        process_to_execute.turnaround_time = process_to_execute.completion_time - process_to_execute.arrival_time
        
        completed_processes.append(process_to_execute)

    return completed_processes