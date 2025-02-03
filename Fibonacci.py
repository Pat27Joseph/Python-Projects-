#def fibonacci_to_number(max_num):
    #sequence = [0,1]
    #while sequence[-1] + sequence[-2] <= max_num:
        #sequence.append(sequence[-1] + sequence[-2])
    #return sequence

# Example usuage 
#max_number = int(input("Enter the maximum number: "))
#print(f"Fibonacci sequence up to {max_number}: {fibonacci_to_number(max_number)}")


def fibonacci_to_nth(n):
    if n <= 0:
        return "N must be a positive integer."
    sequence = [0, 1]
    for _ in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]

n = int(input("Enter the Nth number:  "))
print(f"Fibonacci sequence up to {n}th number: {fibonacci_to_nth(n)}")