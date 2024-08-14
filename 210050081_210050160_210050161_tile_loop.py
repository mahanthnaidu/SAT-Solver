### TEAM MEMBERS
## MEMBER 1: <210050081>
## MEMBER 2: <210050160>
## MEMBER 3: <210050161>

from z3 import *
import sys

file = sys.argv[1]
with open(file) as f:
	n,T = [int(x) for x in next(f).split()]
	matrix = []
	for line in f:
		matrix.append([int(x) for x in line.split()])

vars = [[[Int("p_{}_{}_{}".format(i,j,l)) for l in range(T+1)] for j in range(n)] for i in range(n)]

s = Solver()

for i in range(n):
	for j in range(n):
		s.add(vars[i][j][0] == matrix[i][j])

for i in range(n):
    for j in range(n):
        s.add(vars[i][j][T] == n*i+j+1)

t1 = [Int("t1_{}".format(l)) for l in range(T)]
t2 = [Int("t2_{}".format(l)) for l in range(T)]
m = [Int("m_{}".format(l)) for l in range(T)]

for t in range(T):
    r = []
    r1 = [Int("r_{}".format(l)) for l in range(T)]
    for i in range(n):
        x1 = vars[i][0][t]
        condition1 = True
        for y in range(0, n - 1):
            condition1 = And(condition1,vars[i][y][t+1] == vars[i][y + 1][t])
        condition1 = And(condition1,vars[i][n-1][t+1] == x1,r1[t]==i)
        for x in range(n):
            for z in range(n):
                if x!=i:
                    condition1 = And(condition1,vars[x][z][t+1] == vars[x][z][t])
        p1 = (And(And(t1[t]==0,t2[t]==0,m[t]==0),condition1))

        x2 = vars[i][n - 1][t]
        condition2 = True
        for y in range(1, n):
            condition2 = And(condition2,vars[i][y][t+1] == vars[i][y - 1][t])
        condition2 = And(condition2,vars[i][0][t+1] == x2,r1[t]==i)
        for x in range(n):
            for z in range(n):
                if x!=i:
                    condition2 = And(condition2,vars[x][z][t+1] == vars[x][z][t])
        p2 = (And(And(t1[t]==0,t2[t]==1,m[t]==0),condition2))

        x3 = vars[n - 1][i][t]
        condition3 = True
        for y in range(1, n):
            condition3 = And(condition3,vars[y][i][t+1] == vars[y - 1][i][t])
        condition3 = And(condition3,vars[0][i][t+1] == x3,r1[t]==i)
        for x in range(n):
            for z in range(n):
                if x!=i:
                    condition3 = And(condition3,vars[z][x][t+1] == vars[z][x][t])
        p3 = (And(And(t1[t]==1,t2[t]==0,m[t]==0),condition3))

        x4 = vars[0][i][t]
        condition4 = True
        for y in range(0, n - 1):
            condition4 = And(condition4,vars[y][i][t+1] == vars[y + 1][i][t])
        condition4 = And(condition4,vars[n - 1][i][t+1] == x4,r1[t]==i)
        for x in range(n):
            for z in range(n):
                if x!=i:
                    condition4 = And(condition4,vars[z][x][t+1] == vars[z][x][t])
        p4 = (And(And(t1[t]==1,t2[t]==1,m[t]==0),condition4))

        condition5 = True
        for x in range(n):
            for z in range(n):
                condition5 = And(condition5,vars[z][x][t+1] == vars[z][x][t])
        p5 = (And(m[t]==1,condition5,r1[t]==i))

        r.append(And(Or(p1,p2,p3,p4,p5),PbEq([(p1,1),(p2,1),(p3,1),(p4,1),(p5,1)],1)))
    s.add(Or(r))  
    s.add(PbEq([(d,1) for d in r],1)) 


# Set s to the required formulae
x = s.check()
print(x)
if x == sat:
    model = s.model()
    for i in range(T):
        if model[m[i]]==0:
            if model[t1[i]]==0 :
                if model[t2[i]]==0:
                    print(str(model[r1[i]])+'l')  
                else:
                    print(str(model[r1[i]])+'r') 
            else:
                if model[t2[i]]==0:
                    print(str(model[r1[i]])+'d')  
                else:
                    print(str(model[r1[i]])+'u') 
        else:continue


	# Output the moves
