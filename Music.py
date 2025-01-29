import sys,os

class Music:
	def __init__(self):
		print "INIT"
	"""
	/isilon/blconfig/bl32xu/local_bss/yam/nc52356.wav
	/isilon/blconfig/bl32xu/local_bss/yam/nc91912.mp3
	/isilon/blconfig/bl32xu/local_bss/yam/nc41828.wav
	/isilon/blconfig/bl32xu/local_bss/yam/nc41829.wav
	/isilon/blconfig/bl32xu/local_bss/yam/nc67651.mp3
	/isilon/blconfig/bl32xu/local_bss/yam/nc67698.mp3
	"""

	def playWave(self,wavepath):	
		com="aplay %s"%wavepath
		os.system(com)

	def playMP3(self,mp3path):
		com="mpg123 %s"%mp3path
		os.system(com)

	def play(self,mp3_or_wave):
		if mp3_or_wave.rfind("mp3")!=-1:
			self.playMP3(mp3_or_wave)
		elif mp3_or_wave.rfind("wav")!=-1:
			self.playWave(mp3_or_wave)

if __name__=="__main__":
	mu=Music()
	mu.play("/isilon/blconfig/bl32xu/local_bss/yam/nc41828.wav")
	mu.play("/isilon/blconfig/bl32xu/local_bss/yam/nc41829.wav")
	mu.play("/isilon/blconfig/bl32xu/local_bss/yam/nc67651.mp3")
