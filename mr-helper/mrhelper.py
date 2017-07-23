from datetime import datetime 
from datetime import timedelta
import dateparser
import math
import re
import nltk
from third_party import text2int

class MrHelper(object):

    grammar = r"""
	TP: {(<IN><NN>)?(<IN>|<RB>)(<DT>)?<CD>(<NN(S|P)?>)?(<IN><NN(S)?>)?}
	TODO_PHRASE: {<PRP><MD>?<VB.?>+?<TO>?<DT>?}
	"""

	#AFTER_PHRASE: {<WRB><TODO_PHRASE>}

    chunk_parser = nltk.RegexpParser(grammar, loop=2)

    schedule = [[]]
    state = "IDLE"

    def __init__(self):
        with open("schedule_file") as schedule_reader:
            i = 0
            for line in schedule_reader:
                if line.rstrip() != "---":
                    self.schedule[i].append(line.rstrip())
                else:
                    self.schedule.append([])
                    i += 1

    def WriteToSchedule(self, parsed_input):
        self.schedule.append([parsed_input[0], parsed_input[1]])
        with open("schedule_file", "a") as schedule_writer:
            schedule_writer.write("---\n")
            schedule_writer.write(" ".join([x[0] for x in parsed_input[0]]) + "\n")
            schedule_writer.write(parsed_input[1].strftime("%c") + "\n")


    def RespondToInput(self, user_input):
        tokenized_input = nltk.word_tokenize(text2int(user_input))
        tagged_input = nltk.pos_tag(tokenized_input)
	chunked_input = self.chunk_parser.parse(tagged_input)

        if self.state == "IDLE":
            parsed_input = (None, None)
            for chunk in chunked_input.subtrees():
                print(chunk)
                if chunk.label() == "TODO_PHRASE":
                    parsed_input = ([x for x in chunked_input.leaves() if x not in chunk.leaves()], parsed_input[1])
                if chunk.label() == "TP":
                    parsed_input = ([x for x in parsed_input[0] if x not in chunk], dateparser.parse(" ".join([x[0] for x in chunk.leaves() if x[1] is not "IN"])))
                    if parsed_input[1] is None:
                        self.temp = parsed_input
                        return "Sorry, I wasn't able to understand that date format. Try structuring it like this: at <time> on <day>."
                    if parsed_input[1] < datetime.now():
                        return "I think that was in the past. Can you tell me that again? Try structuring it like this: at <time> on <day>."

            if parsed_input[0] is not None:
                if parsed_input[1] is not None:
                    print(parsed_input)
                    self.WriteToSchedule(parsed_input)
                    return "Adding " + " ".join([x[0] for x in parsed_input[0]]) + " to your schedule for " + parsed_input[1].strftime("%c") + "."
                else:
                    return "Sorry, you didn't give me a date. Can you tell me that again? Try structuring it like this: at <time> on <day>."
	
        return "I'm sorry, I didn't understand that. Try again please?"
