def calculate_average(total_sum, count):
    # This will cause a ZeroDivisionError if count is 0
    average = total_sum / count
    return average

def process_data():
    data = []
    total = sum(data)
    # The count will be 0 here since the data list is empty
    count = len(data)
    
    result = calculate_average(total, count)
    print(f"The average is: {result}")

if __name__ == "__main__":
    process_data()
