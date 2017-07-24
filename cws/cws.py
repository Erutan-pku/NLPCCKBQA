# coding=utf-8
# -*- coding: UTF-8 -*- 
"""
Author  : Erutan
Email   : erutan@pku.edu.cn, erutan.pkuicst@gmail.com
GitHub  : https://github.com/Erutan-pku

version : V1.1.2
date    : May 30th, 2017

Python 2.7.10
"""
import codecs
import numpy as np
import sys
import json, re

#cws
class CWS :
    def __init__ (self, wordBankPath=None, wordBank=None) :
        assert any([wordBankPath is None, wordBank is None])
        if all([wordBankPath is None, wordBank is None]) :
            self.wordBank = None
        elif not wordBankPath is None :
            self.wordBank = self.loadLists(wordBankPath, retTypeSet=True)
        else :
            assert type(wordBank) in [list, set]
            self.wordBank = wordBank
    # input
    def loadLists(self, filename, convert=lambda x : x, retTypeSet=False, ignoreFirstLine=False) :
        # 强调区分旧的接口
        assert not convert is None

        inputLines = codecs.open(filename, encoding='utf-8').readlines()
        retList = []
        
        if ignoreFirstLine :
            inputLines = inputLines[1:]
        retList = [convert(line.strip()) for line in inputLines]

        if retTypeSet :
            retList = set(retList)
        return retList
    def getWordSet (self) :
        assert not self.wordBank is None
        return self.wordBank
    """simple rule tools"""
    def MM(self, sentence) :
        assert not self.wordBank is None
        max_n = 20
        start_loc = 0
        wordList = []
        while start_loc < len(sentence) :
            mark_have = False
            for end_loc in range(min(start_loc + max_n, len(sentence)), start_loc + 1, -1) :
                word_t = sentence[start_loc:end_loc]
                if word_t in self.wordBank :
                    wordList.append(word_t)
                    start_loc = end_loc
                    mark_have = True
                    break
            if not mark_have :
                wordList.append(sentence[start_loc])
                start_loc += 1
        wordList = [word for word in wordList if not word == ' ']
        return wordList
    def RMM(self, sentence) :
        assert not self.wordBank is None
        max_n = 20
        start_loc = 0
        wordList = []
        sentence = sentence[::-1]
        while start_loc < len(sentence) :
            mark_have = False
            for end_loc in range(min(start_loc + max_n, len(sentence)), start_loc + 1, -1) :
                word_t = sentence[start_loc:end_loc]
                word_t = word_t[::-1]
                if word_t in self.wordBank :
                    wordList.append(word_t)
                    start_loc = end_loc
                    mark_have = True
                    break
            if not mark_have :
                wordList.append(sentence[start_loc])
                start_loc += 1
        wordList = [word for word in wordList if not word == ' ']
        return wordList[::-1]
    def MWS(self, sentence) :
        assert not self.wordBank is None
        wordList = []
        for i in range(len(sentence)) :
            for j in range(i+1, len(sentence) + 1) :
                word_t = sentence[i:j]
                if word_t in self.wordBank :
                    wordList.append(word_t);
        return wordList
    def segWithCenter(self, sentence, center) :
        assert not self.wordBank is None
        place = sentence.find(center)
        assert place >= 0

        sen_left = self.RMM(sentence[0:place])
        sen_right = self.MM(sentence[place+len(center):])

        sen_words = sen_left + [center] + sen_right
        place_word = len(sen_left)
        return sen_words, place_word
    

if __name__ == '__main__' :
    cws = CWS(wordBankPath='WordBank')
    sentence = u'匈牙利的中央银行的名称是'
    print ' '.join(cws.MWS(sentence))
    print ' '.join(cws.MM(sentence))
    print ' '.join(cws.RMM(sentence))
    print ' '.join(cws.segWithCenter(sentence, center=u'中央银行')[0])