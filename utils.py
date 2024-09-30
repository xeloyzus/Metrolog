
def average_temperature(temperatures):
    n =30
    n_len =len(temperatures)
    if not temperatures:
        return None  # Handle the case where the list is empty
    avg = sum(temperatures) / n_len
    return avg


