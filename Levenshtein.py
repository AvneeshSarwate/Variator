'''
Created on Dec 30, 2012

@author: avneeshsarwate

'''

import string
import sys
import phrase
import random

def ascend(prog):
    #print prog
    for i in range(1, len(prog)):
        print str(i) + " " + str(len(prog.c[i]))
        while prog.c[i][len(prog.c[i])-1] >= prog.c[i-1][len(prog.c[i-1])-1]:
            prog.c[i].invert(-1)
            print prog.c[i]
        while prog.c[i][len(prog.c[i])-1] <= prog.c[i-1][len(prog.c[i-1])-1]:
            prog.c[i].invert(1)
    return prog

def descend(prog):
    for i in range(1, len(prog)):
        while prog.c[i][len(prog.c[i])-1] <= prog.c[i-1][len(prog.c[i-1])-1]:
            prog.c[i].invert(1)
        while prog.c[i][len(prog.c[i])-1] >= prog.c[i-1][len(prog.c[i-1])-1]:
            prog.c[i].invert(-1)
    return prog
def findsets(prog, phr):
    
    sets = [0] * len(prog)
  
    ind = 0
    l = 0
    isum = 0
    for i in range(len(prog)):
        l += 1.0 / prog.t[i]
        #isum = 0
        while isum < l:
            isum += 1.0/phr.t[ind]
            ind += 1
#        if isum - 1.0/phr.t[ind] < l:
#            ind += 1
        sets[i] = ind
        
    sets.insert(0, 0)
    
    return sets
    
#KEY CHANGE - shift all notes in phrase down by root notenote of original key, 
#shift up by root note of new key

def keychange(*args):
    
    phr = args[0]
    if(len(args) > 2):
        orig = args[1]
        keystr = args[2]
    else:
        orig = phr.key
        keystr = args[1]
    
    newroot = phrase.roots[string.lower(keystr.split(" ")[0])]
    oldroot = phrase.roots[string.lower(orig.split(" ")[0])]
    
    for i in range(len(phr.n)):
        phr.n[i] - oldroot + newroot
    
    phr.key = keystr
    
    return phr

#MODE CHANGE - take root note of phrase and mod 12 it, subtract this form all notes, then
#based on mod12 comparisons and "mode frameworks" in phrase module, look thru notes in 
#phrase and shift them accordingly

def modechange(phr, keystr):
    
    oldmode = phrase.modes[string.lower(phr.key.split(" ")[1])]
    newmode = phrase.modes[string.lower(keystr.split(" ")[1])]
    ##inclode code to handle scales having different numbers of notes
    
    root = phrase.roots[string.lower(phr.key.split(" ")[0])]
    dif = root%12
    
    degrees = [0] * len(phr)
    
    for i in range(len(phr)):
        phr.n[i] -= dif
        degrees[i] = oldmode.index(phr.n[i]%12)
        phr.n[i] -= oldmode[degrees[i]] + newmode[degrees[i]]
        phr.n[i] += dif
    
    return phr
    
def bestchord(*args): #divs is list of starting points of subphrases, plus last element of length
    #for diatonics only
    
    def rec(mod, root):
            return mod + (root/12) * 12
        
    def score(countsL):
        degweight = []
        degweight.append(3)
        degweight.append(-3)
        degweight.append(1)
        degweight.append(-1)
        degweight.append(2)
        degweight.append(-3)
        degweight.append(0)
            
        cscore = 0
        for i in range(len(degweight)):
            cscore += degweight[i] * countsL[i]
        return cscore
    
    
    phr = args[0]
    keystr = phr.key
    if(len(args) > 1):
        keystr = args[1]
    if(keystr != ""):
        root = phrase.roots[keystr.split(" ")[0]]
        key =[(root+k)%12 for k in phrase.modes[keystr.split(" ")[1]]]
        print "key", key
        scores = {}
        for i in range(len(key)):
            degs = [key[(i+j)%7] for j in range(len(key))]
            counts = [0]*7
            for j in range(len(phr.n)):
                counts[degs.index(phr.n[j]%12)] += 1.0/phr.t[j]
                print counts, i
            scores[score(counts)] = i
        print scores
        ranked = scores.keys()
        ranked.sort(reverse=True)
        bestind = scores[ranked[0]]
        print
        print
        print bestind
        
        a = key[bestind]
        print "a", a, i 
        b = key[(i+3)%len(key)]
        c = key[(i+5)%len(key)]
        r = root
        
        notes = [rec(a, r), rec(b, r), rec(c, r)]
        c = phrase.Chord(notes)
        return c
    else: return "need to specify key"
        
        #recovers original chord note from mod12 note, given root of key
        
