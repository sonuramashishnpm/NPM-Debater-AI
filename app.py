from flask import Flask, render_template, request, jsonify, session
from npmai import Ollama, Memory
import uuid
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "48a35791177f22fba22b2cd08ad4436c1c4a1587b289ae9a75419280b934b7de")

# ───────────────────────────────────────────────
#  Exactly the same model instances & memories
# ───────────────────────────────────────────────
memory1 = Memory("llm1")
llm1 = Ollama(model="llama3.2", temperature=0.4)

memory2 = Memory("llm1")   # ← keeping your original naming
llm2 = Ollama(model="qwen2.5-coder:7b", temperature=0.5)

memory3 = Memory("llm1")
llm3 = Ollama(model="mistral:7b", temperature=0.5)

memory4 = Memory("llm1")
llm4 = Ollama(model="vicuna:7b", temperature=0.5)

# For simplicity we keep one shared topic per session
# (you can later extend to per-debate rooms if needed)

@app.route("/")
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template("debate.html")   # ← the HTML you got earlier


@app.route("/debate_step", methods=["POST"])
def debate_step():
    data = request.get_json()
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    # Load previous statements from memory (your original keys)
    history1 = memory1.load_memory_variables() or ""
    history2 = memory2.load_memory_variables() or ""
    history3 = memory3.load_memory_variables() or ""
    history4 = memory4.load_memory_variables() or ""

    # ───────────────────────────────
    #   Llama speaks first (starter or continuation)
    # ───────────────────────────────
    if not history4:  # first round
        prompt_llama = (
            f"You are starting a discussion and topic is:{topic} ,"
            f"in this discussion Qwen,Mistral,Vicuna is also here,"
            f"Instructions:-#be very-very-short and very-very-precise, "
            f"do not tag or reply in name of other models,"
            f"just put your point of view that should be very unique than other response,"
            f"no respond on instructions,complete your point in 100 word or less"
        )
    else:
        prompt_llama = (
            f"you are in a discussion on this topic:{topic},"
            f"in this discussion Qwen,Mistral,Vicuna is also here,"
            f"in this discussion you had said this points {history1} "
            f"try to put something new ,"
            f"Qwen said this {history2[-200:]}..., "   # truncate if too long
            f"Mistral said this {history3[-200:]}..., "
            f"Vicuna said this {history4[-200:]}..., "
            f"Instructions:-#be very-very-short and very-very-precise "
            f"and try to put something new in discussion, "
            f"do not tag or reply in name of other models,"
            f"just put your point of view that should be very unique than other response,"
            f"no respond on instructions,compelete your point in 100 word or less"
        )

    response = llm1.invoke(prompt_llama).strip()
    memory1.save_context("User not here you said in AI", response)

    # ───────────────────────────────
    #   Qwen
    # ───────────────────────────────
    prompt_qwen = (
        f"You are in a discussion on this topic :{topic},"
        f"in this discussion Mistral,Vicuna,Llama is also here, "
        f"where llama said this:{response},"
        f"in this discussion you had said these points {history2} "
        f"try to put something new , "
        f"Instructions:-#be very-very-short and very-very-precise "
        f"and try to put something new in discussion, "
        f"do not tag or reply in name of other models,"
        f"just put your point of view that should be very unique than other response,"
        f"no respond on instructions,complete your point in 100 word or less"
    )
    response2 = llm2.invoke(prompt_qwen).strip()
    memory2.save_context("User not here you said in AI", response2)

    # ───────────────────────────────
    #   Mistral
    # ───────────────────────────────
    prompt_mistral = (
        f"You are in discussion on this topic:{topic},"
        f"in this discussion Vicuna,Llama,Qwen is also here, "
        f"where llama said this{response} and Qwen said this {response2},"
        f"in this discussion you had said these points {history3} "
        f"try to put something new,"
        f"Instructions:-#be very-very-short and very-very-precise "
        f"and try to put something new in discussion, "
        f"do not tag or reply in name of other models,"
        f"just put your point of view that should be very unique than other response,"
        f"no respond on instructions,complete your point in 100 word or less"
    )
    response3 = llm3.invoke(prompt_mistral).strip()
    memory3.save_context("User not here you said in AI", response3)

    # ───────────────────────────────
    #   Vicuna (last)
    # ───────────────────────────────
    prompt_vicuna = (
        f"You are in a discussion on this topic:{topic},"
        f"in this discussion Llama,Qwen,Mistral is also here, "
        f"where llama said this {response} and Qwen said this {response2} "
        f"and Mistral said this {response3},"
        f"in this discussion you had said these points {history4} "
        f"try to put something new,"
        f"Instructions:-#be very-very-short and very-very-precise "
        f"and try to put something new in discussion, "
        f"do not tag or reply in name of other models,"
        f"just put your point of view that should be very unique than other response,"
        f"no respond on instructions,complete your point in 100 word or less"
    )
    response4 = llm4.invoke(prompt_vicuna).strip()
    memory4.save_context("User not here you said in AI", response4)

    # Return the four new statements (frontend appends them)
    return jsonify({
        "llama":   response,
        "qwen":    response2,
        "mistral": response3,
        "vicuna":  response4
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
