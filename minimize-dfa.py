from collections import deque
from tabulate import tabulate


class DFA:
    def __init__(self, states, alphabet, transitions, accepting_states, start_state):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions
        self.accepting_states = set(accepting_states)
        self.start_state = start_state

def minimize_dfa(dfa):
    
    # Step 1: Initialize the partition as the accepting and non-accepting states
    partition = [dfa.accepting_states, dfa.states - dfa.accepting_states]
    print(f"Partition 0: {partition}")
    partition_changed = True
    step = 1

    # Step 2: Repeat until the partition no longer changes
    while partition_changed:
        partition_changed = False
        new_partition = []
        for group in partition:
            if len(group) <= 1:
                new_partition.append(group)
                continue
            # Step 2a: Divide each group into subgroups based on transitions
            subgroups = {}
            for state in group:
                transitions = dfa.transitions[state]
                subgroup_key = tuple(transitions.values())
                if subgroup_key not in subgroups:
                    subgroups[subgroup_key] = set()
                subgroups[subgroup_key].add(state)
            # Step 2b: Add the subgroups to the new partition
            for subgroup in subgroups.values():
                new_partition.append(subgroup)
                if len(subgroup) < len(group):
                    partition_changed = True
        prev_partition = partition
        partition = new_partition
        print(f"Partition {step}: {partition}")
        step += 1
        if partition == prev_partition:
            print("Since current and previous partition are the same, we stop.")
            break
    # Step 3: Build the new DFA using the partition as the states
    new_states = []
    new_accepting_states = set()
    new_transitions = {}
    for group in partition:
        new_state = ",".join(sorted(list(group)))
        new_states.append(new_state)
        for state in group:
            if state in dfa.accepting_states:
                new_accepting_states.add(new_state)
            transitions = dfa.transitions[state]
            for symbol, target_state in transitions.items():
                target_group = None
                for subgroup in partition:
                    if target_state in subgroup:
                        target_group = subgroup
                        break
                if target_group is not None:
                    target_state = ",".join(sorted(list(target_group)))
                if new_state not in new_transitions:
                    new_transitions[new_state] = {}
                new_transitions[new_state][symbol] = target_state
    return DFA(new_states, dfa.alphabet, new_transitions, new_accepting_states, new_states[0])


# Accept input for the DFA
states = input("Enter the states of the DFA, separated by commas: ").split(",")
alphabet = input(
    "Enter the input alphabet of the DFA, separated by commas: ").split(",")
transitions = {}
for state in states:
    transitions[state] = {}
    for symbol in alphabet:
        target_state = input(
            f"Enter the target state for transition {state} --{symbol}--> (enter 'reject' to reject): ")
        if target_state == "reject":
            target_state = None
        transitions[state][symbol] = target_state
accepting_states = input(
    "Enter the accepting states of the DFA, separated by commas: ").split(",")
start_state = input("Enter the start state of the DFA: ")

# Function to print transitions table


def print_transitions_table(dfa):
    # Get the sorted list of states
    states = sorted(list(dfa.states))

    # Initialize the table
    table = [["States"] + list(dfa.alphabet)]

    # Populate the table
    for state in states:
        row = [state]
        for symbol in dfa.alphabet:
            target_state = dfa.transitions[state][symbol]
            row.append(target_state)
        table.append(row)

    # Print the table
    print(tabulate(table, headers="firstrow"))


# Create the DFA object
dfa = DFA(states, alphabet, transitions, accepting_states, start_state)

# Print the original DFA
print("Original DFA:")
print("States:", dfa.states)
print("Alphabet:", dfa.alphabet)
print("Transitions:")
print_transitions_table(dfa)
print("Accepting states:", dfa.accepting_states)
print("Start state:", dfa.start_state)

# Minimize the DFA
min_dfa = minimize_dfa(dfa)
print("---------------------------------------------")
# Print the minimized DFA
print("Minimized DFA:")
print("States:", min_dfa.states)
print("Alphabet:", min_dfa.alphabet)
print("Transitions:")
print_transitions_table(min_dfa)
print("Accepting states:", min_dfa.accepting_states)
print("Start state:", min_dfa.start_state)
