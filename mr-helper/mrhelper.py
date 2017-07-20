import nltk
import re

class MrHelper(object):

    grammar = r"""
	TP: {(<IN>|<RB>)<CD>(<TO><CD>)?}
	TODO_PHRASE: {<PRP><MD>?<VB.?>+?<TO>?<DT>?}
	AFTER_PHRASE: {<WRB><TODO_PHRASE>}
	"""

    chunk_parser = nltk.RegexpParser(grammar, loop=2)

    def __init__(self):
        pass

    def AddToSchedule(action, time):
		

    def RespondToInput(self, user_input):
	has_todo = (False, False)
	has_time = (False, False)

        tokenized_input = nltk.word_tokenize(user_input)
        tagged_input = nltk.pos_tag(tokenized_input)
	chunked_input = self.chunk_parser.parse(tagged_input)

	# This is so hacky why am I doing this
	for i, subtree in enumerate(chunked_input.subtrees()):
	    if subtree.label() == "TODO_PHRASE":
		print(subtree)
		del chunked_input[i - 1]
	        has_todo = (True, chunked_input)

	if has_todo[0]:
	    for i, subtree in enumerate(has_todo[1].subtrees()):
		if subtree.label() == "TP":
		    has_time = (True, subtree.leaves())

		    real_todo = has_todo[1].leaves() 
		    for thing in has_time[1]:
			real_todo.remove(thing)

		    AddToSchedule(real_todo, has_time[1])
		    return "Okay, I've added '" + " ".join(item[0] for item in real_todo) + "' to your schedule " + " ".join(item[0] for item in has_time[1]) + "."
	
        return "I'm sorry, I didn't understand what you said."
        
