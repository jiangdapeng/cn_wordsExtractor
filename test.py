#! /usr/bin/env python
#coding=utf-8
import wordextractor
stopwords=['的','是']
stopwords = [word.decode('utf-8') for word in stopwords]
e=wordextractor.Extractor(stopwords)
e.extract("我们是中国人，中国人是讲道理的，我们理智的对待每一件事情".decode('utf-8'))
e.filter(0.01, 0, 0)
w=e.topKwords(10)
for word in w:
    print(word[1].encode('utf-8'))
