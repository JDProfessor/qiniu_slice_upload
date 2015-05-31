#!/usr/bin/python
#
'''
Making 4M block and 1M chunk
'''
import os,baseinfo

def file_size(upload_file):
	return(os.stat(upload_file).st_size)

def count_block(upload_file):
	file_size = os.stat(upload_file).st_size
	if file_size%baseinfo.Block_Size == 0:
		count = file_size/baseinfo.Block_Size
	else:
		count = file_size/baseinfo.Block_Size + 1 
	return count

def block_maker(upload_file):
	with open(upload_file,'rb') as f:
		data = 	True
		while data:
			data = f.read(baseinfo.Block_Size)
			yield data
		
def get_block_size(data):
	return len(data)

def chunk_maker (dataStream):
	length = 0
	datalist = []
	for i in range(baseinfo.Block_Size/baseinfo.Chunk_Size):
		datalist.append(dataStream[length:length+baseinfo.Chunk_Size])
		length = length+baseinfo.Chunk_Size
	return datalist	

def chunk_size (datelist):
	chunkSize = []
	for i in datelist:
		if len(i) > 0:
			chunkSize.append(len(i))
	return chunkSize

def sortdic(ctxdic):
	ctxdic = sorted(ctxdic.iteritems(), key=lambda d:d[0], reverse = False)
	ctx_list = ''
	for key,value in ctxdic:
		ctx_list = ctx_list + value +','
	ctx_list = ctx_list.rstrip(',')
	return ctx_list

