import time, re
import converter 

# for plotting
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


########### FUNCTIONS TO CARRY OUT ANALYSIS #############


#------------- functions to plot figures from a list of feature vectors ---------------#

def treatment_feature_histogram(X,y,feat, names):
	obs = np.array([[0.]*len(X[0])]*2)
	for i in range(0, len(y)):
		obs[y[i]] += X[i]
	colors = ['b', 'r', 'g', 'm', 'k']							# Can plot upto 5 different colors
	pos = np.arange(1, len(obs[0])+1)
	width = 0.1     # gives histogram aspect to the bar diagram
	gridLineWidth=0.1
	fig, ax = plt.subplots()
# 	ax.xaxis.grid(True, zorder=0)
# 	ax.yaxis.grid(True, zorder=0)
	matplotlib.rc('xtick', labelsize=1)
# 	matplotlib.gca().tight_layout()
	for i in range(0, len(obs)):
# 		lbl = "treatment "+str(i)
		plt.bar(pos+i*width, obs[i], width, color=colors[i], alpha=0.5, label=names[i])
# 	plt.bar(pos, obs[0], width, color=colors[0], alpha=0.5)
	plt.xticks(pos+width, feat.data, rotation="vertical")		# useful only for categories
	#plt.axis([-1, len(obs[2]), 0, len(ran1)/2+10])
	plt.ylabel("# agents")
	feat.display()
	print obs[0]
	plt.legend()
	# saving:
	(matplotlib.pyplot).tight_layout()
	fig.savefig("./plots/"+"+".join(names)+".eps")
# 	plt.show()

def histogramPlots(list):
	a, b = converter.ad_vectors(list)
	obs = np.array(a)
	l = []
	colors = ['b', 'r', 'g', 'm', 'k']							# Can plot upto 5 different colors
	for i in range(0, len(list)):
		l.append([int(i) for i in obs[i]])
	pos = np.arange(1, len(obs[0])+1)
	width = 0.5     # gives histogram aspect to the bar diagram
	gridLineWidth=0.1
	fig, ax = plt.subplots()
	ax.xaxis.grid(True, zorder=0)
	ax.yaxis.grid(True, zorder=0)
	for i in range(0, len(list)):
		lbl = "ads"+str(i)
		plt.bar(pos, l[i], width, color=colors[i], alpha=0.5, label = lbl)
	#plt.xticks(pos+width/2., obs[0], rotation='vertical')		# useful only for categories
	#plt.axis([-1, len(obs[2]), 0, len(ran1)/2+10])
	plt.legend()
	plt.show()
	
def temporalPlots(list):
	obs = np.array(converter.temp_ad_vectors(list))
	#obs = np.array(ad_temp_category(list))
	print obs[0]
	dates = []
	colors = ['b.', 'r.', 'g.', 'm.', 'k.']
	for j in range(0, len(list)):
		dates.append(matplotlib.dates.date2num([list[j].data[i].time for i in range(0, len(list[j].data))]))
	pos = np.arange(len(obs[0]))
	gridLineWidth=0.1
	fig, ax = plt.subplots()
	ax.xaxis.grid(True, zorder=0)
	ax.yaxis.grid(True, zorder=0)
	for i in range(0, len(list)):
		lbl = "ads"+str(i)
		obs[i] = [j+1 for j in obs[i]]
		plt.plot(obs[i], dates[i], colors[i], alpha=0.5, label = lbl)
# 		plt.xticks(pos+width/2., obs[2], rotation='vertical')		# useful only for categories
	#plt.axis([-1, 500, 0, 700])
	plt.legend()
	plt.show()
	
