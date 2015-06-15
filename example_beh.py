#!/usr/bin/env python
# -*- coding: utf-8

###########################################################################################################################################################
#                                                                       vb
#                                                                    Oct 2014
#                                  heavily reling on Yi-Chen LIN scripts (and many online resources found here and there)
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
import itertools                                                      # merge list

'''
====================================================
            What this script does
====================================================

- store info about the subj (name, age, gender)
- present couple of words for a rating task
- present single words for two rating tasks
- task 1 is the first for all subjects
- task 2/3 are in counterbalanced order across subjects
- the order of the two semantic categories is conterbalanced as well
- collect answers and RT for the 4 task
- save them in 4 separate files
====================================================
'''

'''
====================================================
        Define needed functions
====================================================
'''

def WaitAnykey(win):                                                    # to allow the pressing of anykey [escape will close the experiment]
    event.clearEvents()
    resp=None
    while True:
        for key in event.getKeys():
            if key in ['escape']:
                win.close()
                core.quit()
                return None
            else:
                return None

def WaitPressKey_Space(win):                                            # to allow the pressing of spacebar [escape will close the experiment]
    event.clearEvents()
    while True:
        for keys in event.getKeys():
            if keys in ['space']:
                return None
            elif keys in ['escape']:
                win.close()
                core.quit()
                return None 


def WaitTratingAnswer(win):                                             # to allow the pressing of numbers to rate pairs
    event.clearEvents()
    resp=None
    while True:
        for keys in event.getKeys():
            if keys in ['1']:
                T1 = core.getTime()
                resp = 1
                return resp, T1
            elif keys in ['2']:
                T1 = core.getTime()
                resp = 2
                return resp, T1
            elif keys in ['3']:
                T1 = core.getTime()
                resp = 3
                return resp, T1
            elif keys in ['4']:
                T1 = core.getTime()
                resp = 4
                return resp, T1
            elif keys in ['5']:
                T1 = core.getTime()
                resp = 5
                return resp, T1
            elif keys in ['6']:
                T1 = core.getTime()
                resp = 6
                return resp, T1
            elif keys in ['7']:
                T1 = core.getTime()
                resp = 7
                return resp, T1
            elif keys in ['8']:
                T1 = core.getTime()
                resp = 8
                return resp, T1
            elif keys in ['9']:
                T1 = core.getTime()
                resp = 9
                return resp, T1

def Message(win, string):                                                                 # to present a message
    message = visual.TextStim(win,text=string,
                                    ori=0, pos=(0.0, 0.0),
                                    font = 'CourierNew',
                                    alignHoriz='center', alignVert='center',
                                    color = 'WhiteSmoke' )
    message.draw()
    win.flip()
    
def MessageMultiLine(win, string1, string2, string3):                                   # to present a message in multiples lines
    message1 = visual.TextStim(win,text=string1,
                                    ori=0, pos=(0.0, 1.2),
                                    font = 'CourierNew',
                                    alignHoriz='center', alignVert='center',
                                    color = 'WhiteSmoke' )
    message1.draw()
    message2 = visual.TextStim(win,text=string2,
                                    ori=0, pos=(0.0, 0),
                                    font = 'CourierNew',
                                    alignHoriz='center', alignVert='center',
                                    color = 'WhiteSmoke' )
    message2.draw()
    message3 = visual.TextStim(win,text=string3,
                                    ori=0, pos=(0.0, -1.2),
                                    font = 'CourierNew',
                                    alignHoriz='center', alignVert='center',
                                    color = 'WhiteSmoke' )
    message3.draw()
    win.flip()

def PresentGeneralInstruction(win):                                                    # to present the general instructions
    Message(win, u'Bonjour!')
    WaitPressKey_Space(win)
    MessageMultiLine(win, u"""Maintenant""", 
                          u"""nous vous demandons""", 
                          u"""de faire trois tÃ¢ches.""")
    WaitPressKey_Space(win)
    MessageMultiLine(win, u"""Dans tous les cas,""",
                          u"""rÃ©pondez le plus""",
                          u"""automatiquement possible.""")
    WaitPressKey_Space(win)
    Message(win, u'Vous Ãªtes prÃªts?')
    WaitPressKey_Space(win)

def PresentYN(stimulus, Y, N):                                                           # to present target stimuli for task 2 ad 3
    stim = visual.TextStim(win, text=stimulus,pos = (0, 1))
    stim.draw()
    resp_message = '1    2    3    4    5    6    7    8   9'
    stim2 = visual.TextStim(win,text=resp_message,pos = (0,-1))
    stim2.draw()
    win.flip() 
    resp_trial, T1_trial = WaitTratingAnswer(win)
    win.flip() 
    for frameN in range(10):
        if 0 <= frameN < 10:
            fixation.draw()
        win.flip() 
    return resp_trial, T1_trial