def makeprog(keystr, *args): #untested
    prog = phrase.Progression()
    
    rootN = phrase.roots[keystr.split(" ")[0]]
    keynotes = phrase.key(keystr)
    rooti = keynotes.index(rootN) - 1  #-1 because then, root + 1 (for first degree) gives index of first degree
    
    for i in args:
        c = phrase.Chord([keynotes[rooti+i],keynotes[rooti+i+2], keynotes[rooti+i+4]])
        prog.append((c, 4))
    
    return prog        

def makechrdmel(keystr, prog, *args):  #untested
    
    times = [2, 4, 4, 8, 8, 16, 16]
    t = []
    
    if(len(args) == 0):
        sum = 0
        for i in prog.t:
            sum += 1.0/i
        #print sum, "total prog sum"
        while(sum >= 1.0/2):
            t.append(times[random.randint(0, 6)])
            sum -= 1.0/t[len(t)-1]
            #print sum, "sum2"
        while(sum >= 1.0/4):
            t.append(times[random.randint(1, 6)])
            sum -= 1.0/t[len(t)-1]
            #print sum, "sum4"
        while(sum >= 1.0/8):
            t.append(times[random.randint(3, 6)])
            sum -= 1.0/t[len(t)-1]
            #print sum, "sum8"
        while(sum >= 1.0/16):
            t.append(times[random.randint(5, 6)])
            sum -= 1.0/t[len(t)-1]
            #print sum, "sum16"
        n = [i for i in t]
        p = phrase.Phrase(n, t)
    if(len(args) == 1):
        t = args[0].t
        p = args[0]
    
    tsum = [1.0/i for i in t]
    print sum, tsum, "sum compare"
    
    divs = findsets(prog, p)
    keynotes = phrase.key(keystr)
    phsum = 0
    prsum = 0
    n = []
    print keynotes
    print
    for i in range(len(divs)-1):
        root = prog.c[i].root
        rootI = keynotes.index(root) #what if notes in prog really high/low, out of keynotes range?
        #print rootI, "rootI", keynotes[rootI], keynotes[rootI+4]
        prsum += 1.0/prog.t[i]
        for k in range(divs[i], divs[i+1]):
            r = random.randint(rootI, rootI+4)
            #print r, "randIndex", keynotes[r]
            n.append(keynotes[r])
            phsum += 1.0/t[k] 
        if(phsum > prsum): # does not "mix" last note in section if it doesnt overlap, can add that condition here to fix it
            old15 = [j%12 for j in keynotes[rootI:rootI+5]]
            oldnotes = keynotes[rootI:rootI+5]
            root = prog.c[i+1].root
            rootI = keynotes.index(root)
            new15 = [j%12 for j in keynotes[rootI:rootI+5]]
            intersect = []
            for j in range(len(old15)):
                if old15[j] in new15:
                    intersect.append(oldnotes[j]) 
            print "intersect", intersect
            n[len(n)-1] = intersect[random.randint(0, len(intersect)-1)]
    
    p = phrase.Phrase(n, t)
    return p
        
