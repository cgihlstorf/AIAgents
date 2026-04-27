## Topic7MCP - Task 2

### Discussion Questions

#### MCP vs A2A: How is sending a task to another agent different from calling an MCP tool? What can an agent do that a tool cannot?

Sending a task to another agent rather than calling a tool is different in that the agent is able to reason more deeply about how to approach the task, including what a reasonable out[ut might be given the context, whereas a tool call simply returns a value from a deterministic computation with no additional consideration about the best way top phrase or format its result. Agents are also more dynamic in their behavior than tools in that they can more reasdily adapt to unexpected behavior or edge-case scenarios. For example, in class we were able to ask our agents to reply with a funny, sarcastic answer if the question was outside of their scope of knowledge. A tool call that fails to retrieve a correct answer because the question is out of its scope would probably not be able to do this.

#### Discovery: We used a central registry. What are the alternatives? What are the tradeoffs of centralized vs decentralized discovery?

Using a central registry allowed us to limit the agents we could call to those from the class. This was useful as a classroom exercise, and could be useful in practice if there are only a specified number of agents that you want to be able to call for a particulasr task (e.g., they are very specialized or you trust them more than just any other agent). Decentralized discovery might also be useful, however, if you want to search through as many agents as possible to find the best agent for your task.

#### System prompts as strategy: How much did the system prompt matter for scoring? Could you craft a prompt that is good at all categories while still being funny on off-topic questions?

The system prompt is important in defining the scope of the agent's knowledge. Particularly when the agent is asked to be funny on off-topic questions, it is important for the model to know when a question is off-topic or not. An agent that performs well in all categories theoretically might never encounter an off-topc question if it is supposedly good at everything, but an agent that is good at *most* things might need additional specification of what it is **not** good at, so whenever it encounters a question outside of its already large scope, it knows how to recognize that the topic is outside of its scope and respond in a funny way.

#### Smart routing: TF-IDF matched questions to agents based on text overlap. What would happen with semantic embeddings instead? What if agents could self-report confidence?

Semantic embeddings would likely offer a more meaningful comparison between questions and agents because the embeddings store information about word order patterns, which approximates the "meaning" of a word as opposed to simply checking for an overlap score. Self-reported confidence could offer another method of checking the validity of a match. Assuming an agent's self-reported confidence scores actually align with the ground-truth similarity (which does not seem to always be the case, according to past research in this area), results could be filtered not only by overlap or semantic similarity, but by model confidence as well, which could aid in resolving ties between results with similar overlap or semantic similarity by preferring the result that the model is more confident in.

#### Trust and reliability: In a real multi-agent system, how would you handle an agent that returns bad data? What if an agent is slow or goes offline mid-task?

In a real-world scenario, it might be beneficial to assign one or multiple "backup" agents if the agent you choose to perform a task returns bad results. This way, the task can be re-assigned to the other agent(s), hopefully resulting in minimal interruptions to the process. If none of these agents return good results, or no other suitable agents are available, it may be worth hard-coding some condition that returns a message stating that the task failed or that the result was unreliable, so you can be notified of the occurrance before it affects other parts of the process. A similar framework might be applied if an agent is slow or goes offline mid-task. After a certain amount of time has ellapsed without a result, or if the agent goes offline, the task could then be shifted to another agent in the "backup" queue, or, if such a queue is exhausted or unavailable, a message can be returned explaining that the process could not be completed, which will hopefully be helpful in communication with other agents that that specific task could not be performed so they can respond accordingly. 

#### Scaling: What would break if there were 1,000 agents instead of 20? What architectural changes would you need?

With 1,000 agents instead of 20, I imagine there might be more computational strain on the trivia tournament agent in terms of having to go through all agents, compute similarity, score answers, and sort results. One potential fix is having the agent sort results as it goes through the answers so that it does not have to sort all 1,000 responses and scores at once. 

