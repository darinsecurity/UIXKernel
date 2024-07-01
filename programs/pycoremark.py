import time

def get_tick():
   try:
      return time.perf_counter()
   except Exception as e:
      return time.ticks_ms()/1000

print("Running PyCoreMark")

start = get_tick()
x = 1
for _ in range(100):
   x += 1
basic_loop_performance = get_tick()-start

start = get_tick()
x = ""
for _ in range(100):
   x += "a"
del x
string_add_performance = get_tick()-start

start = get_tick()

for _ in range(10):
   x = []
   for _ in range(100):
      x.append("a"*50)
   for item in x:
      del item
   del x
mem_alloc_performance = get_tick()-start

total_score = 10/(basic_loop_performance+string_add_performance+mem_alloc_performance)
print("Score: {}".format(total_score))


