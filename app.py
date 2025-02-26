from flask import Flask, request, jsonify
from vector_store import VectorStore

app = Flask(__name__)
store = VectorStore()

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query")
    results = store.search(user_query)
    return jsonify({"response": results if results else "No relevant info found."})

if __name__ == "__main__":
    app.run(debug=True)