def chordvary(c, keystring):
    chord = phrase.Chord(c)
    
    keynotes = phrase.key(keystring)
    rootI = keynotes.index(chord.root)
    addons = [7, 9, 11, 13]
    numremove = random.randint(2,3)
    for i in range(numremove): #removes 2-3 elements from addons 
        addons.remove(random.choice(addons))
    for i in addons:
        chord.append(keynotes[rootI-1+i])
    inverts = random.randint[-2, 2]
    chord.invert(inverts)
    
    return chord
    
def randfittokey(phrCrd, keystr):
    if(phrCrd.type == "phrase"):
        p = phrase.Phrase(phrCrd)
    if(phrCrd.type == "chord"):
        p = phrase.Chord(phrCrd)
    
    vals = phrase.key(keystr)
    
    for i in range(len(p.n)):
        if(not p.n[i] in vals):
            m = 0
            while not(vals[m] < p.n[i] and p.n[i] < vals[m+1]):
                m += 1
            if(random.choice([True, False])):
                p.n[i] = vals[m]
            else:
                p.n[i] = vals[m+1]
    return p

def morphN(phr, n, *args):  
    p = phrase.Phrase(phr)
    if(len(args) != 0):
        spread = args[0]
    else: spread = 5
    for i in range(n):
        l = random.randint(0, len(phr)-1)
        p.n[l] = random.randint(p.n[l]-spread, p.n[l]+spread) #base spread range on p or phr? p allows for some crazy deviation at high n
    return p 

def morphT(phr, n): 
    p = phrase.Phrase(phr)
    ts = [2, 4, 4, 8, 8, 16, 16]
    for i in range(n):
        l = random.randint(0, len(phr)-1)
        p.t[l] = random.choice(ts) #base spread range on p or phr? p allows for some crazy deviation at high n
    return p

def keymorph(phr, keystr, n, *args): #untested
    keyN = phrase.key(keystr)
    p = phrase.Phrase(phr)
    if(len(args) != 0):
        spread = args[0]
    else: spread = 3
    for i in range(n):
        l = random.randint(0, len(phr)-1)
        print "i,", l
        ind = keyN.index(closestrandinkey(p.n[l], keystr))
        new = random.choice(keyN[ind-spread:ind] + keyN[ind+1:spread+1]) #base spread range on p or phr? p allows for some crazy deviation at high n
        #print p.n[l], new
        p.n[l] = new
    return p 

def closestrandinkey(n, keystr, prob=.5): #untested
    vals = phrase.key(keystr)
    #print "find it in key", n, vals
    if(n in vals):
        return n
    else:
        m = 0
        while not(vals[m] < n and n < vals[m+1]):
            m += 1
        if(random.uniform(0, 1) < prob):
            return vals[m]
        else:
            return vals[m+1]
    

#can morph to ANY key, can weight how much a morph is key based or non key,
#can weight whether a morph is on notes or rhythms, 
#can weight whether a morph is add/remove or replace
#can weight between add or remove 
#time length preserving? (add halves a note, remove adds them) 
def supermorph(phr, n, keystr=None, nORr=1.0, keyORno=0, stableL=1, addP=.5, flatspread=5, keyspread=3): #untested
    if(keystr == None):
        keystr = string.lower(bestkey(phr)) + " major" 
    keyN = phrase.key(keystr)
    ts = [2, 4, 4, 8, 8, 16, 16]
    p = phrase.Phrase(phr)
    for i in range(n):
        ind = random.randint(0, len(p)-1)
        #print "i,", i, ind
        if(random.uniform(0, 1) < nORr):
            #notes
                if(random.uniform(0, 1) < keyORno):
                    #key
                    if(random.uniform(0, 1) < stableL):
                        #stable 
                        p = keymorph(p, keystr, 1, keyspread)
                    else:
                        #add/remove
                        if(random.uniform(0, 1) < addP):
                            #add
                            keyind = keyN.index(closestrandinkey(p.n[ind], keystr))
                            note = random.choice(keyN[keyind-keyspread:keyind+keyspread])
                            time = random.choice(ts)
                            p.insert(ind, (note, time))
                        else:
                            #subtract
                            p.pop(ind)
                else:
                    #nonkey
                    if(random.uniform(0, 1) < stableL):
                        #stable
                        p = morphN(p, 1, flatspread)
                    else:
                        #add/remove
                        if(random.uniform(0, 1) < addP):
                            #add
                            note = random.randint(p.n[ind]-flatspread, p.n[ind]+flatspread)
                            time = random.choice(ts)
                            p.insert(ind, (note, time))
                        else:
                            #subtract
                            p.pop(ind)
        else:
            p = morphT(p, 1)
    return p
 
