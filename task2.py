def binary_search_min_ge(arr, target):
    left, right = 0, len(arr) - 1
    iteration = 0
    min_ge = None
    while left <= right:
        mid = (left + right) // 2
        iteration +=1
        
        if arr[mid] >= target:
            min_ge = arr[mid]
            right = mid - 1
        else:
            left = mid + 1
    return (iteration, min_ge)


arr = [1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 7.8]
target = 4.0
result = binary_search_min_ge(arr, target)
print(f"Ітерацій: {result[0]}, мінімальне значення >= {target}: {result[1]}")