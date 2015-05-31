#usr/bin/python
#
import threading,upload_block,mkblock,baseinfo,time

class Count(threading.Thread):
	def __init__(self,cond):
		threading.Thread.__init__(self)
		self.cond = cond

	def run(self):
		cond = self.cond
		global blocknum
		while blocknum <= mkblock.count_block(filename):
			cond.acquire()
			blocknum = blocknum + 1
			if blocknum >mkblock.count_block(filename):
				break
			cond.wait()
			cond.release()

class uploadThread(threading.Thread):
	def __init__(self,cond):
		threading.Thread.__init__(self)
		self.local = threading.local()

	def run(self):
		while blocknum <= mkblock.count_block(filename)  :
			cond.acquire()
			cond.notify()
			self.local.blocknum = blocknum	
			input_stream = f.read(baseinfo.Block_Size)
			cond.release()
			global ctxdic
			num = 0
			ctx,offset,datalist,block_size = upload_block.upload_block(filename,self.local.blocknum,input_stream)
			while num < baseinfo.Block_Size/baseinfo.Chunk_Size -1 :
				ctx,offset,ctxdic,num = upload_block.upload_chunk(filename,self.local.blocknum,num,datalist,ctxdic,offset,ctx)	

if __name__ == '__main__':

#	filename = '/home/jd/backups/SmartHome.pdf'
	filename = baseinfo.filename
	blocknum = 0
	ctxdic = {}
	threads = []
	cond = threading.Condition()
	f = open(filename,'r')
	count = Count(cond)
	count.start()
	for i in range(3):
		upload_thread = uploadThread(cond)
		upload_thread.start()
		threads.append(upload_thread)
		time.sleep(1)

	for Thread in threads:
		Thread.join()
	f.close()
	upload_block.make_file(filename,ctxdic)
	
