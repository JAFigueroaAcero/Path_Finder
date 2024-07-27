# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 09:15:22 2021

@author: Juan Antonio
"""
def magnitud(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

def main(nodos,start,end):
    paths = [[start]]
    
    finalpaths = []
    
    while paths != []:
        pathsloc = []
        for n,p in enumerate(paths):
            nc = nodos.copy()
            loc = nc[p[-1]].copy()
            for coord in loc:
                if coord not in p:
                    path = p + [coord]
                    if coord == end:
                        finalpaths.append(path)
                    else:
                        pathsloc.append(path)
        paths = pathsloc  
    lons = []
    for f in finalpaths:
        loc = 0
        for n,m in enumerate(f[1::]):
            loc += magnitud(f[n],m)
        lons.append(loc)
    mlen = min(lons)
    mult = []
    for n,s in enumerate(lons):
        if s == mlen:
            mult.append(finalpaths[n])
    
    print(f'distance: {mlen}')
    print(mult)
    return mult
                
if __name__ == '__main__':
    main()