class CounterInfo:
#inactive_2count_31count_0count_0count_0count_0count_0count_0count'
	def __init__(self,counter_char):
		self.info_list=counter_char.split('_')

	def get(self,channel):
		self.channel=int(channel)
		return self.info_list[channel]
