##add_dependencies=time
class TaskScheduler:
    def __init__(self):
        self.gen_task_dict = {}
        self.task_dict = {}
        self.refresh_ms = 125
        self.accumulated_ms = 0

    def add_task(self, task_func, refresh_hz=None):
        # obtain the generator from the function
        task_gen = task_func()
        
        if self.task_dict.get(task_gen, None) == True:
            return
        task_count = len(self.task_dict)

        if self.accumulated_ms != 0 or task_count != 0:
            avg = self.accumulated_ms / task_count
            alter_ratio = (self.refresh_ms)+(self.refresh_ms+avg)
            
            for task_key, task_value in self.task_dict.items():
                self.task_dict[task_key] *= alter_ratio

        self.task_dict[task_gen] = avg
        self.gen_task_dict[task_func] = task_gen
        

    def remove_task(self, task_func):
        task_gen = self.gen_task_dict.get(task_func,None)
        if task_gen:
            del self.task_dict[task_gen]

    def _refresh(self):
        # clean slate
        for task_key, task_value in self.task_dict.items():
            self.task_dict[task_key] = 0

    def force_refresh(self):
        self._refresh()

    def tick(self):
        start = time.perf_counter()
        func = min(self.time_dict, key=self.time_dict.get)
        next(func)
        end = time.perf_counter() - start
        self.time_dict[func] += end
        self.accumulated_ms += end

        if self.accumulated_ms > self.refresh_ms:
            self._refresh()

        

