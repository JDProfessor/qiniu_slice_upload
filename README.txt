此程序实现了七牛云存储的分片上传,断点续上传,多线程上传，适用于文件较大的上传需求。

baseinfo    模块：填写基本信息 
				1. deadline 为token的截止时间,默认为60S
				2. dic     需要填写仓库名
				3. ak
				4. sk
				5. Block_Size  设置每块大小(默认4M)
				6. Chunk_Size  设置每片大小(默认1M)
				7. filename    设置需上传文件的路径

tkproductor 模块 ：生成token

Time 		模块 :可以设置deadline,默认60S

mkblock     模块 :分片器 

upload_block 模块 ：分片文件上传器

continueUpload 模块: 断点续传器,需要之前upload_block上传出现断点.断点保存在bkpoint.txt中,每次断点续上传完毕必须后需要清空其内容,为下次断点做准备.

Thread_upload 模块: 多线程上传器,默认启动3个线程.

