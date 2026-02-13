from flask import Flask, render_template, request, jsonify, session, Response, stream_with_context
from npmai import Ollama, Memory
import json
import uuid
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "158bcd2e3f9b0e4b6a2db45fc48b461a65498478d0fbe9441fe0314bf534c23c")

llm1 = Ollama(model="llama3.2", temperature=0.85)

llm2 = Ollama(model="qwen2.5-coder:7b", temperature=0.75)

llm3 = Ollama(model="mistral:7b", temperature=0.80)

llm4 = Ollama(model="vicuna:7b", temperature=0.80)

@app.route("/")
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    if 'debate_topic' not in session:
        session['debate_topic'] = None
    return render_template("index.html")


@app.route("/debate_step", methods=["POST"])
def debate_step():
    memory1 = Memory("llm1")
    memory2 = Memory("llm2")
    memory3 = Memory("llm3")
    memory4 = Memory("llm4")
    
    data = request.get_json()
    topic_input = data.get("topic", "").strip()

    if topic_input:
        session['debate_topic'] = topic_input

    topic = session.get('debate_topic')
    if not topic:
        return jsonify({"error": "No topic set. Please enter a topic first."}), 400

    
    history1 = memory1.load_memory_variables() 
    history2 = memory2.load_memory_variables() 
    history3 = memory3.load_memory_variables() 
    history4 = memory4.load_memory_variables() 

    def generate():
        if not history4:
            response = llm1.invoke(f"You are starting a discussion and topic is:{topic} ,in this discussion Qwen,Mistral,Vicuna is also here,Instructions:-#be very-very-short and very-very-precise, do not tag or reply in name of other models,just put your point of view that should be very unique than other response,no respond on instructions,complete your point in 100 word or less")
            memory1.save_context("User not here you said in AI", response)
            yield json.dumps({"llama":response.strip()}) + "\n"
        else:
            response = llm1.invoke(f"you are in a discussion on this topic:{topic},in this discussion Qwen,Mistral,Vicuna is also here,in this discussion you had said this points {history1.split("AI: ")[-1].strip()} try to put something new ,Qwen said this {history2},Mistral said this {history3},Vicuna said this {history4} ,Instructions:-#be very-very-short and very-very-precise and try to put something new in discussion, do not tag or reply in name of other models,just put your point of view that should be very unique than other response,no respond on instructions,compelete your point in 100 word or less")
            memory1.save_context("User not here you said in AI", response)
            yield json.dumps({"llama":response.strip()}) + "\n"
            
        response2 = llm2.invoke(f"You are in a discussion on this topic :{topic},in this discussion Mistral,Vicuna,Llama is also here, where llama said this:{response},in this discussion you had said these points {history2.split("AI: ")[-1].strip()} try to put something new , Instructions:-#be very-very-short and very-very-precise and try to put something new in discussion, do not tag or reply in name of other models,just put your point of view that should be very unique than other response,no respond on instructions,complete your point in 100 word or less")
        memory2.save_context("User not here you said in AI", response2)
        yield json.dumps({"qwen":response2.strip()}) + "\n"
        
        response3 = llm3.invoke(f"You are in discussion on this topic:{topic},int this discussion Vicuna,Llama,Qwen is also here, where llama said this{response} and Qwen said this {response2},in this discussion you had said these points {history3.split("AI: ")[-1].strip()} try to put something new,Instructions:-#be very-very-short and very-very-precise and try to put something new in discussion, do not tag or reply in name of other models,just put your point of view that should be very unique than other response,no respond on instructions,complete your point in 100 word or less")
        memory3.save_context("User not here you said in AI", response3)
        yield json.dumps({"mistral":response3.strip()}) + "\n"

        response4 = llm4.invoke(f"You are in a discussion on this topic:{topic},in this discussion Llama,Qwen,Mistral is also here, where llama said this {response} and Qwen said this {response2} and Mistral said this {response3},in this discussion you had said these points {history4.split("AI: ")[-1].strip()} try to put something new,Instructions:-#be very-very-short and very-very-precise and try to put something new in discussion, do not tag or reply in name of other models,just put your point of view that should be very unique than other response,no respond on instructions,complete your point in 100 word or less")
        memory4.save_context("User not here you said in AI", response4)
        yield json.dumps({"vicuna":response4.strip()}) + "\n"
    
    # Return only the **new** statements (frontend appends them)
    return Response(stream_with_context(generate()),mimetype='application/x-ndjson')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
