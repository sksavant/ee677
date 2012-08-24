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

class QuineMcClusky:
    def __init__(self,filename):
        self.filename=filename #filename passed from main function
        self.vars=0 #no. of variables: to be parsed
        self.minterms=[] #to store the minterms : to be parsed
        self.reducedterms=[] #to store the output reducedterms
        try:
            self.fin=open(filename,"r") #open the file
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
        #To implement the algorithm

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
                            #If not merged with any of the one difference ones, it's an essential prime. Append it to the prime list
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
        for e in self.reducedterms:
            print e


if __name__=="__main__":
    #call a instance of the class QuineMcClusky with the filename of minterms.txt
    qm=QuineMcClusky("../clang/minterms.txt")
    #call the do_quinemcclusky method which will compute the reducedterms
    qm.do_quinemcclusky()
    #print the reduceedterms
    qm.print_reduced_terms()
