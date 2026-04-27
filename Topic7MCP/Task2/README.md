## Topic7MCP - Task 2

### Discussion Questions

#### MCP vs A2A: How is sending a task to another agent different from calling an MCP tool? What can an agent do that a tool cannot?

Sending a task to another agent rather than calling a tool is different in that the agent is able to reason more deeply about how to approach the task, including what a reasonable out[ut might be given the context, whereas a tool call simply returns a value from a deterministic computation with no additional consideration about the best way top phrase or format its result. Agents are also more dynamic in their behavior than tools in that they can more reasdily adapt to unexpected behavior or edge-case scenarios. For example, in class we were able to ask our agents to reply with a funny, sarcastic answer if the question was outside of their scope of knowledge. A tool call that fails to retrieve a correct answer because the question is out of its scope would probably not be able to do this.

#### Discovery: We used a central registry. What are the alternatives? What are the tradeoffs of centralized vs decentralized discovery?

Using a central registry allowed us to limit the agents we could call to those from the class. This was useful as a classroom exercise, and could be useful in practice if there are only a specified number of agents that you want to be able to call for a particulasr task (e.g., they are very specialized or you trust them more than just any other agent). Decentralized discovery might also be useful, however, if you want to search through as many agents as possible to find the best agent for your task.

#### System prompts as strategy: How much did the system prompt matter for scoring? Could you craft a prompt that is good at all categories while still being funny on off-topic questions?

The system prompt is important in defining the scope of the agent's knowledge. Particularly when the agent is asked to be funny on off-topic questions, it is important for the model to know when a question is off-topic or not. An agent that performs well in all categories theoretically might never encounter an off-topc question if it is supposedly good at everything, but an agent that is good at *most* things might need additional specification of what it is **not** good at, so whenever it encounters a question outside of its already large scope, it knows how to recognize that the topic is outside of its scope and respond in a funny way.

#### Smart routing: TF-IDF matched questions to agents based on text overlap. What would happen with semantic embeddings instead? What if agents could self-report confidence?

#### Trust and reliability: In a real multi-agent system, how would you handle an agent that returns bad data? What if an agent is slow or goes offline mid-task?

#### Scaling: What would break if there were 1,000 agents instead of 20? What architectural changes would you need?
