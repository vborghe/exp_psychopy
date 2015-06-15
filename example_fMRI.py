#!/usr/bin/env python
# -*- coding: utf-8

###########################################################################################################################################################
#                                                                      vb
#                                                                   Oct 2014
#                               heavily reling on Yi-Chen LIN scripts (and many online resources found here and there)
#                 [WARNING: I'm a terrible coder! which means...a lot of work yet to be done in terms of efficiency and cleaning...  ;-)
#                plus, Psychopy has many terrific features (e.g. helps to handle the trials) that I had no time to review yet..be The One!]
###########################################################################################################################################################

'''
====================================================
            Import needed tools
====================================================
'''

from __future__ import division                             # so that 1/3=0.333 instead of 1/3=0
import os                                                     # for file/folder operations
import numpy as np                                             # numbers
import pandas as pd                                             # data storage 
from numpy.random import random, shuffle                         # for random number generators and shuffling
from psychopy import visual, event, core, gui, data, logging      # all needed modules from psychopy
from psychopy.constants import *                                    # things like STARTED, FINISHED


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
- 32 stimuli repeated 4 times plus 6 odd
- list of stimuli order needs to be already saved
_ interface with fMRI 
- number of frames computed for monitor with 60hz refresh rate (16.7 ms per frame)

====================================================
'''


'''
====================================================
        Define needed functions
====================================================
'''

def WaitMRITTL(win):                                                       # to wait for fMRI TTL [or S key pressing on the keyboard]
    Message(win, "+")                                                        # message the subject will be reading while waiting the TTL
    event.clearEvents()
    while True:
        for keys in event.getKeys():                                        # check if a key got pressed
            if keys in ['s']:                                               # go on if that key was the S
                return None
    win.flip()

def WaitPressKey_Space(win):                                               # to allow the pressing of spacebar/esacpe 
    event.clearEvents()
    while True:
        for keys in event.getKeys():
            if keys in ['space']:                                            # if SPACE, go on
                return None
            elif keys in ['escape']:                                         # if ESCAPE, stop experiment
                win.close()
                core.quit()
                return None 

def WaitTyesnoAnswer(win,resp_trial, rt_trial,onset_trial):                # to allow the pressing of L/R for yes/no answers
    listkeys = event.getKeys()
    if len(listkeys) >  0:                                                   # check if any response has been given now
        if resp_trial == 0:                                                  # check if any response has been given before
            for keys in listkeys:
                # answer mapping:
                if int(exp_info['answ'])==1:                                 # [1 = YES/x-left, NO/y-right]
                    if keys in ['x']:
                        rt_trial = (core.getTime()) - onset_trial
                        resp_trial = 1                                        # in this run, this is a YES done with x-left = 1
                    elif keys in ['y']:
                        rt_trial = (core.getTime()) - onset_trial
                        resp_trial = 2                                        # in this run, this is a NO done with y-right = 2
                    elif keys in ['escape']:
                        win.close()
                        core.quit()
                        return None
                else:                                                        # [2 = YES/y-right, NO/x-left]
                    if keys in ['y']:
                        rt_trial = (core.getTime()) - onset_trial
                        resp_trial = 4                                        # in this run, this is a YES done with y-right = 4
                    elif keys in ['x']:
                        rt_trial = (core.getTime()) - onset_trial
                        resp_trial = 3                                        # in this run, this is a NO done with x-left = 3
                    elif keys in ['escape']:
                        win.close()
                        core.quit()
                        return None
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

def Presenttarget(trial,stim, ISI, count):                                              # to present target stimuli 
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
    tot_trial = isi_trial+60
    for frameN in range(tot_trial):
        # stimuli are presented for a fixed number of frames (60)
        if 1 <= frameN < 60:
            stim.draw()
        # fixation intrastimuli randomized
        if 60 <= frameN < tot_trial:
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
    for frameN in range(240):
        if 1 <= frameN < 200:
            stim1.draw()
            stim2.draw()
            stim3.draw()
            stim4.draw()
            win.flip()
            if resp_trial == 0:
                resp_trial, rt_trial = WaitTyesnoAnswer(win, resp_trial,rt_trial,onset_trial)
        if 200 <= frameN < 240:
            fixation.draw()
            win.flip()
            if  resp_trial == 0:
                resp_trial, rt_trial = WaitTyesnoAnswer(win, resp_trial,rt_trial,onset_trial)
    return stim_trial, resp_trial, rt_trial, onset_trial
    
def PresentStimuli(stim, odd1, odd2, runlist, ISI):
    count = 0
    # create a dictionary for results
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
            results.setdefault('numb', []).append(i)
            results.setdefault('stim', []).append(stim_trial)
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
exp_name = 'SemDim fMRI'
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
stimuli_file = 'imaging.csv'
resultpath = 'results/fMRI/'+ exp_info['id']
if not os.path.isdir(resultpath):
    os.makedirs(resultpath)
    
# load stimuli table
sti = pd.read_csv(stimuli_file, header = 0, sep=';', encoding = 'latin-1')
stims = sti['w1']

# target stimuli
stim = stims[0:32]
# odd stimuli
odd1 = stims[32:64]
odds = sti['w2']
odd2 = odds[32:64]

# load stimuli list for this run (each number corresponds to a given stimulus)
runlist = np.load('exp_info['id'] + '/'+ 'run' + exp_info['run'] +  '.npy')

# Clock
clock = core.Clock()

# Set properties of the window
win = visual.Window(size=(1366, 768),fullscr=True, monitor="testMonitor", units="deg", color='Black')
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
ISImin = 162.00
ISImax = 198.00
ISI = np.arange(ISImin, ISImax, (ISImax-ISImin)/128)
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

# TTL and then start
WaitMRITTL(win)
TTl_onset = core.getTime()

# Wait a bit  [should be ~3 TR => (2300*3)/16.7]
for frameN in range(414):
    fixation.draw()
    win.flip()

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
results['onsets'] = results['onsets']-TTl_onset

taskone = results.copy()
taskone.to_csv(results_fname, index=False, encoding = 'latin-1') 

print("#" * 20 + "               we made it!               " + "#" * 20)

# Quit the experiment
core.quit() 
