keys = [
        ['msg', 'conv', 'hey', 'its', 'hello'], 
        ['msg', 'conv', 'hey', 'thats', 'world'],
        ['msg', 'comm'],
        ['wish', 'happy', 'birthday'],
    ]
d = {}

def createHie(dist, arr):
    for i in range(len(arr)):
        ele = arr[i]
        if ele not in dist:
            dist[ele] = {}
        arr.pop(i)
        dist[ele] = createHie(dist[ele], arr)
        return dist

for i in range(len(keys)):
    d = createHie(d, keys[i])

print(d)

