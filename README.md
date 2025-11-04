# Belief-Networks-Hidden-Markov-Models
Fall 2025 CS 362/562

I will be using one token for this submission.

My current total as of 11/03/2025 is 2, so I will have 1 left.

## Results of old_carnet.py without KeyPresent
P(!B|!M)  
+-----------------------+----------------+  
| Battery               |   phi(Battery) |  
+=======================+================+  
| Battery(Works)        |         0.6410 |  
+-----------------------+----------------+  
| Battery(Doesn't work) |         0.3590 |  
+-----------------------+----------------+   

P(!S|!R)  
+-------------+---------------+  
| Starts      |   phi(Starts) |  
+=============+===============+  
| Starts(yes) |        0.1313 |  
+-------------+---------------+  
| Starts(no)  |        0.8687 |  
+-------------+---------------+   

P(R|B^G)  
+------------------------+--------------+  
| Radio                  |   phi(Radio) |  
+========================+==============+  
| Radio(turns on)        |       0.7500 |  
+------------------------+--------------+  
| Radio(Doesn't turn on) |       0.2500 |  
+------------------------+--------------+   

P(R|B^!G)  
+------------------------+--------------+  
| Radio                  |   phi(Radio) |  
+========================+==============+  
| Radio(turns on)        |       0.7500 |  
+------------------------+--------------+  
| Radio(Doesn't turn on) |       0.2500 |  
+------------------------+--------------+   

P(R) Does not change.  

P(!I|!M^G)  
+------------------------+-----------------+  
| Ignition               |   phi(Ignition) |  
+========================+=================+  
| Ignition(Works)        |          0.2199 |  
+------------------------+-----------------+  
| Ignition(Doesn't work) |          0.7801 |  
+------------------------+-----------------+   

P(!I|!M^!G)  
+------------------------+-----------------+  
| Ignition               |   phi(Ignition) |  
+========================+=================+  
| Ignition(Works)        |          0.5178 |  
+------------------------+-----------------+  
| Ignition(Doesn't work) |          0.4822 |  
+------------------------+-----------------+   

P(!I) would decrease, because the car not moving has a higher chance to be caused by the not having gas, rather than the ignition failing.  

P(S|R^G)  
+-------------+---------------+  
| Starts      |   phi(Starts) |  
+=============+===============+  
| Starts(yes) |        0.7212 |  
+-------------+---------------+  
| Starts(no)  |        0.2788 |  
+-------------+---------------+   

## Results of old_carnet.py with KeyPresent

P(!B|!M)  
+-----------------------+----------------+  
| Battery               |   phi(Battery) |  
+=======================+================+  
| Battery(Works)        |         0.6612 |  
+-----------------------+----------------+  
| Battery(Doesn't work) |         0.3388 |  
+-----------------------+----------------+   

P(!S|!R)  
+-------------+---------------+  
| Starts      |   phi(Starts) |  
+=============+===============+  
| Starts(yes) |        0.0880 |  
+-------------+---------------+  
| Starts(no)  |        0.9120 |  
+-------------+---------------+   

P(R|B^G)  
+------------------------+--------------+  
| Radio                  |   phi(Radio) |  
+========================+==============+  
| Radio(turns on)        |       0.7500 |  
+------------------------+--------------+  
| Radio(Doesn't turn on) |       0.2500 |  
+------------------------+--------------+   

P(R|B^!G)  
+------------------------+--------------+  
| Radio                  |   phi(Radio) |  
+========================+==============+  
| Radio(turns on)        |       0.7500 |  
+------------------------+--------------+  
| Radio(Doesn't turn on) |       0.2500 |  
+------------------------+--------------+   

P(R) Does not change.  

P(!I|!M^G)  
+------------------------+-----------------+  
| Ignition               |   phi(Ignition) |  
+========================+=================+  
| Ignition(Works)        |          0.3339 |  
+------------------------+-----------------+  
| Ignition(Doesn't work) |          0.6661 |  
+------------------------+-----------------+   

P(!I|!M^!G)  
+------------------------+-----------------+  
| Ignition               |   phi(Ignition) |  
+========================+=================+  
| Ignition(Works)        |          0.5280 |  
+------------------------+-----------------+  
| Ignition(Doesn't work) |          0.4720 |  
+------------------------+-----------------+   

P(!I) would decrease, because the car not moving has a higher chance to be caused by the not having gas, rather than the ignition failing.  

P(S|R^G)  
+-------------+---------------+  
| Starts      |   phi(Starts) |  
+=============+===============+  
| Starts(yes) |        0.5216 |  
+-------------+---------------+  
| Starts(no)  |        0.4784 |  
+-------------+---------------+   

P(!K|!M)  
+-----------------+-------------------+  
| KeyPresent      |   phi(KeyPresent) |  
+=================+===================+  
| KeyPresent(yes) |            0.6604 |  
+-----------------+-------------------+  
| KeyPresent(no)  |            0.3396 |  
+-----------------+-------------------+   

## Reflection

### Give an example of a word which was correctly spelled by the user, but which was incorrectly “corrected” by the algorithm.
"RSX" was incorrectly corrected to "zzz".

### Why did this happen?
The word "RSX" was corrected to "zzz" beacause there was no emission data of "R" showing as an "R", and only had data being observed as an "r".
This applies to all the letters that are present in "RSX". They have only emitted as their lowercase versions, and because of this, their emission
probabilities into themselves was 0. The viterbi algortihm that I implemented does not have a way to correctly handle edge cases where all possible
corrections have a zero probability. Instead, it gives the letter that is at the end of the two-dimensional matrix, which just happens to be a "z".
If I were to rewrite the code, I would most likely just handle cases where all possible corrections have a probability of zero to return the unknown word.
I will keep it this way so that it is easily identifiable when a word has corrections with all possible probabilities equal to zero.

### Give an example of a word which was incorrectly spelled by the user, but which was still incorrectly “corrected” by the algorithm.
"abouy" was incorrectly corrected to "abory"

### Why did this happen?
This particular incorrect correction happened because of a very particular coincidence in the transition probability data of "o" to "r" and "o" to "u".
The transition probability for both transitions happened to be the same, with a floating value of 0.006329113924050633. Because of this, the algorithm would
pick the best path based on the emission probability, and  it just so happens that "r" is more often emitted as itself that "u", which is why the algorithm thought
that "r" was the most likely next letter.

Emission probability of "r" observed as "r": 0.04130280859098419
Emission probability of "u" observed as "u": 0.02242152466367713

In order to verify this, I did a rudimentary check on the number of "r" and "u" that show up in the corpus as themselves, and it just so happens that
"u" does show up less than "r", with "u" totalling at 95 instances where it is observed as itself, and "r" totalling at 175.
The subsequent letters after the incorrect prediction is then much more likely to give an incorrect prediction,
as the probability that it gave for t-1 is already erroneous.

### Give an example of a word which was incorrectly spelled by the user, and was correctly corrected by the algorithm.
"cumbo" was correctly corrected to "combo"

### Why was this one correctly corrected, while the previous two were not?
The main reason it differs from the first example is the fact that it has a possibility that has probability more than zero. This already guarantees a result.
The main reason it differs from the second example is that it involves no letters that have the same transition probability as its expected corrected letter.

More on the way it differs for the second example, the only real place that the algorithm could fail is the transition from "c" to "u", where the algorithm
had to notice that the letter "u" was incorrect, and needs to be corrected to "o". Let's take a look at the transition and emission probabilities for this instance.

Emission probability of "c" transitioning to "o": 0.009737098344693282
Emission probability of "c" transitioning to "u": 0.0029211295034079843
Emission probability of "o" observed as "o": 0.04035874439461883
Emission probability of "u" observed as "u": 0.02242152466367713

As you can see, there are no similar probabilities here that can confuse the algorithm like it did in the second example, and it is quite obvious that
"c" transitioning to "o" * "o" observed as "o" would give a larger result, which would result in it being picked.

Other than the above mentioned reasons, this particular observed word does not have many letters in it that are different from the correct word, nor does it differ in length.
Because of the minimized amount of differences between both words, the algorithm has an easier time correcting the word.

### How might the overall algorithm’s performance differ in the “real world” if that training dataset is taken from real typos collected from the internet, versus synthetic typos (programmatically generated)?
The biggest difference that using "real world" data could have as opposed to synthetic typos is that the algorithm could potentially develop its own biases on the words it will and
will not correct. Not all typos are created equal, and a lot of the typos that humans make quite heavily depend on a few factors, the biggest of which are the proximity of the letters
to each other on the typing instrument that a person uses. A person is more likely to typo an "o" to a "p" rather than to a "g" for example, because "o" is right next to "p", whereas
"g" is quite far away in the middle of the keyboard. This heavily affects the emission probabilities for many letters, and we will start to see a trend in the emissions, where
the distribution is concentrated on their location. A synthetic typo probably does not take this into account, and gives purely random typos as training data. This would give a somewhat even, but un-natural, distribution of data, which should make it harder to correct typos.

Another big difference would be in terms of vernacular. The internet is filled with slang, and what is considered a typo in the english language is not entirely a typo on the internet.
For example, someone saying "lol" would not really make much sense when you try to look for it in the dictionary, but it has its own meaning on the internet.
The model would need to be able to understand context quite well, because someone writing "u" could mean "you" but can also be a typo when they wanted to write "i", for example,
which are incredibly likely scenarios. Of course, if internet language is static, we could just update the "dictionary" of internet words, to keep track of the
vernacular of the internet, but the words that people use are ever-evolving. What could be considered a typo today could be a deliberate way to communicate tomorrow,
and this makes static models less useful much more quickly if it cannot learn constantly.

## References:
Pseudocode from slides:

M[t,s] = 0
Backpointers[t,s] = 0 # this will keep our path to the best previous state.
\#\# set up the initial probabilities from the start state (states[0] to observation 1.
\#\# T is the transition probabilities, E is the emission probabilities, O is the vector of observations.
for s in state_values :
M[1,s] = T[states[0], s] * E[s, O[1]]
\#\# the probability of that state * the probability of that state given observation 1.
for o in observations : ## for each time step
for s in state_values : ## for each possible hidden state
al = max[ M[state2, o-1] * T[state2, s] *p(s, o) for state2 in state_values ].
\#\# look at the likelihood of the sequence so far, times T, times the likelihood of that state, given the observation.
M[s,o] = val
Backpointers[s,o] = index(val)
list = []
Best = max(M[t,:]). #find the most likely state for time t
for o in observations.reverse : # work backwards through time to the initial state
list.push(best)
best = backpointers[best, o] ## from this best state, what was the most likely state?
return list