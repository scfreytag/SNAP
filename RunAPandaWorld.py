import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print dir_path

import sys
sys.path.append('.\src\pylsl')

import direct.directbase.DirectStart
import PandaWorld
from direct.task import Task

from pylsl import continuous_resolver, stream_info, stream_inlet, vectorf


import tobii

w = PandaWorld.World()

resolver = continuous_resolver('type','3DCoord')
inlet = None

def task_aquireLSLValues(inlet, task):
	allSamplesAvailable = []
	
	sample = vectorf()

	while inlet.samples_available():
		ts = inlet.pull_sample(sample)
		pythonVector = [x for x in sample]
		
		allSamplesAvailable.append((ts, pythonVector)) 
		
	w.processLSLSamples(allSamplesAvailable)

	return task.cont

def task_lookUpLSL(task):
	results = resolver.results()

	if len(results) > 0:
		print 'Found stream'
		inlet = stream_inlet(results[0])
		inlet.open_stream()
		taskMgr.add(task_aquireLSLValues, 'ReadLSLSamples', extraArgs =[ inlet ], appendTask=True)
		return task.done

	return task.cont

	
	
	
# Eye Tracking
def task_lookUpEyeTracker(task):

	# do eyetracking stuff here...
	# push the values to the world
	# w.processEyePosition
	pass

taskMgr.add(task_lookUpLSL, 'LookUpLSLStream')
taskMgr.add(task_lookUpEyeTracker, 'LookUpEyeTracker')

taskMgr.add(w.Update, 'MainUpdateLoop')


tobii.addGazeCallback(w.processGaze)
tobii.connect()


run()