import time


def test_func():
    for i in range(100):
        x = i + 5
    return x


if __name__ =="__main__":

    start_time_cpu = time.process_time()
    start_time_gpu = time.perf_counter()

    test_func()

    end_time_cpu = time.process_time()
    end_time_gpu = time.perf_counter()

    duration_cpu = end_time_cpu - start_time_cpu
    duration_gpu = end_time_gpu - start_time_gpu

    print("Duration CPU:", duration_cpu)
    print("Duration GPU:", duration_gpu)
