# -*- coding: utf-8 -*-
"""
Created on Tue May  2 15:45:33 2017

@author: thomas
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import time
import random


def selection(toSort):
    start = time.clock(); l = len(toSort); comparison = 0
    for i in range(l):
        swap = False
        curr_min = toSort[i]
        for j  in range(i+1, l):
            if toSort[j] < curr_min:
                curr_min = toSort[j]
                pos_min = j
                swap = True
            comparison += 1

        if swap: toSort[i], toSort[pos_min] = toSort[pos_min], toSort[i]
    t = time.clock() - start
    return {"SortedList": toSort, "Time": t, "Comparisons": comparison}



def insertion(toSort):
    start = time.clock(); l = len(toSort); comparison = 0; swaps = 0
    for i in range(1,l):
        j = i
        while 0 < j and toSort[j] < toSort[j-1]:
            toSort[j], toSort[j-1] = toSort[j-1], toSort[j]
            swaps += 1; j -= 1; comparison += 1

    t = time.clock() - start
    return {"SortedList": toSort, "Time": t, "Comparisons": comparison, "Swaps": swaps}


def bubble(toSort):
    start = time.clock(); l = len(toSort); comparison = 0; count = 0; i = 0
    swapped = True; swaps = 0
    while i < l-1-count:
        swapped = False
        if toSort[i+1] < toSort[i]:
            toSort[i+1], toSort[i] = toSort[i], toSort[i+1]
            swapped = True
            swaps += 1
        i += 1; comparison += 1
        if i == l-1-count and swapped:
            i = 0
            count += 1

    t = time.clock() - start
    return {"SortedList": toSort, "Time": t, "Comparisons": comparison, "Swaps": swaps}

def heap(toSort):
    start = time.clock()
    min_heap = build_heap(toSort)

    for i in range(len(toSort)):
        l = len(min_heap)
        toSort[i] = min_heap[0]
        min_heap[0] = min_heap[l-1]
        del min_heap[l-1]
        check_node_downwards(0, min_heap)

    t = time.clock() - start
    return {"SortedList": toSort, "Time": t}

def build_heap(toSort):
    heap = []
    for i in range(len(toSort)):
        heap.append(toSort[i])
        check_node_upwards(i, heap)
    return heap


def check_node_upwards(node, heap):
    if node == 0: return None
    elif node%2 == 0: prev_node = int(0.5*(node - 2))
    else: prev_node = int(0.5*(node - 1))
    if heap[node] < heap[prev_node]:
        heap[prev_node], heap[node] = heap[node], heap[prev_node]
        check_node_upwards(prev_node, heap)


def check_node_downwards(node, heap):
    if 2*node+1 < len(heap) and 2*node+2 < len(heap):
        if heap[2*node+1] < heap[2*node+2]: min_node = 2*node+1
        else: min_node = 2*node+2
    elif 2*node+1 < len(heap) and 2*node+2 >= len(heap):
        min_node = 2*node+1
    else: return None

    if heap[min_node] < heap[node]:
        heap[min_node], heap[node] = heap[node], heap[min_node]
        check_node_downwards(min_node, heap)


def merge(toSort):
    start = time.clock()
    merger = []
    l = len(toSort)
    for i in range(int(l/2)):
        if toSort[2*i] < toSort[2*i+1]: merger.append([toSort[2*i], toSort[2*i+1]])
        else: merger.append([toSort[2*i+1], toSort[2*i]])
    else:
        if l%2 != 0: merger.append([toSort[l-1]])

    merger = merge_all(merger, l)


    t = time.clock() - start
    return {"SortedList": toSort, "Time": t}

def merge_all(merger, l):
    if len(merger[0]) == l:
        return merger[0]
    new_merger = []
    d = len(merger)
    for i in range(int(d/2)):
        tmp_merger = []
        full1 = True; full2 = True
        while full1 or full2:
            if full1 == False:
                for j in merger[2*i+1]:
                    tmp_merger.append(j)
                full2 = False
            elif full2 == False:
                for j in merger[2*i]:
                    tmp_merger.append(j)
                full1 = False
            elif merger[2*i][0] <= merger[2*i+1][0]:
                tmp_merger.append(merger[2*i][0])
                del merger[2*i][0]
                if len(merger[2*i]) == 0: full1 = False
            else:
                tmp_merger.append(merger[2*i+1][0])
                del merger[2*i+1][0]
                if len(merger[2*i+1]) == 0: full2 = False
        new_merger.append(tmp_merger)
    else:
        if d%2 != 0: new_merger.append([merger[d-1]])

    new_merger = merge_all(new_merger, l)
    return new_merger



if __name__ == "__main__":
    n = 100
#    random.seed(15)
#    toSort = [random.randrange(-10,10) for i in range(n)]
#    print(heap(toSort)["Time"])
    random.seed(15)
    toSort = [random.randrange(-10,10) for i in range(n)]
    start = time.clock()
    sorted(toSort[:])
    print("Timsort: ", time.clock() - start)

    start = time.clock()
    insertion(toSort[:])
    print("Insertion: ", time.clock() - start)

    start = time.clock()
    bubble(toSort[:])
    print("Bubble: ", time.clock() - start)

    start = time.clock()
    heap(toSort[:])
    print("Heap: ", time.clock() - start)

