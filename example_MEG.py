#!/usr/bin/env python
# -*- coding: utf-8

###########################################################################################################################################################
#                                                                       vb
#                                                                    Oct 2014
#                                  heavily reling on Yi-Chen LIN scripts (and many online resources found here and there)
#                                                 thanks to Marco + [Jaco,Denis,Noa] for the MEG part
#                 [WARNING: I'm a terrible coder! which means...a lot of work yet to be done in terms of efficiency and cleaning...  ;-)
#                plus, Psychopy has many terrific features (e.g. helps to handle the trials) that I had no time to review yet..be The One!]
###########################################################################################################################################################

'''
====================================================
            Import needed tools
====================================================
'''

from __future__ import division                                           # so that 1/3=0.333 instead of 1/3=0
import os                                                                   # for file/folder operations
import numpy as np                                                           # numbers
import pandas as pd                                                            # data storage 
from numpy.random import random, shuffle                                         # for random number generators and shuffling
from psychopy import visual, core, data, event, logging, gui, parallel            # all needed modules from psychopy
from psychopy.constants import *                                                      # things like STARTED, FINISHED


'''
====================================================
            What this script does
====================================================

- store info about the subj (name, age, run)
- present single target words 
- present couples of odd words 
- collect answers and RT for the odd detection task
- sub answers are coded in order to later identify  both YES vs NO and LEFT vs RIGHT click
- save results (one sub = one folder, 6 runs = 6 files)
- 32 stimuli repeated 5 times plus 10 odd
- list of stimuli order needs to be already saved
_ interface with MEG 
- number of frames computed for monitor with 60hz refresh rate (16.7 ms per frame)

====================================================
'''


'''
====================================================
        MEG parallel port for input/output
====================================================
'''
# you need parallel port in order to:

try:
   trig_port = parallel.ParallelPort(address=0x0378)               # send triggers corresonding to your stimuli
   trig_port.setData(0)
   print('Reset trigger port\n')
except:
   print('Problem connecting to PC parallel port')
try:
   resp_port1 = parallel.ParallelPort(address=0x0379)              # get subject responses
   resp_port2 = parallel.ParallelPort(address=0x0BCE1)
except:
   print('Problem connecting to e-prime parallel port')
   class MockPort(object):
      def __init__(self):
          pass

      def readData(self):
         return 0

   resp_port = MockPort()


'''
====================================================
        Define needed functions
====================================================
'''

def WaitPressKey_Space(win):                                        # to allow the pressing of spacebar [escape will close the experiment]
    event.clearEvents()
    while True:
        for keys in event.getKeys():
            if keys in ['space']:
                return None
            elif keys in ['escape']:
                win.close()
                core.quit()
                return None 

def WaitTyesnoAnswer(win,resp_trial, rt_trial,onset_trial):
    resp1 = resp_port1.readData()
    resp2 = resp_port2.readData()
    if resp1 !=  0:                                                    # check if any response has been given now with 8
        if resp_trial == 0:                                            # check if any response has been given before
            if int(exp_info['answ'])==1:                              # [8 = port1 = right]
                if resp1 in [8]:
                    rt_trial = (core.getTime()) - onset_trial
                    resp_trial = 1
                    print( resp_trial)
            else:                                                      # [8 = port1 = right]
                if resp1 in [8]:
                    rt_trial = (core.getTime()) - onset_trial
                    resp_trial = 4
                    print(resp_trial)
    elif resp2 !=  0:                                                  # check if any response has been given now with 16
        if resp_trial == 0:                                            # check if any response has been given before
            if int(exp_info['answ'])==1:                               # [16 = port2 = left]
                if resp2 in [16]:
                    rt_trial = (core.getTime()) - onset_trial
                    resp_trial = 2
                    print(resp_trial)
            else:                                                      # [16 = port2 = left]
                if resp2 in [16]:
                    rt_trial = (core.getTime()) - onset_trial
                    resp_trial = 3
                    print(resp_trial)
    else:                                                               # no answer has been given, put 0
        resp_trial = 0
        rt_trial = 0
    return resp_trial, rt_trial                                         # return response and RT

