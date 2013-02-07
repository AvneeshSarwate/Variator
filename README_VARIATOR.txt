CONTENTS
--Objects
--Interface Directions
--Transformation API
	phrase Module
	comp Module
--Known Bugs

-----------------------------Objects---------------------------------
--the PHRASE object:
can be used like a python iterable (implements: set, .append, slice, concatenate, get)  whose elements are tuples of integers (note, time). Has members n - which is the list of notes, and t - which is the listlist of times, 

construction:
#creates an empty phrase
p = phrase.Phrase()

#creates a phrase and sets list1 as the notes list and list2 as the times list 
p = phrase.Phrase(list1, list2)  

#a copy constructor 
p = phrase.Phrase(q)   #where q is another phrase 

--the CHORD object:
(minimally) a list of notes (sorted increasing order), one of which is indicated to be the root. 
has members .root = the root of the chord, and .n = the list of notes in the chord. 

construction:
#creates an empty chord, root set to 0
c = phrase.Chord()

#creates a chord with a list of notes. Root and name arguments optional. Root default set to lowest of notes if root argument not given, name set to empty string if name argument not given
c = phrase.Chord(list, [rootInt, [nameString)

.append(int) - adds note int to the chord (inserts it into chord.n), resorts chord.n 

.invert(int) - method that inverts the chord up or down depending on sign of argument
if int > 0 - increases the lowest note by 12, resorts, resets root value to root + 12 if root is the note increased.
if int < 0 - decreases the highest note by 12, resorts, resets root value to root - 12 if root is the note decreased.

--the PROGRESSION object
a list of chords (pro.c) and a corresponding list of times (prog.t). 

construction:
#creates an empty phrase
prog = phrase.Progression()

.append((chord, time))
adds chord to end of pro.c

----------------------------Interface Directions-------------------------
Directions not included in Variator paper.

When using input method, make sure there are no extra spaces (known bug)

When using input method, Key;Root;Chord Name entry, there must be 2 semicolons to separate all arguments
	EX to insert only a root of 60 - string entered is ";60;"

phrase.play() cannot be called more than once at a time in the code entry 


---------------------------Transformation API-----------------------------
all functions must be called as module.function()

-----------------------phrase module: phrase.func()
--cycle(phrase, int)
Takes a phrase and "cycles" it forwards (notes and times move up one index, last note goes to front) int times if int > 0, or backwards |int| times if int < 0

--cycleN(phrase, int)
Cycles only the note list

--cycleT(phrase, int)
Cycles only the times list

--transpose(phrase, int)
Transposes the phrase up int semitones if int > 0, or down |int| if int < 0

--keyTranspose(phrase, int, keyString)
Transposes the phrase up int scale degrees in the given key if int > 0, or down |int| if int < 0

--retrograde(phrase)
reverses the order of note and time lists

--retrogradeN(phrase)
reverses the order of only notes lists

--retrogradeT(phrase)
reverse the order of only the times list

--inversionN(phrase)
performs an inversion on the phrase

--keyInvert(phrase, keyString)
performs an inversion on the phrase based on the difference in scale degrees of the given scale rather than the reversal of explicit intervals
EX in the key of C:    B -> C is inverted to B -> A, not B -> A# 

--shuffle(phrase)
randomizes the phrase
preserves note-time pairings


-----------------------comp module: comp.func()
--ascend(progression)
inverts the progression so that the top notes of the chords ascend as smoothly as possible 

--descend(progression)
inverts the progression so that the top notes of the chords descend as smoothly as possible 

--findsets(progression, phrase)
finds the indexes of how the notes fit over the chords
EX   sets = findsets(prog, phrase)
sets[i] gives the index of the first note in the phrase that plays over chord i in the progression 

--keychange(phrase, keyString)
changes the key of the phrase to keyString, preserves the mode

--modechange(phrase, keyString)
converts the phrase to the parallel mode keyString of the original key of the phrase. 
if phrase in C major, calling modechange(phrase, "dorian") produces similar phrase in C dorian

--bestchord(phrase)
finds the best single triad that fits over the phrase. returns a chord object

--bestkey(phrase)
returns the keyString for the key that best fits the phrase

--fit(progression, phrase, float)
fits the phrase to the chord progression.
float = 0 does not change the phrase,
float = 1 changes all the notes to chord tones

--melodize(progression, phrase)
revoices the chords in the progression to follow the notes in phrase as closely as possible. 

--rerhythm(phrase, keyString)
rematches the notes and times list of the phrase so that the longest times are matched to the most "important" notes as defined by an inbuilt importance rankning

--blend(phrase, phrase, float)
outputs a mix between the two phrases. A float value of 0 produces the first phrase again, a float value of 1 produces the second value again. 

--lev(iterable, iterable)
helper method to blend, calculates the alignment matrix for the Levenshtein distance between two iterables

--editpath(iterable, iterable)
helper method to blend, returns the list of intermediate values in transforming first iterable to second 


---------------------------Known Bugs-----------------------------------
defining chords in the input window does not work (was functional previously)
blend fails on functions where either notes or times are same
phrases of length 1 do not play properly 
unidentified bug in the melodize method
