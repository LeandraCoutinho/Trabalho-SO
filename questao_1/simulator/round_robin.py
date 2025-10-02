
import copy
from collections import deque
from typing import List

from .models import Process 

def round_robin(processes: List[Process], quantum: int, context_switch_cost: int) -> List[Process]:
    """
    Simula o algoritmo de escalonamento Round Robin (RR) preemptivo.
    """
    
    process_list = sorted(copy.deepcopy(processes), key=lambda p: p.arrival_time)
    
    ready_queue = deque()
    completed_processes = []
    current_time = 0
    process_index = 0
    running_process = None
    
    while len(completed_processes) < len(process_list):
        while process_index < len(process_list) and process_list[process_index].arrival_time <= current_time:
            ready_queue.append(process_list[process_index])
            process_index += 1
        
        if running_process is None and ready_queue:
            process_to_run = ready_queue.popleft()

            if current_time > 0 and (process_to_run.remaining_time < process_to_run.burst_time):
                current_time += context_switch_cost

                while process_index < len(process_list) and process_list[process_index].arrival_time <= current_time:
                    ready_queue.append(process_list[process_index])
                    process_index += 1
            
            if process_to_run.start_time is None:
                process_to_run.start_time = current_time
            
            running_process = process_to_run
            
        if running_process is None:
            if process_index < len(process_list):
                current_time = process_list[process_index].arrival_time
                continue
            else:
                break 
       
        time_to_execute = min(quantum, running_process.remaining_time)
        
        current_time += time_to_execute
        running_process.remaining_time -= time_to_execute
        
        while process_index < len(process_list) and process_list[process_index].arrival_time <= current_time:
            ready_queue.append(process_list[process_index])
            process_index += 1
        
        if running_process.remaining_time == 0:
            running_process.finish_time = current_time
            running_process.turnaround_time = running_process.finish_time - running_process.arrival_time
            completed_processes.append(running_process)
        else:
            ready_queue.append(running_process)
            
        running_process = None

    return sorted(completed_processes, key=lambda p: p.pid)