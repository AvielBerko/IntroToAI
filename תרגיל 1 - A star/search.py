#search
import state
import frontier

def search(n):
    s=state.create(n)
    # print(s)
    f=frontier.create(s)
    while not frontier.is_empty(f):
        s=frontier.remove(f)
        if state.is_target(s):
            return [s, f[1], f[3]]
        ns=state.get_next(s)
        for i in ns:
            frontier.insert(f,i)
    return 0

# print(search(3))

def avg_search(times, n):
    sum_depth = 0
    sum_items = 0

    for i in range(times):
        _, items, depth = search(n)
        sum_depth += depth
        sum_items += items

    avg_depth = sum_depth / times
    avg_items = sum_items / times
    return avg_depth, avg_items

def avg_search_threading(times, n):
    from multiprocessing.pool import ThreadPool

    sum_depth = 0
    sum_items = 0

    with ThreadPool(8) as p:
        result = p.map(search, [n] * times)
        for i in result:
            _, items, depth = i
            sum_depth += depth
            sum_items += items

    avg_depth = sum_depth / times
    avg_items = sum_items / times
    return avg_depth, avg_items
    

print("--- Starting average search of 3 ---")
depth3, items3 = avg_search_threading(100, 3)
print("Average depth", depth3)
print("Average items", items3)

print("--- Starting average search of 4 ---")
depth4, items4 = avg_search_threading(100, 4)
print("Average depth", depth4)
print("Average items", items4)

