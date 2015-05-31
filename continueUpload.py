#!/usr/bin/python

import mkblock,upload_block,tkproductor,baseinfo

def protect_bk(filename,blocknum,num,ctx,ctxdic,offset):
	bklist = []
	bklist.append((filename,blocknum,num,ctx,ctxdic,offset))
	with open('bkpoint.txt','a') as f:
		f.write('%s\n'%str(bklist))
		f.flush 

def get_bk():
	with open('bkpoint.txt','r') as f1:
		bk = eval(f1.readline())
	for filename,blocknum,num,ctx,ctxdic,offset in bk:
		pass		
	return filename,blocknum,num,ctx,ctxdic,offset

if __name__ == '__main__':
	filename,blocknum,num,ctx,ctxdic,offset = get_bk()
	input_data = mkblock.block_maker(filename)
	token = 'UpToken '+tkproductor.present_token
	for i in range(blocknum-1):
		input_stream = input_data.next()
	if num != 0:
		input_stream = input_data.next()
		datalist = mkblock.chunk_maker (input_stream)
		contentLen = mkblock.chunk_size(datalist)[num]
		num = num -1
		while baseinfo.Block_Size/baseinfo.Chunk_Size - num -1 >0  :
			ctx,offset,ctxdic,num = upload_block.upload_chunk(filename,blocknum,num,datalist,ctxdic,offset,ctx)
	else :
		blocknum = blocknum -1
	while (blocknum < mkblock.count_block(filename)):
		num = 0
		blocknum = blocknum + 1
		input_stream = input_data.next()
		ctx,offset,datalist,block_size = upload_block.upload_block(filename,blocknum,input_stream)
		while num < baseinfo.Block_Size/baseinfo.Chunk_Size -1 :
			ctx,offset,ctxdic,num = upload_block.upload_chunk(filename,blocknum,num,datalist,ctxdic,offset,ctx)		

	upload_block.make_file(filename,ctxdic)
