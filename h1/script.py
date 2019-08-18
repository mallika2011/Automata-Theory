import json

with open('input.json', 'r') as f:
    data=f.read()

obj=json.loads(data)

#*****************************************PRINTS THE NFA MODEL *****************************************************

print(obj)           


def func (a,stateno):
    arr=[]
    for i in range (0,len(obj['t_func'])):
        if(obj['t_func'][i][1]==a and obj['t_func'][i][0]==stateno):
            # arr.append(obj['t_func'][i][2])
            arr=obj['t_func'][i][2]
    return (arr)

#********************************************CREATING SUBSETS*******************************************************

pset_size=pow(2,obj['states'])
# print(pset_size)

subsets={}
st=[]
relation=[]

for x in obj['letters']:
    relation.append([[],x,[]])

for i in range(0,obj['states']):
    st.append(i)

c=0
i=0

for c in range(0,pset_size):
    sub=[]
    for i in range(0,obj['states']):
        if c & 1<<i:
            sub.append(st[i])
    
    subsets.update({c:sub})

#******************************************************** PRINTING THE SUBSETS ***************************************

print (subsets)                                         
max=pow(2,obj['states']-1)
stateno=0
mark=[]


for i in range(0,pset_size):
    mark.append(0)

mark[0]=1

#*******************************************************INITIAL DFA FOR SINGLETON SETS ************************************   

for i in range(1,max+1):            
    for j in range(0,len(obj['letters'])):
        let=obj['letters'][j]
        # print("Func for   ", let,stateno)
        a=func(let,stateno)
        # print(a)
        relation.append([subsets[i],let,a])
        # print("subsets  ", subsets[i])
    mark[i]=1
    i=i*2
    stateno=stateno+1


# print(mark)
print(relation)

#**************************************************CREATING THE UNION OF THE REMAINING SUBSETS *********************************

for j in range(0,pset_size):
    if(mark[j]==0):
        x=subsets[j]
        for z in range (0,len(obj['letters'])):
            letter=obj['letters'][z]
            union=[]
            for k in range(0,len(x)):
                el=[]
                el.append(x[k])
                # print("Letter is   ", letter, "el is    ", el)
                for c in range(0,len(relation)):
                    if(relation[c][0]==el and relation[c][1]==letter):
                            # print("to be merged ", union, "   ", relation[c][2])
                            union=list(set(union)|set(relation[c][2]))
                    # print("Union is ", union)
                    c=c+1

            relation.append([x,letter,union])
        mark[j]=1
    j=j+1

    
print(relation)

#********************************************** DETERMINING FINAL STATES ***********************************************************

final_states=[]

for i in range(0,len(relation)):
    s=relation[i][2]
    # print("state------",s)
    for j in range(0,len(s)):
        if(s[j] in obj['final'] and s not in final_states):
            final_states.append(s)

copy=final_states
check_copy=[]
for i in range(0, len(final_states)):
    check_copy.append(0)

for i in range(0, len(copy)):
    for j in range(0, len(copy)):
        if(set(copy[i])==set(copy[j]) and i!=j and check_copy[j]!=2 and check_copy[i]!=2):
            # final_states.remove(copy[i])
            check_copy[i]=1
            check_copy[j]=2
            # print(set(copy[i])==set(copy[j]))

final_st=[]

for i in range(0, len(check_copy)):
    if(check_copy[i]!=1):
        final_st.append(final_states[i])

print(final_st)

#****************************************************** CREATING FINAL JSON *********************************************************

finaljson={
    "states":pset_size,
    "letters":obj['letters'],
    "t_func":relation,
    "start":obj['start'],
    "final":final_st
}
print(finaljson)


#*************************************************** WRITING INTO FINAL JSON **********************************************************

with open("output.json",'w') as f2:
    # f2.write(finaljson)
    json.dump(finaljson,f2)

f.close()
f2.close()



        
        





