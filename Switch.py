# Spanning Tree project for GA Tech OMS-CS CS 6250 Computer Networks
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To 
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm - 
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

from Message import *
from StpSwitch import *


class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors): #Custom Constructor
    	#s1 = Switch(01,1,2)
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)

        # TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.

    	self.root = self.switchID #Seen as the root
    	self.distance = 0 #Distance to the switch's root
    	self.activeLinksList = [] #list that stores active links
    	self.switchThrough = self.switchID #keeps track of which neighbor it goes through to get to the root

    def send_initial_messages(self):
        # TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
        #      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        #		Do not define data structure here since it'll be overwritten every time the switch class is called
        #		All switches send their initial messages and push them tio the queue
        for destinationNeighbor in self.links:
        	message = Message(self.switchID,0,self.switchID,destinationNeighbor,False) #Message(claimedRoot, distanceToRoot, originID, destinationID, paththrough) 
        	self.send_message(message) #Sends msg to the queue-> EX: root = 1, distance = 0, origin = 1, destination - 2, path = False
        return

    def process_message(self, message):
        # TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.

        #Scenario 1) if message's root id is lower then self.root
        if message.root < self.root:
            self.root = message.root
            self.distance = message.distance + 1
            if message.origin not in self.activeLinksList:
                self.activeLinksList.append(message.origin)
            self.switchThrough = message.origin
        	
            for destinationNeighbor in self.links:
                message = Message(self.root,self.distance,self.switchID,destinationNeighbor,message.origin == destinationNeighbor)
                self.send_message(message)

        #Scenario 2) same root but shorter distance to the root
        if message.root == self.root and message.distance + 1 < self.distance:
            self.distance = message.distance + 1
            self.activeLinksList.remove(self.switchThrough)
            if message.origin not in self.activeLinksList:
                self.activeLinksList.append(message.origin)
            self.switchThrough = message.origin
        	
            for destinationNeighbor in self.links:
                message = Message(self.root,self.distance,self.switchID,destinationNeighbor,self.switchThrough == destinationNeighbor)
                self.send_message(message)
        
        #Scenario 3) same root, same distance but use lower switchID to get to the root
        if message.root == self.root and message.distance + 1 == self.distance and message.origin < self.switchThrough:
        	self.activeLinksList.remove(self.switch)
        	self.switchThrough = message.origin

        	for destinationNeighbor in self.links:
        		message = Message(self.root,self.distance,self.switchID,destinationNeighbor,self.switchThrough == destinationNeighbor)
        		self.send_message(message)
        #Scenario 4)
        if message.pathThrough:
            if message.origin not in self.activeLinksList:
        	    self.activeLinksList.append(message.origin)
        elif message.pathThrough == False:
            if message.origin in self.activeLinksList:
                self.activeLinksList.remove(message.origin)

        return

    def generate_logstring(self):
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      Print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.

        joinLinks = []
        self.activeLinksList.sort()
        for destinationNeighbor in self.activeLinksList:
            joinLinks.append(str(self.switchID)+ "-" + str(destinationNeighbor))
        return ', '.join(joinLinks)

