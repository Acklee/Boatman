import dropbox
import os
import sys
import time
import threading
import Queue

token_file = open('token.txt',"r+")
token = (token_file.read())[6:]
queue = Queue.Queue()


def GetFileList(rootDir):
	files_list = []
	list_dirs = os.walk(rootDir)
	for root,dirs,files in list_dirs:
		for f in files:
			files_list.append(os.path.join(root, f))
	return files_list
	
class ThreadUpload(threading.Thread):
	def __init__(self,queue):
		threading.Thread.__init__(self)
		self.queue = queue
		
	def run(self):
		while True:
			file = queue.get()
			UploadFile(file)
			self.queue.task_done()

	
def	FileExist(file):
	if os.path.exists(file):
		return True
	else:
		print "File do not exist."
		exit()

def	UploadFile(file_src):
	FileExist(file_src)
	file_dst = "/"+os.path.basename(file_src)
	dbx = dropbox.dropbox.Dropbox(token)
	with open(file_src,'rb') as f:
		result = dbx.files_upload(f.read(),file_dst)
	if isinstance(result,dropbox.files.FileMetadata):
		print file_src+" upload success"

def	main():
	file_list = GetFileList(sys.argv[2])
	#UploadFile(sys.argv[2])
	for i in range(int(sys.argv[3])):
		t = ThreadUpload(queue)
		t.setDaemon(True)
		t.start()
	for file in file_list:
		queue.put(file)
	queue.join()
	
if	__name__=="__main__":
	if len(sys.argv)<3:
		print '''
example:
Upload.py upload filepath
upload.py upload c:\\\\xxx\\\\xx\\\\1.txt
upload.py updir c:\\\\xxx\\\\xxxx threads
		'''
		exit()
	else:
		main()