def PresentSemDist(stimpair):                                                          # to present target stimuli for semantic distance measure
    spltited = stimpair.split()
    stim1 = visual.TextStim(win, text=spltited[0],pos = (-4, 1))
    stim2 = visual.TextStim(win, text=spltited[1],pos = (+4, 1))
    resp_message = '1    2    3    4    5    6    7    8   9'
    stim3 = visual.TextStim(win,text=resp_message,pos = (0,-1))
    stim1.draw()
    stim2.draw()
    stim3.draw()
    win.flip() 
    resp_trial, T1_trial = WaitTratingAnswer(win)
    win.flip() 
    for frameN in range(10):
        if 0 <= frameN < 10:
            fixation.draw()
        win.flip() 
    return resp_trial, T1_trial

def SingleWords(stimS, Y,N):                                                          # task TWO and THREE
    shuffle(stimS)
    rt_all = []
    stim_all = []
    resp_all = []
    for i in range(0,32):
        T0 = core.getTime()
        resp_trial, T1_trial = PresentYN(stimS[i],Y, N)
        rt_trial = T1_trial - T0
        resp_all.append(resp_trial)
        rt_all.append(rt_trial)
        stim_all.append(stimS[i])
    return stim_all, resp_all, rt_all

def PairedWords(stimP):                                                                # task ONE
    resp_all = []
    rt_all = []
    stim_all1 = []
    stim_all2 = []
    for i in range(0,240):
        T0 = core.getTime()
        resp_trial, T1_trial = PresentSemDist(stimP[i])
        rt_trial = T1_trial - T0
        resp_all.append(resp_trial)
        rt_all.append(rt_trial)
        stim_all1.append(stimP[i].split()[0])
        stim_all2.append(stimP[i].split()[1])
    return stim_all1,stim_all2,resp_all, rt_all

def RunTaskOne(win, stimP):
    Message(win, u'DISTANCE SÃ‰MANTIQUE')
    WaitPressKey_Space(win)
    Message(win, u'Deux mots vont apparaitre.')
    WaitPressKey_Space(win)
    MessageMultiLine(win, u"""Vous devez juger""", 
                          u"""la similaritÃ© des objets/animaux""", 
                          u"""auxquels se rÃ©fÃ¨rent les mots.""")
    WaitPressKey_Space(win)
    MessageMultiLine(win, u"""Le jugement s'exprime sur une Ã©chelle:""", 
                          u"""        de 1 (trÃ¨s Ã©loignÃ©s)""", 
                          u"""        Ã  9 (trÃ¨s similaires).""")
    WaitPressKey_Space(win)
    MessageMultiLine(win, u"""Par exemple:""", 
                          u"""chat - baleine = 1""", 
                          u"""table - chaise = 8""")
    WaitPressKey_Space(win)
    stim_all1,stim_all2, resp_all, rt_all=  PairedWords(stimP)
    task1 = {
            'stim_1':stim_all1, 
            'stim_2':stim_all2, 
            'resp_all':resp_all,  
            'rt_all':rt_all, 
            }
    return task1

def RunTaskTwo(win, stimS):
    Message(win, u'PROPRIÃ‰TÃ‰S SONORES')
    WaitPressKey_Space(win)
    MessageMultiLine(win, u"""Un mot va apparaitre.""", 
                          u"""Vous devez rÃ©pondre""", 
                          u"""Ã  une question.""")    
    WaitPressKey_Space(win)
    MessageMultiLine(win, u"""L'objet ou animal auquel""",
                          u"""le mot se rÃ©fÃ¨re""",
                          u"""produit un son caractÃ©ristique?""")
    WaitPressKey_Space(win)
    MessageMultiLine(win, u"""Par exemple:""", 
                          u"""chat  = 9""", 
                          u"""table = 1""")
    WaitPressKey_Space(win)
    stim_all, resp_all, rt_all=  SingleWords(stimS, 'pas son','son',)
    task2 = {
            'stim_all':stim_all, 
            'resp_all':resp_all,  
            'rt_all':rt_all, 
            }
    return task2

def RunTaskThree(win, stimS):
    Message(win, u'PROPRIÃ‰TÃ‰S VISUELLES')
    WaitPressKey_Space(win)
    MessageMultiLine(win, u"""Un mot va apparaitre.""", 
                          u"""Vous devez rÃ©pondre""", 
                          u"""Ã  une question.""")    
    WaitPressKey_Space(win)
    MessageMultiLine(win, u"""Par rapport Ã """,
                          u"""une boÃ®te Ã  chaussures,""",
                          u"""l'objet/animal est""")
    WaitPressKey_Space(win)
    MessageMultiLine(win, u"""plus grand ou plus petit?""", 
                          u"""De combien?""", 
                          u"""Par exemple:""")
    WaitPressKey_Space(win)
    MessageMultiLine(win, u"""abeille  = 1""", 
                          u"""chien  = 6""", 
                          u"""table = 9""")
    WaitPressKey_Space(win)
    stim_all, resp_all, rt_all=  SingleWords(stimS, 'petit','grand',)
    task3 = {
            'stim_all':stim_all, 
            'resp_all':resp_all,  
            'rt_all':rt_all, 
            }
    return task3

