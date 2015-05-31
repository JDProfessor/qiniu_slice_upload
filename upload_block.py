#!/usr/bin/python
#
import sys,httplib,urllib,mkblock,tkproductor,continueUpload,baseinfo

httpClient = None
ctxdic = {}
num = 0

class req_block:
	def __init__(self,reqType,reqSize,contentLen,first_datalist):
		self.contentLen = contentLen
		self.params = first_datalist
		self.headers = {"Host":"upload.qiniu.com",
						"Content-type"  : "application/octet-stream",
						"Content-Length":  self.contentLen,
						"Authorization" :  'UpToken '+tkproductor.present_token}
		self.req_config = '/%s/%d'%(reqType,reqSize)
	def blockUpload(self):
		self.httpClient = httplib.HTTPConnection("upload.qiniu.com")
		self.httpClient.request("POST", self.req_config, self.params, self.headers)

	def finalResponse(self):
		self.response = self.httpClient.getresponse()
		print self.response.status
		print self.response.reason
		self.back_str = eval(self.response.read())

	def getMessage(self):
		self.ctx = self.back_str["ctx"]
		self.offset = self.back_str["offset"]
		return self.ctx,self.offset

class req_chunk(req_block):
	def __init__(self,reqType,reqSize,ctx,contentLen,datalist):
		req_block.__init__(self,reqType,reqSize,contentLen,datalist)
		self.ctx = ctx
		self.chunk_config = '/%s/%s/%d'%(reqType,self.ctx,reqSize)
	
	def chunkUpload(self):
		self.httpClient = httplib.HTTPConnection("upload.qiniu.com")
		self.httpClient.request("POST", self.chunk_config, self.params, self.headers)


class req_makefile(req_block):
	def __init__(self,reqType,reqSize,params,contentLen,filename):
		self.headers = {"Host":"upload.qiniu.com",
                        "Content-type"  : "text/plain",
                        "Content-Length":  contentLen,
                        "Authorization" :  'UpToken '+tkproductor.present_token}
		self.req_config = '/%s/%d/key/%s'%(reqType,reqSize,tkproductor.base_64(filename))
		self.params = params
	
	def mkfileUpload(self):
		self.httpClient = httplib.HTTPConnection("upload.qiniu.com")
		self.httpClient.request("POST", self.req_config, self.params, self.headers)

	def finalResponse(self):
		self.response = self.httpClient.getresponse()
		print self.response.status
		print self.response.reason
		print self.response.read()

def upload_block(filename,blocknum,input_stream):
	try:
		ctx = None
		offset = None
		block_size = mkblock.get_block_size(input_stream)
		datalist = mkblock.chunk_maker (input_stream)
		contentLen = mkblock.chunk_size(datalist)[0]
		reqblock = req_block('mkblk',block_size,contentLen,datalist[0])
		print 'block number : %s  chunk number :1' %blocknum
		reqblock.blockUpload()
		reqblock.finalResponse()
		(ctx,offset) = reqblock.getMessage()
		mkblock.chunk_size(datalist)[1]
	except IndexError :
		ctxdic[blocknum] = ctx
	except:
		continueUpload.protect_bk(filename,blocknum,num,ctx,ctxdic,offset=None)
		sys.exit(1)
	return ctx,offset,datalist,block_size

def upload_chunk(filename,blocknum,num,datalist,ctxdic,offset,ctx):
	try:
		num = num+1
		contentLen = mkblock.chunk_size(datalist)[num]
		reqchunk = req_chunk('bput',offset,ctx,contentLen,datalist[num])
		print 'block number : %d  chunk number :%d  '%(blocknum,num+1)
		reqchunk.chunkUpload()
		reqchunk.finalResponse()
		if num == 3:
			(ctx,offset) = reqchunk.getMessage()
			ctxdic[blocknum] =  ctx
		else:
			(ctx,offset) = reqchunk.getMessage()
			mkblock.chunk_size(datalist)[num+1]
	except IndexError :
		ctxdic[blocknum] = ctx
	except:
		continueUpload.protect_bk(filename,blocknum,num,ctx,ctxdic,offset)
		sys.exit(1)
	return ctx,offset,ctxdic,num

def make_file(filename,ctxdic):
	ctx_list = mkblock.sortdic(ctxdic)
	contentLen = len(ctx_list)
	reqmakefile = req_makefile('mkfile',mkblock.file_size(filename),ctx_list,contentLen,filename)
	reqmakefile.mkfileUpload()
	reqmakefile.finalResponse()

if __name__ == '__main__':
	blocknum = 1
	filename = baseinfo.filename
	input_data = mkblock.block_maker(filename)
	while (blocknum <= mkblock.count_block(filename)):
		num = 0
		input_stream = input_data.next()
		ctx,offset,datalist,block_size = upload_block(filename,blocknum,input_stream)
		while num < baseinfo.Block_Size/baseinfo.Chunk_Size -1 :
			ctx,offset,ctxdic,num = upload_chunk(filename,blocknum,num,datalist,ctxdic,offset,ctx)		
		blocknum = blocknum + 1	
	make_file(filename,ctxdic)

