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
    timeline = []
    current_time = 0
    process_idx = 0
    num_processes = len(process_list)
    
    last_running_process: Process = None

    while len(completed_processes) < num_processes:
        
        while process_idx < num_processes and process_list[process_idx].arrival_time <= current_time:
            ready_queue.append(process_list[process_idx])
            process_idx += 1

        if not ready_queue:
            if process_idx < num_processes:
                current_time = process_list[process_idx].arrival_time
            else:
                break
            last_running_process = None
            continue

        process = ready_queue.popleft()

        if last_running_process and last_running_process.pid != process.pid:
            current_time += context_switch_cost
            while process_idx < num_processes and process_list[process_idx].arrival_time <= current_time:
                ready_queue.append(process_list[process_idx])
                process_idx += 1

        if process.start_time is None:
            process.start_time = current_time
        
        time_slice = min(quantum, process.remaining_time)
        
        slice_start_time = current_time
        current_time += time_slice
        
        timeline.append({
            "pid": process.pid,
            "start": slice_start_time,
            "finish": current_time
        })

        process.remaining_time -= time_slice
        
        last_running_process = process

        while process_idx < num_processes and process_list[process_idx].arrival_time <= current_time:
            ready_queue.append(process_list[process_idx])
            process_idx += 1
            
        if process.remaining_time == 0:
            process.finish_time = current_time
            process.waiting_time = process.finish_time - process.arrival_time - process.burst_time
            completed_processes.append(process)
            last_running_process = None
        else:
            ready_queue.append(process)

    completed_processes.sort(key=lambda p: p.pid)
    return completed_processes, timeline