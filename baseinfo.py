#!/usr/bin/python
'''
record your infomathon
'''
import Time

deadline = Time.current_time()
dic =  '{"scope":"xxx","deadline":%d}' %deadline
ak = 'xxxxxx'
sk = 'xxxxx' 
Block_Size = 4194304
Chunk_Size = 1048576
filename = 'xxxx'
