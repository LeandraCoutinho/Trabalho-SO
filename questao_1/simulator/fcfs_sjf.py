import copy

def fcfs(processes, context_switch_cost: int = 0):
    process_list = sorted(copy.deepcopy(processes), key=lambda p: p.arrival_time)
    
    current_time = 0
    completed_processes = []
    timeline = []
    last_process_finished = False

    for process in process_list:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
            last_process_finished = False
        
        if last_process_finished:
            current_time += context_switch_cost

        process.start_time = current_time
        process.waiting_time = process.start_time - process.arrival_time
        
        current_time += process.burst_time
        
        process.finish_time = current_time
        
        timeline.append({"pid": process.pid, "start": process.start_time, "finish": process.finish_time})
        completed_processes.append(process)
        last_process_finished = True
       
    return completed_processes, timeline


def sjf(processes, context_switch_cost: int = 0):
    process_list = [copy.deepcopy(p) for p in processes]
    
    current_time = 0
    completed_processes = []
    timeline = []
    num_processes = len(process_list)

    while len(completed_processes) < num_processes:
        ready_queue = [
            p for p in process_list 
            if p.arrival_time <= current_time and p not in completed_processes
        ]
        
        if not ready_queue:
            remaining_processes = [p for p in process_list if p not in completed_processes]
            current_time = min(p.arrival_time for p in remaining_processes)
            continue

        if completed_processes:
            current_time += context_switch_cost
            
        process_to_execute = min(ready_queue, key=lambda p: p.burst_time)
        
        process_to_execute.start_time = current_time
        process_to_execute.waiting_time = process_to_execute.start_time - process_to_execute.arrival_time
        
        current_time += process_to_execute.burst_time
        
        process_to_execute.finish_time = current_time

        timeline.append({"pid": process_to_execute.pid, "start": process_to_execute.start_time, "finish": process_to_execute.finish_time})
        completed_processes.append(process_to_execute)

    completed_processes.sort(key=lambda p: p.pid)
    return completed_processes, timeline