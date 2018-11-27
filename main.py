import sys, os, argparse, re, subprocess, wikipedia, json, pprint


class FactoidQuesGenerator():

	def __init__(self, input_file=None):
		if input_file:
			print ("Taking file %s as input" % (input_file))
			self.input_file = input_file
		currDirName = os.path.dirname(os.path.realpath(__file__))
		os.chdir(os.path.join(currDirName, 'JavaBackend'))

	def get_rawOutput(self, input_sentence):
		# This function invokes the QuestionGenerator Java class to generate questions given a declarative statement.
		# input_sentence is the declarative statement that needs to be converted to a question

		# Runs the command "java -Xmx1200m -cp question-generation.jar edu/cmu/ark/QuestionAsker --verbose --model models/linear-regression-ranker-reg500.ser.gz --prefer-wh --max-length 30 --downweight-pro"
		p = subprocess.Popen(['bash', 'run.sh'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

		output = p.communicate(input=input_sentence)[0]
		return output.decode() # Return format is question followed by answer followed by score

	def generate_question(self, sentence):
		# The main method that generates a question for a single sentence

		output = self.get_rawOutput(bytearray(sentence, 'utf-8'))
		try:
			quest_ans_pairs = output.split('\n')[3:]
		except:
			exit('No questions detected. Please try a different sentence.')

		question_types = ['Wh', 'Are', 'How', 'Do']
		results = []

		for qType in question_types:
			regexStr = r"{}\w+|\W\?".format(qType)
			for quest_ans in quest_ans_pairs:
				if re.match(regexStr, quest_ans):
					qa_tuple = quest_ans.split('\t')
					question, sent, answer, score = qa_tuple[0], qa_tuple[1], qa_tuple[2], qa_tuple[3]
					results.append({'Sentence': sent, "Question": question, 'Answer': answer, 'Score': score})

		return results # Returns an array of length (question_types)

def add_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '-sentence', type=str, help="The sentence for which questions are to be generated.")
	parser.add_argument('-t', '-question_type', type=str, default=['Wh', 'Are', 'Who', 'Do'], choices=['Wh', 'Are', 'Who', 'Do', 'All'], help='The types of questions to be generated.')
	return parser.parse_args()

def data(topic):
	page=wikipedia.page(topic)
	return page.content

def getWikiArticle(topic, number=10):
	x=data(topic).split('\n')
	blocks=[]
	for i in x:
		if i and not "=" in i:
			blocks.append(i)
			
	sentences=[]
	for i in blocks:
		sentences+=i.split(".")
	return sentences[:number]

q  = FactoidQuesGenerator()

while True:
	qType = input("Enter input type (W for wikipedia, S for sentence): ")

	if qType == "W":
		topic = input("Enter topic: ")
		sentences = getWikiArticle(topic)
	elif qType == "S":
		sentence = input("Enter sentence: ")
		sentences = [sentence]
	else:
		print("Invalid question type")
		continue

	final = []
	for sentence in sentences:
		question_list = q.generate_question(sentence)
		final.extend(question_list)

	outputDict = {}

	for qa in final:
		if qa['Sentence'] in outputDict:
			outputDict[qa['Sentence']].append({"Question": qa['Question'], "Answer": qa['Answer'], "Score": qa['Score']})
		else:
			outputDict[qa['Sentence']] = [{"Question": qa['Question'], "Answer": qa['Answer'], "Score": qa['Score']}]

	output = [{elem: sorted(outputDict[elem], key=lambda k: float(k['Score']))} for elem in outputDict]

	outputDict = json.loads(json.dumps(outputDict))

	with open("../output.json","w") as f:
		json.dump(outputDict, f, indent=4)
