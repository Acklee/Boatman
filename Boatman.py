import dropbox
import os
import sys
import time

def	FileExist(file):
	if os.path.exists(file):
		return True
	else:
		print "File do not exist."
		exit()

def	UploadFile(file_src,token):
	FileExist(file_src)
	file_dst = "/"+os.path.basename(file_src)
	dbx = dropbox.dropbox.Dropbox(token)
	with open(file_src,'rb') as f:
		dbx.files_upload(f.read(),file_dst)
	if isinstance(result,dropbox.files.FileMetadata):
		print file_src+" upload success"

def	main():
	token_file = open('token.txt',"r+")
	token = (token_file.read())[6:]
	UploadFile(sys.argv[2],token)

if	__name__=="__main__":
	if len(sys.argv)<3:
		print '''
example:
Upload.py upload filepath
upload.py upload c:\\\\xxx\\\\xx\\\\1.txt
		'''
	else:
		main()