def Message(win, string):                                              # to present a message
    message = visual.TextStim(win,text=string,
                                    ori=0,
                                    pos=(0.0, 0.0),
                                    font = 'CourierNew',
                                    color = 'Silver')
    message.draw()
    win.flip()
    return message

def Presenttarget(trial,stim, ISI, count):                                       # to present target stimuli 
    stim_trial = stim[trial]
    resp_trial = 99
    rt_trial = 99
    stim = visual.TextStim(win, text=stim_trial,
                                    ori=0,
                                    pos=(0.0, 0.0),
                                    font = 'CourierNew',
                                    color = 'Silver' )
    onset_trial = core.getTime()  
    isi_trial = int(round(ISI[count]))
    tot_trial = isi_trial+30
    for frameN in range(tot_trial):
        # stimuli are presented for a fixed number of frames (30)
        if 1 <= frameN < 18:
            codetrial=int(trial+1)
            trig_port.setData(codetrial)           # send to the parallel port the code for this stimulus
            stim.draw()
        # fixation intrastimuli randomized
        if 18 <= frameN < tot_trial:
            trig_port.setData(0)                   # send to the parallel port 0 to reset 
            fixation.draw()
        # show
        win.flip() 
    return stim_trial, resp_trial, rt_trial, onset_trial
    
def Presentodd(trial,odd1, odd2):                                                 # to present odd stimuli [timing is fixed]
    odd1_trial = odd1[trial]
    odd2_trial = odd2[trial]
    stim_trial = odd1_trial
    resp_trial = []
    rt_trial = []
    stim1 = visual.TextStim(win, text=odd1_trial,
                                    ori=0,
                                    pos=(0.0, 0.5),
                                    font = 'CourierNew',
                                    color = 'DarkRed' )
    stim2 = visual.TextStim(win, text=odd2_trial,
                                    ori=0,
                                    pos=(0.0, -0.5),
                                    font = 'CourierNew',
                                    color = 'DarkRed' )
    if int(exp_info['answ'])==1:
        R ='no'
        L ='oui'
    else:
        R ='oui'
        L ='no'
    stim3 = visual.TextStim(win, text=R,
                                    ori=0,
                                    pos=(3.5, -1.5),
                                    font = 'CourierNew',
                                    color = 'Silver' )
    stim4 = visual.TextStim(win, text=L,
                                    ori=0,
                                    pos=(-3.5, -1.5),
                                    font = 'CourierNew',
                                    color = 'Silver' )
    onset_trial = core.getTime()
    event.clearEvents()
    resp_trial = 0
    for frameN in range(200):
        if 1 <= frameN < 10:
            codetrial=int(trial+1)
            trig_port.setData(codetrial)            # send to the parallel port the code for this stimulus (100 ms should be enough)
            stim1.draw()
            stim2.draw()
            stim3.draw()
            stim4.draw()
            win.flip()
            if resp_trial == 0:
                resp_trial, rt_trial = WaitTyesnoAnswer(win, resp_trial,rt_trial,onset_trial)
        if 10 <= frameN < 150:
            codetrial=int(trial+1)
            trig_port.setData(0)                    # send to the parallel port 0 to reset 
            stim1.draw()
            stim2.draw()
            stim3.draw()
            stim4.draw()
            win.flip()
            if resp_trial == 0:
                resp_trial, rt_trial = WaitTyesnoAnswer(win, resp_trial,rt_trial,onset_trial)
        if 150 <= frameN < 200:
            fixation.draw()
            win.flip()
            if  resp_trial == 0:
                resp_trial, rt_trial = WaitTyesnoAnswer(win, resp_trial,rt_trial,onset_trial)
    return stim_trial, resp_trial, rt_trial, onset_trial

