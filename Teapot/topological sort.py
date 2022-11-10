repeaters, redstone = map(int, input().split())


wiring = {}
vis = {}
stack = []

for i in range(redstone):
    a, b = input().split()
    vis[a], vis[b] = False, False
    if a in wiring:
        wiring[a] += [b]
    else:
        wiring[a] = [b]

def topoSort(node):
    #print("travelled to node " + str(node))
    vis[node] = True
    if node in wiring:
        for n in wiring[node]:
            if not vis[n]:
                topoSort(n)

    print("pushed node " + str(node))
    stack.insert(0, node)



topoSort(next(iter(wiring)))

for repeater in wiring:
    if not vis[repeater]:
        topoSort(repeater)
        
print(stack, list(reversed(stack)))