def bestkey(*args):
    
    if(len(args) == 1):
        phr = args[0]
        pri = mod12majPri
    if(len(args) == 2):
        phr = args[0]
        pri = args[1]
    
    scores = {}
    
    for k in phrase.roots.keys():
        scores[k] = 0
        print k
        notes = [(phrase.roots[k]+i)%12 for i in phrase.modes["major"]]
        print notes
        for i in phr.n:
            if (i%12) in notes:
                scores[k] += 7 - pri[notes.index((i%12))]
    maxk = ""
    maxs = 0
    print scores
    for k in scores.keys():
        if scores[k] > maxs:
            maxs = scores[k]
            maxk = k
    return maxk + " major"

def fit(prog, phr, mix):
    dis = []
    dis.append(1)
    dis.append(6)
    dis.append(2)
    
    sets = findsets(prog, phr)
    
    totalchange = 0 
    for i in range(0, len(sets)-1):
        pfrag = phr.n[sets[i]:sets[i+1]]
        for k in pfrag:
            for j in prog.c[i]:
                if abs(j-k) in dis:
                    totalchange += 1
    
    nchange = int(mix * totalchange)
    
    randbucket = list(range(1, totalchange+1))
    changes = []
    
    #find some way to make it more 
    for i in range(nchange):
        k = random.randint(0, len(randbucket))
        changes.append(randbucket[k])
        randbucket.pop(k)
    
    changeind = 0
    for i in range(0, len(sets)-1):
        pfrag = phr.n[sets[i]:sets[i+1]]
        for k in pfrag: #want k to be index not note 
            for j in prog.c[i]: #could multi count notes
                if abs(j-k) in dis:
                    changeind += 1
                    if changeind in changes:
                        phr.n[sets[i] + k] = onefit(prog.c[i], pfrag[k])
                        
    return phr

    def onefit(chrd, note):
        min = float("inf")
        newnote = 0;
        for i in chrd.n:
            if(abs(note - i) < min):
                min = abs(note-i)
                newnote = i
        return newnote

def melodize(prog, phr):
    
    #split longer chords and revoice?
    
    sets = findsets(prog, phr)
    
    for i in range(len(sets)-1):
        while prog.c[i][len(prog.c[i])-1] > phr.n[sets[i]]:
             prog.c[i].invert(-1)
        while prog.c[i][len(prog.c[i])-1] < phr.n[sets[i]]:
             prog.c[i].invert(1)
        dist1 = abs(prog.c[i][len(prog.c[i])-1] - phr.n[sets[i]])
        prog.c[i].invert(-1)
        dist2 = abs(prog.c[i][len(prog.c[i])-1] - phr.n[sets[i]])
        if(dist1 < dist2):
            prog.c[i].invert(1)
    return prog
 
 
mod12majPri = [0, 4, 2, 3, 6, 5, 1]  

