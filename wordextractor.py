#! /usr/bin/env python
#coding=utf-8
"""

"""
from __future__ import division
import math
#import os
#import os.path

special="。，？！（）@\"\'\n\t".decode('utf-8')
SPACE=" ".decode('utf-8')

class Extractor():

    def __init__(self, stopwords, fromfile=False):
        if fromfile is True:
            pass
        else:
            self.stopwords=stopwords

    def extract(self, s, fromfile=False):
        if fromfile is True:
            pass
        else:
            s=self.__prepare(s)
            self.frqs, right=self.__wordfrq(s)
            a, left=self.__wordfrq(s[::-1]) #reverse string
            self.__codegree()              #cohere degree
            self.fd=self.__entropy(right)  #right freedom degree
            lfd=self.__entropy(left)       #left freedom degree
            for word in self.fd:
                self.fd[word] = min(self.fd[word], lfd[word[::-1]])
            total=len(s)
            for word in self.frqs:
                self.frqs[word]/=total
    
    def __prepare(self, s):
        """
        eliminate ，。！？ and so on
        """
        def filter(c):
            if c in special:
                return SPACE
            else:
                return c
        return "".join([filter(c) for c in s])
    
    def __wordfrq(self, s, gramlength=5):
        length=len(s)
        frqs={}
        for i in range(1, gramlength+1):
            for j in range(0, length-i+1):
                #split string to i-gram
                ngram=s[j:j+i]
                if SPACE in ngram:
                    continue
                #print(ngram.encode('utf-8'))
                if ngram in frqs:
                    frqs[ngram]+=1
                else:
                    frqs[ngram]=1
        words=[]
        words.extend(frqs.keys())
        words.sort()
        right={}
        pre=words[0]
        #calculate right-freedom-degree rfd
        for w in words[1:]:
            for i in range(1, len(pre)+1):
                pri=pre[:i]
                if pri not in right:
                    right[pri]={}
                if pri in w:
                    if w[i] not in right[pri]:
                        right[pri][w[i]]=frqs[w]
                    else:
                        right[pri][w[i]]+=frqs[w]
                else:
                    if pre not in right:
                        right[pre]={}
                    break
            pre=w
        right[pre]={} #here be cautious!
        return (frqs, right)
    
    def __entropy(self, neighbor):
        rdf={} #information entropy
        for word in neighbor:
            s=sum(neighbor[word].values())
            rdf[word]=sum([m/s*math.log(s/m) for m in neighbor[word].values()])
        return rdf

    def __codegree(self):
        """
        calculate cohere degree
        """
        cd=[]
        cd.append(lambda s: 1)
        cd.append(lambda s: self.frqs[s]/(self.frqs[s[0]]*self.frqs[s[1]]))
        cd.append(lambda s: min(self.frqs[s]/(self.frqs[s[:2]]*self.frqs[s[2:]]), self.frqs[s]/(self.frqs[s[0]]*self.frqs[s[1:]])))
        cd.append(lambda s: self.frqs[s]/(self.frqs[s[:2]]*self.frqs[s[2:]]))
        cd.append(lambda s: 1)
        self.coheredegree={}
        for word in self.frqs:
            length=len(word)
            self.coheredegree[word]=cd[length-1](word)

    def filter(self, frq, cd, fd):
        self.words=[(self.frqs[word], word) for word in self.frqs if word not in self.stopwords and self.frqs[word]>=frq and self.coheredegree[word]>=cd and self.fd[word] >=fd]
        self.words.sort(None, None, True)

    def topKwords(self, k):
        return self.words[:k]