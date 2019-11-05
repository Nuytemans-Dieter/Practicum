# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0
    return answerDiscount, answerNoise



# Prefer the close exit (+1), risking the cliff (-10)
def question3a():
    answerDiscount = 0.1        # Gamma value: lower discount means closer goals will be considered to be worth more (each step ^2)
    answerNoise = 0             # The chance that the agent makes a different choice than its policy
    answerLivingReward = 0      # The reward or penalty offered at each move
    return answerDiscount, answerNoise, answerLivingReward



# Prefer the close exit (+1), but avoiding the cliff (-10)
def question3b():
    answerDiscount = 0.1		# Low gamma value is needed: prefer close exit
    answerNoise = 0.1 			# Noise may make the agent move into the cliff: the agent prevents this by taking the top route
    answerLivingReward = 0      # No reward is required
    return answerDiscount, answerNoise, answerLivingReward



# Prefer the distant exit (+10), risking the cliff (-10)
def question3c():
    answerDiscount = 0.1		# Only a small penalty for moving further: goals that are far away are desired
    answerNoise = 0 			# No noise, else the cliff is too dangerous for the agent
    answerLivingReward = 5	    # Give the agent a reward for moving further
    return answerDiscount, answerNoise, answerLivingReward



# Prefer the distant exit (+10), avoiding the cliff (-10)
def question3d():
    answerDiscount = None
    answerNoise = 0 			# Random actions are not desired
    answerLivingReward = None
    return answerDiscount, answerNoise, answerLivingReward



# Avoid both exits and the cliff (so an episode should never terminate)
def question3e():
    answerDiscount = None
    answerNoise = 0 			# Random actions are not desired
    answerLivingReward = None
    return answerDiscount, answerNoise, answerLivingReward

def question8():
    answerEpsilon = None
    answerLearningRate = None

    return 'NOT POSSIBLE'
    # There is no combination of values for which the optimal policy will be learned.

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
