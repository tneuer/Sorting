#!/home/thomas/anaconda3/bin/python

"""
    # Author : Thomas Neuer (tneuer)
    # File Name : topological_sort.py
    # Creation Date : Don 04 Okt 2018 09:46:07 CEST
    # Last Modified : Sam 06 Okt 2018 15:38:44 CEST
    # Description : Implements a topological sorting algorithm for constraints needed
                for the class "Softwareconstruction" @ UZH in HS18. The specific algorithm is called Kahn's algorithm.

                Please note, that this program is explicitly NOT written in pythonic
                matter, as this program serves as template for the final Eiffel project.
"""
#==============================================================================

import re
import sys

import numpy as np


class Main_mode():
    def __init__(self):
        self.elements = Elements()
        self.constraints = Constraints()
        self.tree = Tree()
        self.show_options("main")

    def main(self):
        while True:
            choice = input("[Main mode] User input: ")

            if choice in ["e", "elements", "1"]:
                print("\nEntering element_mode...\n")
                self.activate_elements_mode()
                self.constraints.update(self.elements)
            elif choice in ["c", "constraints", "2"]:
                print("\nEntering constraint_mode...\n")
                self.activate_constraints_mode()
            elif choice in ["r", "run", "3"]:
                print("\nEntering execution_mode...\n")
                self.activate_execution_mode()
            elif choice in ["l", "list", "4"]:
                self.list()
            elif choice in ["!q", "!quit", "!9"]:
                sys.exit()
            else:
                self.show_options("main")

    def activate_elements_mode(self):
        while True:
            choice = input("[Element mode] User input: ")

            if choice in ["a", "add", "1"]:
                self.elements.add()
            elif choice in ["r", "remove", "2"]:
                removed = self.elements.remove()
                self.constraints.remove(remove=removed)
            elif choice in ["m", "modify", "3"]:
                self.elements.modify()
            elif choice in ["l", "list", "4"]:
                self.elements.list()
            elif choice in ["b", "back", "5"]:
                print("")
                break
            elif choice in ["!q", "!quit", "!9"]:
                sys.exit()
            else:
                self.show_options("element")

    def activate_constraints_mode(self):
        while True:
            choice = input("[Constraint mode] User input: ")

            if choice in ["a", "add", "1"]:
                self.constraints.add(self.elements)
            elif choice in ["r", "remove", "2"]:
                self.constraints.remove()
            elif choice in ["l", "list", "3"]:
                self.constraints.list(self.elements)
            elif choice in ["b", "back", "4"]:
                print("")
                break
            elif choice in ["!q", "!quit", "!9"]:
                sys.exit()
            else:
                self.show_options("constraint")

    def activate_execution_mode(self):
        self.tree.top_sort()

    def list(self):
        print("List of elements:\n")
        self.elements.list()
        print("\nList of constraints:\n")
        self.constraints.list()

    def show_options(self, option):
        if option == "main":
            print("\nFollowing options are possible:\n\t1: e(lements): Enter elements_mode\n\t2: c(onstraints): Enter constraints_mode\n\t3: r(un): Run algorithm\n\t4: l(ist): List elements and constraints\n\t9: !q(uit): Quit program\n")

        elif option == "element":
            print("\nFollowing options are possible:\n\t1: a(dd): Enter add_mode\n\t2: r(emove): Enter remove_mode\n\t3: m(odify): Enter modify_mode\n\t4: l(ist): List all elements\n\t5: b(ack): Go to main_mode\n\t!9 !q(uit): Quit program\n")

        elif option == "constraint":
            print("\nFollowing options are possible:\n\t1: a(dd): Enter add_mode\n\t2: r(emove): Enter remove_mode\n\t3: l(ist): List all elements\n\t4: b(ack): Go to main_mode\n\t!9 !q(uit): Quit program\n")


