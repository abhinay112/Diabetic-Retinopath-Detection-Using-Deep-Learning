arr = [1,1,1,1,0]
n = len(arr)

low = 0
high = n-1
first_occ = None
while low<=high:
    
    mid = (low+high)//2
    
    if arr[mid]==1:
        low = mid+1
    else:
        first_occ = mid
        high = mid - 1
print(first_occ)

low = 0
high = n-1
secound_occ = None
while low<=high:
    
    mid = (low+high)//2
    
    if arr[mid]==1:
        low = mid+1
    else:
        secound_occ = mid
        low = mid + 1
print(secound_occ)