def PresentStimuli(stim, odd1, odd2, runlist, ISI):
    count = 0
    # create dictionary for results
    results = {}
    for i in range(0,15):            # right now we don't want to see ALL the stimuli, but just some
    #for i in range(0,len(runlist)):
        trial = runlist[i]
        stim_code = trial
        try:                         # try/except, if fails we still get the results up to where we are
            if trial >= 32:
                stim_trial, resp_trial, rt_trial, onset_trial = Presentodd(trial, odd1, odd2)           # present an odd event, the subject is supposed to answer
            else:
                stim_trial, resp_trial, rt_trial, onset_trial = Presenttarget(trial,stim, ISI, count)   # present a target event, the subject is supposed to read
                count = count + 1
        # fill in the dictionary with the results
            results.setdefault('stim', []).append(stim_trial)
            results.setdefault('numb', []).append(i)
            results.setdefault('stim_code', []).append(stim_code)
            results.setdefault('onsets', []).append(onset_trial)
            results.setdefault('rt', []).append(rt_trial)
            results.setdefault('response', []).append(resp_trial)
        except:
            print('Problem here %s' % i )
            break
    return results

'''
====================================================
    Store info about the experiment session
====================================================
'''
# Show a dialog box to enter session information
exp_name = 'SemDim MEG'
exp_info = {
            'id': '',                      # ID of the sub
            'run': '',                     # run (to know which runlist has to be loaded)
            'answ':'',                     # answer mapping [1 = YES/x-left, NO/y-right] vs [2 = YES/y-right, NO/x-left]
            }
dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()



'''
====================================================
            Set main variables
====================================================
'''

# I/O directories and names 
stimuli_file = 'stimuli/imaging.csv'
resultpath = 'results/MEG/'+ exp_info['id']
if not os.path.isdir(resultpath):
    os.makedirs(resultpath)
    
# load stimuli table
sti = pd.read_csv(stimuli_file, header = 0, sep=';', encoding = 'latin-1') # sti.XXX is "XXX" column
stims = sti['w1']

# target stimuli
stim = stims[0:32]
# odd stimuli
odd1 = stims[32:64]
odds = sti['w2']
odd2 = odds[32:64]

# load stimuli list for this run
runlist = np.load('stimuli/MEG/' + exp_info['id'] + '/'+ 'run' + exp_info['run'] +  '.npy')

# Clock
clock = core.Clock()

# Set properties of the window    [1024 x 778 MEG screen]
win = visual.Window(size=(1024, 778),fullscr=True, monitor="testMonitor", units="deg", color='Black')
myMouse = event.Mouse(win=win)
myMouse.setVisible(0)                                                                       # Mouse not visible

# Other objects to be presented
fixation = visual.TextStim(win, text='+',                                                   # Fixation
                                    height=0.8,
                                    ori=0,
                                    pos=(0.0, 0.0),
                                    font = 'CourierNew',
                                    color = 'Silver')


# List of ISI
ISImin = 130.00
ISImax = 200.00
ISI = np.arange(ISImin, ISImax, (ISImax-ISImin)/160)
shuffle(ISI)

'''
====================================================
        Run the experiment
====================================================
'''
print("#" * 20 + "              Grab your towel              " + "#" * 20)

# INTRO
Message(win, u'Gardez les yeux fixÃ©s sur la croix')
WaitPressKey_Space(win)
Message(win, u'Vous Ãªtes prÃªts?')
WaitPressKey_Space(win)

# Wait a bit
for frameN in range(30):
    fixation.draw()
    win.flip()

Start_onset = core.getTime()
print(Start_onset)

# Present all stimuli of this run and get results
results =  PresentStimuli(stim, odd1, odd2, runlist,ISI)

'''

====================================================
                End the experiment
====================================================
'''
Message(win, u'Cette bloc est terminÃ©e.')
WaitPressKey_Space(win)

Message(win, u'Merci beaucoup!')
WaitPressKey_Space(win)

# Save all data to a file
results_fname = exp_info['run'] + '_' + 'results.csv'
results_fname = os.path.join(resultpath, results_fname)
results = pd.DataFrame(results)

# Subtract TTL from all onsets
results['onsets'] = results['onsets']-Start_onset

taskone = results.copy()
taskone.to_csv(results_fname, index=False, encoding = 'latin-1') 

print("#" * 20 + "               we made it!               " + "#" * 20)

# Quit the experiment
core.quit()  
