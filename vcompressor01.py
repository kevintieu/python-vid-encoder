import subprocess, os, math, shutil

def convert(size):
	if (size == 0):
		return '0B'
	size_name = ("B", "KB", "MB", "GB", "TB")
	i = int(math.floor(math.log(size, 1024)))
	p = math.pow(1024, i)
	s = round(size / p, 2)
	return '%s %s' % (s, size_name[i])

def converttime(secs):
	mins, secs = divmod(secs, 60)
	return '%02d:%02d' % (mins, secs)

def runagain():
	print("\nProcess another folder? (y/n)")
	choice = input().lower()
	if (choice == 'y' or choice == 'yes'):
		run()

def run():
	import time
	print("\nEnter a directory: ")
	user_dir = input()
	if os.path.exists(user_dir):
		start = time.time()
		total_size = 0
		compressed_size = 0
		total_vids = 0
		compressed_vids = 0
		for subdir, dirs, files in os.walk(user_dir):
			for file in files:
				if file.lower().endswith('.mov') or file.lower().endswith('.avi'): 
					# or file.lower().endswith('.flv') or file.lower().endswith('.wmv')
					filepath = subdir + os.sep + file
					filename = file
					filesize = os.path.getsize(filepath)
					total_size += filesize
					total_vids += 1
					temp = subdir + os.sep + 'temp_v'
					filename_new = os.path.splitext(filename)[0] + '_new.mp4'
					filepath_new = subdir + os.sep + filename_new
					subprocess.call(['ffmpeg', '-i', filepath, '-vcodec', 'h264', filepath_new])				
					filesize_new = os.path.getsize(filepath_new)
					if filesize_new > filesize:
						os.remove(filepath_new)
						total_size -= filesize
					else:
						if not os.path.exists(temp):
							os.makedirs(temp)
						shutil.move(filepath_new, temp + os.sep + filename_new)
						compressed_vids += 1
						compressed_size += filesize_new
		end = time.time()
		time = round(end - start, 2)
		print("Compressed " + str(compressed_vids) + " out of " + str(total_vids) + " videos.")
		print("Raw size: " + convert(total_size) + "\nCompressed size: " + convert(compressed_size))
		print('Time elapsed: ' + converttime(time))
		runagain()

	else:
		print("\nThis path does not exist")
		run()

run()