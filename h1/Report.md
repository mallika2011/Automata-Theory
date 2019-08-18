# NFA TO DFA CONVERSION 

The python script, script.py, reads an input.json file and convers the NFA thus read in the file into a DFA. 
The obtained DFA is then written into an output.json file.

## Running the Script

The input.json file and the script.py file must be in the same directory. Simply run the script.py file and it will create an ouput.json file with the desired DFA output. 

Use the following command with python3 to run the script 

```bash
python3 script.py
```

## Brief description of an NFA and DFA

Consider an NFA 
    N  =  <   Q<sub>n</sub>,    q<sub>n</sub>,    Σ<sub>n</sub>,    δ<sub>n</sub>  :  Q<sub>n</sub>  x  Σ<sub>n</sub>  -->  Q<sub>n</sub>,   F<sub>n</sub>   >

And its equivalent DFA
    D  =  <   Q<sub>d</sub>,   q<sub>d</sub>,   Σ<sub>d</sub>,   δ<sub>d</sub>,   F<sub>d</sub>     >

Then the following relations exist:
- Q<sub>d</sub>=2<sup>Q<sub>n</sub></sup> (Power set of Q<sub>n</sub>)
- q<sub>d</sub>=q<sub>n</sub>
- Σ<sub>d</sub>=Σ<sub>n</sub>


## Procedure of Conversion (CODE)

* Once the input file is read and the number of states in the NFA are known, the program creates the power set of Q<sub>n</sub>
```python
for c in range(0,pset_size):
    sub=[]
    for i in range(0,obj['states']):
        if c & 1<<i:
            sub.append(st[i])
    
    subsets.update({c:sub})
```

The subsets are formed as per this rule:
If there are "p" states in the NFA, then in the binary representation of each number of a state, namely q<sub>n0</sub>,q<sub>n1</sub>,...,q<sub>n(p-1)</sub>, the bits that are high indicate those states that are a part of a particular state in the DFA.
For eg:
    If there are 2 states in the NFA, then for q<sub>3</sub> binary representation is 11. 
    Hence the state in the DFA will be {q<sub>n0</sub>, q<sub>n1</sub>}

* Next is the creation of the transition relation (or function) for the DFA. We begin by first including all the singleton set elements of the set Q<sub>d</sub> and using the "t_func" of the NFA, we determine their relation in the DFA. 

```python 
for i in range(1,max+1):            
    for j in range(0,len(obj['letters'])):
        let=obj['letters'][j]
        a=func(let,stateno) #func returns the value on parsing "tfunc" from the input file.
        relation.append([subsets[i],let,a])
    mark[i]=1 #used for other parts in the program.
    i=i*2
    stateno=stateno+1
```

* Once all the singleton set elements are covered, the relations for the remaining elements of Q<sub>d</sub> for each input alphabet of Σ can be found by simply taking the union of the results of their individual elements of the set. 


* To determine the final states of the DFA, let R be a collection of states q.
Then 
            F={R ∈ Q<sub>d</sub> | ∃ q ∈ R ⋂ F<sub>n</sub>}   ----- (1)

Therefore first all the elements of F<sub>n</sub> are added to the set of F<sub>d</sub>. Following which all states in Q<sub>d</sub> that satisfy conditon (1) are included (excluding repeat elements)


* Finally the output json is created, integrating all the elements of the DFA Q<sub>d</sub>. This json is then written into the output.json file. 