from parse import read_input_file, write_output_file
import os
import bisect

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """

    """
    tasks: 
        - task_id (int): task id of the Task [i]
        - deadline (int): deadline of the Task [0 < t < 1440] - length of deadlines restricted
        - duration (int): duration of the Task [0 < d < 60] - duration
        - perfect_benefit (float): the benefit recieved from [0 < p < 100] - profit
        completing the Task anytime before (or on) the deadline
    """


    """
    Pseudocode
    dp approach
    1. sort the jobs by deadline (t) (earliest to latest)
    2. intialize dp [time] = profit (to store maximum profit at time i)
    3. for each task : [id, deadline, duration, profit] 
        if we dont do the task: nothing changes
        if we do the task: ..
    """

    sorted_tasks = sorted(tasks, key = lambda x : x.get_deadline())
    # for t in sorted_tasks:
    #     print(t.get_task_id())
    memo = [[0,0,-1,0]] # time, current max profit, prev_idx, task_id 

    for x in sorted_tasks:
        curr_id = x.get_task_id()
        ddl = x.get_deadline()
        dur = x.get_duration()
        prof = x.get_max_benefit()
        prev_idx = bisect.bisect(memo, [ddl-dur]) - 1
        """
        if max profit at the latest end time before the current task's latest possible start time,
        plus the profit of the current task, is greater than the 
        for example: memo = [0, 0], [3, 20], [5, 30]
        current task (whose end time has to be >=5 because it is sorted):
        - option A: ddl 6, dur 5, profit 100, bisect would search for 1, return index 1-1 = 0, 
            (0 + 100) is greater than the current max profit at the latest end time (30),
            so we append(6, 0+100) -> [6, 100, 0, curr task id] to memo (prev idx)
        - option B: ddl 6, dur 2, profit 5, bisect search for 4, return index 2-1 = 1,
            (20 + 5) is less than the curr max profit at latest time, so we don't do the task
            nothing is appended
        **observation** the profit is strictly increasing  
        """
        if memo[prev_idx][1] + prof > memo[-1][1]:
            memo.append([ddl, memo[prev_idx][1] + prof, prev_idx, curr_id])
        else:
            min_late = dur + memo[-1][0] - ddl
            memo.append([dur + memo[-1][0], memo[-1][1] + x.get_late_benefit(min_late), len(memo) - 1, curr_id])
        """
        check if doing the task late would give profit
        """
        # min_late = dur + memo[-1][0] - ddl
        # memo.append([dur + memo[-1][0], memo[-1][1] + x.get_late_benefit(min_late), len(memo) - 1, curr_id])
    # print(memo[-1])
    
    prev_memo_idx = memo[-1][2]
    igloos_reversed = [memo[-1][3]]
    while(prev_memo_idx != -1):
        prev_memo = memo[prev_memo_idx]
        igloos_reversed.append(prev_memo[3])
        prev_memo_idx = prev_memo[2]

    # print(igloos_reversed)
    igloos_reversed.reverse()
    igloos_reversed.remove(0)

    return igloos_reversed
    # pass

def run_solver(size):
    for input_file in os.listdir('inputs/{}/'.format(size)):
        if size not in input_file:
            continue
        input_path = 'inputs/{}/{}'.format(size, input_file)
        output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
        print(input_path, output_path)
        tasks = read_input_file(input_path)
        output = solve(tasks)
        write_output_file(output_path, output)


if __name__ == '__main__':
    run_solver('small')


# if __name__ == '__main__':
#     tasks = read_input_file("samples/100.in")
#     output = solve(tasks)
#     print(output)
#     # for t in tasks:
#     #     print(t.get_task_id())

# Here's an example of how to run your solver.
# if __name__ == '__main__':
#     for size in os.listdir('inputs/'):
#         if size not in ['small', 'medium', 'large']:
#             continue
#         for input_file in os.listdir('inputs/{}/'.format(size)):
#             if size not in input_file:
#                 continue
#             input_path = 'inputs/{}/{}'.format(size, input_file)
#             output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
#             print(input_path, output_path)
#             tasks = read_input_file(input_path)
#             output = solve(tasks)
#             write_output_file(output_path, output)