class Elements():
    def __init__(self):
        self.elements = {}

    def add(self):
        while True:
            inpt = input("[Add Element] Element {}: ".format(self.get_length()))
            if inpt in ["!q", "!quit", "!9"]:
                sys.exit()
            elif inpt == "":
                print("")
                break
            elif self.contains(inpt):
                print("Element already added (ignored input).")
            else:
                self.elements[inpt] = []

    def remove(self):
        while True:
            inpt = input("[Remove Element] Element: ")
            if inpt in ["!q", "!quit", "!9"]:
                sys.exit()
            elif inpt == "":
                print("")
                break
            elif self.contains(inpt):
                self.elements.pop(inpt)
                print("Successfully removed element.")
            else:
                message = self.create_message(0).format(inpt)
                print(message)

    def modify(self):
        while True:
            inpt = input("[Modify Element] Element (old->new): ")

            if "->" in inpt:
                e1, e2 = inpt.split("->")
            if inpt in ["!q", "!quit", "!9"]:
                sys.exit()
            elif inpt == "":
                break
            elif "->" in inpt:
                e1 = inpt.split("->")
                e2 = inpt.split("->")[1]
                e1 = inpt.split("->")[0]
                if self.contains(e1):
                    self.elements[e2] = self.elements.pop(e1)
                    print("Successfully modified element.")
                else:
                    message = self.create_message(0).format(inpt)
                    print(message)
            else:
                print("Old and new element need to be separated by an arrow '->'.")

    def list(self):
        print("")
        if self.elements == {}:
            print("Yet no elements added!")
        else:
            for i, e in enumerate(list(self.elements.keys())):
                print("{} : {}".format(i, e))
        print("")

    def get_length(self):
        return len(self.elements)

    def contains(self, e):
        if e in list(self.elements.keys()):
            return True
        else:
            return False

    def add_edge(self, e1, e2):
        if e2 in self.elements[e1]:
            print("Constraint already present (input ignored).")
        else:
            self.elements[e1].append(e2)

    def create_message(self, n):
        if n == 0:
            return ("Element {} not contained. Use 'list' method to see all " +
                    "elements.")


class Constraints():
    def __init__(self):
        self.constraints = []

    def add(self, elements):
        print("\nAvailable elements:")
        elements.list()
        while True:
            inpt = input("[Add Constraint] Constraint {} (a->b): ".format(self.get_length()))
            if inpt in ["!q", "!quit", "!9"]:
                sys.exit()
            elif inpt == "":
                print("")
                break
            elif "->" in inpt:
                e1 = inpt.split("->")
                e2 = inpt.split("->")[1]
                e1 = inpt.split("->")[0]
                if elements.contains(e1) and elements.contains(e2):
                    elements.add_edge(e1, e2)
                else:
                    print("One input not contained in elements.")
            else:
                print("Elements need to be separated by an arrow '->'.")

    def remove(self, remove=None):
        if remove is not None:
            for c in self.constraints:
                for r in remove:
                    if r in c:
                        self.constraints.remove(c)
        else:
            pass

    def list(self, elements):
        for i, c in enumerate(elements.elements.items()):
            print("{} : {}".format(i, c[0], "->", c[1]))

    def get_length(self):
        return len(self.constraints)


class ClassName(object):
     """docstring for ClassName"""
     def __init__(self, arg):
         super(ClassName, self).__init__()
         self.arg = arg
          Tree():
    def __init__(self):
        self.edges = []
        self.outgoing_from_node = {}
        self.incoming_edge_counter = {}

    def top_sort():
        has_no_incoming_edge = []
        for key, value in self.incoming_edge_counter.items():
            if value==0:
                has_no_incoming_edge.append(key)

        L = [] # sorted, will be filled
        while has_no_incoming_edge:
            removed_node = has_no_incoming_edge.pop(0)
            L.append(removed_node)

            outgoing_from_removed_node = self.outgoing_from_node[removed_node]
            for target_node in outgoing_from_removed_node:
                self.incoming_edge_counter[target_node] -= 1
                self.edges.remove([removed_node, target_node])
                if self.incoming_edge_counter[target_node]==0:
                    has_no_incoming_edge.append(target_node)

        if edges: # Check if empty
            raise Value--Error("Cyclic input")
        else:
            print(L)
            pass


main = Main_mode()
main.main()
