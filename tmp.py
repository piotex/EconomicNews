import time


def wait_for_element(max_wait_time_s: float):
    max_wait_time_s *= 100
    for time_s in range(1, int(max_wait_time_s), 1):
        time.sleep(1/100)

def wait_for_element_mm(max_wait_time_s: float):
    start_time = time.time()
    wait_for_element(max_wait_time_s)
    end_time = time.time()
    total_s = end_time - start_time
    total_m = int(total_s / 60)
    total_s = int(total_s - total_m * 60)
    print(f"")
    print(f"#####################################")
    print(f"Total time: {total_m}m {total_s}s")
    print(f"#####################################")


wait_for_element_mm(1)
wait_for_element_mm(0.3)
wait_for_element_mm(13)


