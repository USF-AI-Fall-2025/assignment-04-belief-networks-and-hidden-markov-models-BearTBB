import pandas as pd
import numpy as np

f = open("aspell.txt")
lines = f.readlines()
transition_total = 0
emission_total = 0
transitions = {}
emissions = {}
start_prob = {}

t_rows = ['start', "'", 'N', 'P', 'R', 'S', 'X', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
t_cols =["'", 'N', 'P', 'R', 'S', 'X', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'end']
cols =["'", 'N', 'P', 'R', 'S', 'X', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

df_transition = pd.DataFrame(0.0, [t_rows], columns=t_cols)
df_emission = pd.DataFrame(0.0, [t_cols], columns=t_cols)

for line in lines:
    prev_letter = 'start'
    letter_index = 0
    line = line.strip()
    words = line.split(":")
    correct_word = words[0]
    incorrect_word = words[1]
    incorrect_word = incorrect_word.split(" ")

    max_incorrect_length = 0
    for w in incorrect_word:
        if len(w) > max_incorrect_length:
            max_incorrect_length = len(w)
    max_length = max(len(correct_word), max_incorrect_length)

    for i in range(max_length):
        if i < len(correct_word):
            transitions[(prev_letter, correct_word[i])] = transitions.get((prev_letter, correct_word[i]), 0) + 1
            prev_letter = correct_word[i] if i < len(correct_word) else 'end'
            transition_total += 1
        for word in incorrect_word:
            if i < len(word):
                emissions[(correct_word[i] if i < len(correct_word) else 'end', word[i])] = emissions.get((correct_word[i] if i < len(correct_word) else 'end', word[i]), 0) + 1
                emission_total += 1

    transitions[(prev_letter, 'end')] = transitions.get((prev_letter, 'end'), 0) + 1
    transition_total += 1

print(transitions['c', 'o'])
print(transitions['c', 'u'])
print(emissions['o', 'o'])
print(emissions['u', 'u'])

for (a, b), count in transitions.items():
    df_transition.at[a, b] = count / transition_total

for (a, b), count in emissions.items():
    df_emission.at[a, b] = count / emission_total

print(df_transition['o']['c'])
print(df_transition['u']['c'])
print(df_emission['o']['o'])
print(df_emission['u']['u'])

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    for state in states:
        V[0][state] = start_p[state] * emit_p[obs[0]][state]
        path[state] = [state]

    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for cur_state in states:
            (prob, state) = max(
                [(V[t-1][prev_state] * trans_p[cur_state][prev_state] * emit_p[cur_state][obs[t]], prev_state) for prev_state in states]
            )

            V[t][cur_state] = prob
            newpath[cur_state] = path[state] + [cur_state]

        path = newpath

    (prob, state) = max([(V[-1][state], state) for state in states])
    return (prob, path[state])

def spellcheck(done = False):
    while not done:
        user_input = input("Enter a word to spellcheck (or 'exit' to quit): ")
        if user_input == 'exit':
            done = True
        else:
            user_words = user_input.split(" ")
            for a in df_transition.items():
                start_prob[a[0]] = a[1]['start']

            for word in user_words:
                result = viterbi(word, cols, start_prob, df_transition, df_emission)
                print("Corrected word:", ''.join(result[1]))

spellcheck()