def rerhythm(*args):
    
    #scale degrees-1
    
    phr = args[0]
    keystr = args[1]
    if(len(args) < 3):
        relpri = mod12majPri
    else:
        relpri = args[2] 
    keysplit = keystr.split(" ")
    
    modepri1 = phrase.modes[keysplit[1]]
    modepri = []
    print modepri1
    print "yo"
    for i in range(len(modepri1)):
        modepri.append(modepri1[relpri[i]])
    print modepri
    
    root = phrase.roots[string.lower(keysplit[0])]
    
    modpri = []
    for i in range(len(modepri)):
        modpri.append((modepri[i] + root) % 12)
    print modpri
    
    times = list(phr.t)
    
    #since times are listed as reciprocals of their length
    #sort puts smallest numbers first
    #this doble cancelation puts longest duraations in front 
    times.sort()
    ranks = [0] * len(phr)
    for i in range(len(phr.n)):
        ranks[i] = modpri.index(phr.n[i]%12)
    print ranks
    
    ind = 0
    for i in range(len(modpri)):
        for j in range(len(phr)):
            if ranks[j] == i:
                phr.t[j] = times[ind]
                ind += 1
    
    return phr
                
        

def blend(p1, p2, mix):
    if p1.type != p2.type:
        print "not same type"
        return
    
    if p1.type == "chord":
        steps = editpath(p1, p2)
        i = int(mix * len(steps))
        return steps[i]
    if p1.type == "phrase":
        stepsN = editpath(p1.n, p2.n)
        stepsT = editpath(p1.t, p2.t)
        print stepsN
        print stepsT
        iN = int(mix * len(stepsN))
        iT = int(mix * len(stepsT))
        l = min(len(stepsN[iN]), len(stepsT[iT]))
        p = phrase.Phrase(stepsN[iN][0:l], stepsT[iT][0:l])
        return p

def lev(str1, str2):
    
    d = [[0]* (len(str2)+1) for x in range(len(str1)+1)]
    
    print len(d)
    print len(d[0])
    
    for i in range(len(d)):
        d[i][0] = i
    for i in range(len(d[0])):
        d[0][i] = i
    
    for i in range(1, len(str1)+1):
        for j in range(1, len(str2)+1):
            if(str1[i-1] == str2[j-1]):
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+cost)
    print "distance " + str(d[len(d)-1][len(d[0])-1])
    return d

def editpath(str1, str2):
    
    d = lev(str1, str2)
    
    s1 = list(str1)
    s2 = list(str2)
    print "path"
    print len(s1)
    print len(s2)
    
    i = len(str1)
    j = len(str2)
    
    printout(d)
    
    steps = []
    
    while not (d[i][j] == 0):
        print str(i) + " " + str(j) 
        
        if i == 0:
            a = float("inf")
        else:
            a = d[i-1][j] #deletion
        if j == 0:
            b = float("inf")
        else:
            b = d[i][j-1] #insertion
        if i*j == 0:
            c = float("inf")
        else:
            c = d[i-1][j-1] #substitution if less than {i][j]
        e = min(a, b, c)
        if(e == a and e != c):
            s1 = s1[0:i-1] + s1[i:len(s1)]
            i = i-1
            choice = "up-delete"
       
        if(e == b and e != c and e != a):
            s1 = s1[0:i] + s2[j-1:j] + s1[i:len(s1)]
            j = j-1
            choice = "left-add"
            
        if(e == c):
            
            if(c < d[i][j]):
                s1[i-1] = s2[j-1]
            i = i-1
            j = j-1
            choice = "diag-swap"
        print str(i) + " " + str(j)  + " " + choice
        print "     " + string.join(str(s1))
        steps.append(list(s1))
    
    if(len(steps) == 0):
        steps.append(s1)
    
    return steps
    
def printout(d):
    
    for i in range(len(d)):
        for j in range(len(d[0])):
            sys.stdout.write(str(d[i][j]) + "  ")
        sys.stdout.write("\n\n")


#a = "moombathonesque"
#b = "trickster"
#
#d = lev(a, b)
#g = editpath(a, b)
#
#print g 