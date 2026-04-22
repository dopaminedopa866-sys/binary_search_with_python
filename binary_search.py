arr = [10, 20, 30, 40, 50, 60, 70]
target = 50
left = 0
right = len(arr) - 1
found = False
while left <= right:
    mid = (left + right) // 2
    if arr[mid] == target:
        print("Element found at index :", mid)
        found=True
        break
    elif arr[mid] < target:
        left = mid + 1
    else:
        right = mid - 1

if not found:
    print("Element not found")