'''
====================================================
    Store info about the experiment session
====================================================
'''

# Show a dialog box to enter session information
exp_name = 'SemDim Behavioural'
exp_info = {
            'catord':'',
            'taskord':'',
            'id': '',  
            }
dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()


#exp_info['date'] = data.getDateStr()                          # Add the date and the experiment name, if needed
#exp_info['exp_name'] = exp_name

results = {
            'taskone':'', 
            'tasktwo':'',  
            'taskthree':'', 
            }

'''
====================================================
            Set main variables
====================================================
'''

# I/O directories and names 
stimuli_file = 'behavioural.csv'
resultpath = 'results/behavioural/' + exp_info['id']
if not os.path.isdir(resultpath):
    os.makedirs(resultpath)
    
# Load stimuli table
sti = pd.read_csv(stimuli_file, header = 0, sep='\t', encoding = 'latin-1') # sti.XXX is "XXX" column
stim = sti['stimuli']

# Stimuli Pairs (order A vs T balanced across subjects according to catord)
stimPA = stim[32:152].values
stimPT = stim[152:272].values
shuffle(stimPA)
shuffle(stimPT)
stimP = []
if 12==0:                             # 0 = animal first, 1 = tool first (counterbalanced across subjects)
    stimP.append(stimPA)
    stimP.append(stimPT)
    stimPAll = [i for i in itertools.chain.from_iterable(stimP)]
else:
    stimP.append(stimPT)
    stimP.append(stimPA)
    stimPAll = [i for i in itertools.chain.from_iterable(stimP)]
stimP = []
stimP = stimPAll 

# Stimuli Single Words (order A vs T balanced across subjects according to catord)
stimSA = stim[0:16].values
stimST = stim[16:32].values
shuffle(stimSA)
shuffle(stimST)
stimS = []
if int(exp_info['catord'])==0:       # 0 = animal first, 1 = tool first (counterbalanced across subjects)
    stimS.append(stimSA)
    stimS.append(stimST)
    stimSAll = [i for i in itertools.chain.from_iterable(stimS)]
else:
    stimS.append(stimST)
    stimS.append(stimSA)
    stimSAll = [i for i in itertools.chain.from_iterable(stimS)]
stimS = []
stimS = stimSAll 

# Clock
clock = core.Clock()

# Set properties of the window
win = visual.Window(size=(1366, 768),fullscr=True, monitor="testMonitor", units="deg",allowStencil=False)
myMouse = event.Mouse(win=win)
myMouse.setVisible(0)                                                                       # Mouse not visible
 
# Other objects to be presented, not target stimuli
fixation = visual.TextStim(win, text='+')                                                   # Fixation

'''
====================================================
        Run the experiment
====================================================
'''

print("#" * 20 + "              Grab your towel              " + "#" * 20)

PresentGeneralInstruction(win)                                                                  # general instruction

task1 = []
task2 = []
task3 = []

task1 = RunTaskOne(win, stimP)                                                                  # task one is always the first one

# Check orderd of the tasks for this subject and run them

if int(exp_info['taskord'])==0:                  # 0 = 2 3 
    task2 = RunTaskTwo(win,stimS)
    task3 = RunTaskThree(win,stimS)
    
elif int(exp_info['taskord'])==1:                # 1 = 3 2
    task3 = RunTaskThree(win,stimS)
    task2 = RunTaskTwo(win,stimS)

else:
    core.quit() 


'''
====================================================
                End the experiment
====================================================
'''
Message(win, u'Cette session est terminÃ©e.')
WaitAnykey(win)

Message(win, u'Merci beaucoup!')
WaitAnykey(win)

# Save all data to a file
results_fname = 'taskone.csv'
results_fname = os.path.join(resultpath, results_fname)
taskone = pd.DataFrame(task1)
taskone.to_csv(results_fname, index=False, encoding = 'latin-1') 

results_fname = 'tasktwo.csv'
results_fname = os.path.join(resultpath, results_fname)
tasktwo = pd.DataFrame(task2)
tasktwo .to_csv(results_fname, index=False, encoding = 'latin-1')

results_fname = 'taskthree.csv'
results_fname = os.path.join(resultpath, results_fname)
taskthree = pd.DataFrame(task3)
taskthree.to_csv(results_fname, index=False, encoding = 'latin-1')


print("#" * 20 + "               You made it!               " + "#" * 20)

# Quit the experiment
core.quit() 
