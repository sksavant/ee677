# Quine-McClusky Implementation
# Written by Savant Krishna "savant.2020@gmail.com"
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
import sys

class QuineMcClusky:
    def __init__(self,filename):
        self.filename=filename #filename passed from main function
        self.vars=0 #no. of variables: to be parsed
        self.minterms=[] #to store the minterms : to be parsed
        self.reducedterms=[] #to store the output reducedterms
        notgotfile=True
        while notgotfile:
            try:
                self.fin=open(self.filename,"r") #open the file
                notgotfile=False
            except IOError:
                print "Cannot open the file! Give another minterms file name!"
                self.filename=raw_input("Filename :")
        self.getminterms()
        self.fin.close()

    def getminterms(self):
        line=self.fin.readline() #read first line
        try:
            assert line[:7]=="vars = "
        except AssertionError:
            print "Not correct format! Need \'vars = <>\'"
            return
        try:
            self.vars=int(line[7:]) #get the no. of variables
        except ValueError:
            print "Not an integer variable number!"
            return
        line=self.fin.readline() #read the next line
        try:
            assert line[:11]=="minterms = "
        except AssertionError:
            print "Not correct format! Need \'minterms = <>\'"
            return
        try:
            self.minterms=map(int,line[11:len(line)-2].split(','))
            for term in self.minterms:
                if term >= 2**self.vars:
                    print "Are they minterms? You need more variables"
                    sys.exit()
            #Eg : minterms = 0,1,2,5,7,8,9,10,13,15,
            #gets the minterms into a list of int
        except ValueError:
            print "Not got integers as minterms! Error!"
            print line[11:len(line)-2].split(',')
            return

    def do_quinemcclusky(self):
        self.reducedterms=[] #reasserting that initially empty
        self.minterms=self.mintermstobinary()
        #this will change minterms to list of lists(minterms: elements being bits) with binary representation
        #Change the representation from integers to bits corresponding to variables

        #After getting the representation, apply the algo.
        #Steps are
        #@1: Find all the primes.
        self.primes=self.findprimes(self.minterms)
        #for e in self.primes:
        #    print e
        #mpm is the matrix of primes and minterms
        #return
        mpm=[[0 for i in range(len(self.primes))] for j in range(len(self.minterms))]
        #To implement the algorithm
        #@2:To do minimisation :
        #   3 steps
        #   @0. Eliminate identical rows (already guaranteed to be non-identical)
        #   @1. Need to definitely have essential primes : Only one element in
        #   column has a mark
        #   @2. Row dominance elimination of dominated row
        #   @3. Column dominace elimination of the dominating row
        #
        for i in range(len(self.minterms)):
            noofcoveringprimes=0
            primeindex=-1
            needtodeleteamintermrow=False
            for j in range(len(self.primes)):
                if self.covers(self.primes[j],self.minterms[i]):
                    if not mpm[i][j]==-1:
                        mpm[i][j]=1
                        noofcoveringprimes=noofcoveringprimes+1
                        primeindex=j
                    else:
                        needtodeleteamintermrow=True
                        break
            if needtodeleteamintermrow:
                for prind in range(len(self.primes)):
                    mpm[i][prind]=-1
            elif noofcoveringprimes==1:
                self.reducedterms.append(self.primes[primeindex])
                #add the essential prime to reducedterms
                #remove that row or col? or make all -1?
                #then what? then check for dominance
                for minind in range(len(self.minterms)):
                    mpm[minind][primeindex]=-1
                for prind in range(len(self.primes)):
                    mpm[i][prind]=-1
        #self.print_mpmmatrix(mpm)
        #Part 2 row dominance? : If a row is dominated by another, discard it
        for i in range(len(self.minterms)):
            for j in range(0,len(self.minterms)):
                if self.rowdominates(i,j,mpm): #returns true is r1 dominates r2 i.e, r1 is one when r2 is one
                    for k in range(len(self.primes)):
                        mpm[j][k]=-1
        #self.print_mpmmatrix(mpm)
        #part 3 column dominance? : If a column dominates another column, discard it
        for i in range(len(self.primes)):
            for j in range(len(self.primes)):
                if self.columndominates(i,j,mpm): #return true is c1 dominates c2 i.e, c1 is one when c2 is one
                    for k in range(len(self.minterms)):
                        mpm[k][i]=-1
        #self.print_mpmmatrix(mpm)
        #All the 3 minimisation techniques done. Now check for any primes left
        for i in range(len(self.primes)):
            for j in range(len(self.minterms)):
                if mpm[j][i]==1:
                    if not self.primes[i] in self.reducedterms:
                        self.reducedterms.append(self.primes[i])

    def columndominates(self,c1,c2,mpm):
        if c1==c2:
            return False
        sum=0
        for i in range(len(self.minterms)):
            sum=sum+mpm[i][c2]
            if mpm[i][c2]==1:
                if mpm[i][c1]!=1:
                    return False
        if sum==-len(self.minterms):
            return False
        return True

    def rowdominates(self,r1,r2,mpm):
        if r1==r2:
            return False
        for i in range(len(self.primes)):
            if mpm[r2][i]==1:
                if mpm[r1][i]!=1:
                    return False
        return True

    def print_mpmmatrix(self,mpm):
        print "matrix"
        line="\t\t"
        for i in range(len(self.primes)):
            print "prime "+str(i)+" "+str(self.primes[i])
            line=line+"p"+str(i)+"\t"
        print line
        for i in range(len(self.minterms)):
            line=str(self.minterms[i][0:self.vars])
            line=line+"\t"
            for j in range(len(self.primes)):
                line=line+str(mpm[i][j])+"\t"
            print line
        print "over"

    def covers(self,prime,minterm):
        for i in range(self.vars):
            if(prime[i]+minterm[i]==1):
                return False
        return True

    def findprimes(self,minterms):
        #The tabular method for finding all the primes
        p=[]
        #To fill in
        self.orderbynumberof1s() #order the minterms
        #iterate through all adjacent minterms and get the those unticked into primes
        loopedthroughall=False
        nextterms=self.minterms
        while(not loopedthroughall):
            next=[]
            for i in range(len(nextterms)):
                notchecked=True
                notprimedyet=True
                for j in range(i,len(nextterms)):
                    if nextterms[i][self.vars]+1==nextterms[j][self.vars]:
                        #no. of ones differ by 1; check if they differ by more than one element
                        if self.do_terms_differ_more_than1(nextterms[i],nextterms[j]):
                            notchecked=False
                            #length of intersection is self.vars-1 implies self.vars-1 are same i.e, only 1 is different
                            nextterms[i][self.vars+1]=True
                            nextterms[j][self.vars+1]=True
                            #Still to get new combined term into the nextterms array
                            x=[]
                            #Add the term with dash -1 in place of _
                            nooofdc=0
                            for k in range(self.vars):
                                if nextterms[i][k]==nextterms[j][k]:
                                    x.append(nextterms[i][k])
                                    if(nextterms[i][k])==-1:
                                        nooofdc=nooofdc+1
                                else:
                                    nooofdc=nooofdc+1
                                    x.append(-1)
                            x.append(sum(x)+nooofdc)
                            x.append(False)
                            if not x in next:
                                next.append(x)
                    elif nextterms[i][self.vars]+1<nextterms[j][self.vars]:
                        if nextterms[i][self.vars+1]==False:
                            notprimedyet=False
                            #I=-1f not merged with any of the one difference ones, it's an essential prime. Append it to the prime list
                            p.append(nextterms[i][0:self.vars])
                            break #breaks out of one for loop or both?
                if notchecked and notprimedyet:
                    if nextterms[i][self.vars+1]==False:
                        p.append(nextterms[i][0:self.vars])
           # print "next"
           # for e in next:
           #     print e
           # print
            if len(next)==0:
                loopedthroughall=True
            else:
                nextterms=next
        #code here
        #print "primes"
        #for e in p:
        #    print e
        return p

    def do_terms_differ_more_than1(self,term1,term2):
        assert len(term1)==len(term2)
        count=0
        for i in range(len(term1)-2): #Ignore the last 2 elements i.e, the no.of ones and checked status
            if not term1[i]==term2[i]:
                count=count+1
        if count==1:
            return True
        return False

    def orderbynumberof1s(self):
        for i in range(len(self.minterms)):
            self.minterms[i].append(sum(self.minterms[i]))
            self.minterms[i].append(False) #not ticked
        self.minterms=sorted(self.minterms, key=lambda x: x[self.vars])

    def mintermstobinary(self):
        newminterms=[]
        #To change self.minterm to bits
        for term in self.minterms: #go through each minterm and find it's binary form
            newminterms.append(self.tobinary(term))
        return newminterms

    def tobinary(self,term):
        binaryterm=[]
        for i in range(self.vars): #finding the binary form of a number representing minterm
            binaryterm.append(term%2)
            term=term/2
        return binaryterm[::-1]

    def print_reduced_terms(self): #used finally to print the reducedterms
        print "The required reducedterms are"
        for e in self.reducedterms:
            print e

    def print_reduced_terms_tofile(self,terms,filename):
        fout=open(filename,"w")
        for e in terms:
            strminterm=""
            for x in reversed(e):
                if not x==-1:
                    strminterm=strminterm+str(x)
                else:
                    strminterm=strminterm+"-"
            strminterm=strminterm+"\n"
            fout.write(strminterm)
        fout.close()

if __name__=="__main__":
    #call a instance of the class QuineMcClusky with the filename of minterms.txt
    qm=QuineMcClusky("minterms.txt")
    #call the do_quinemcclusky method which will compute the reducedterms
    qm.do_quinemcclusky()
    #print the reduceedterms
    #qm.print_reduced_terms()
    qm.print_reduced_terms_tofile(qm.reducedterms,"result.txt")
    qm.print_reduced_terms_tofile(qm.primes,"result_primes.txt")
