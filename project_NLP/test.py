# -*- coding: utf-8 -*-
from konlpy.tag import Twitter

tw = Twitter()

a = tw.pos("안녕하세요. 여기는 카페입니다.")
print(a)
