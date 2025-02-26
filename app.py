from flask import Flask, request, jsonify
from vector_store import VectorStore

app = Flask(__name__)
store = VectorStore()
store.load_pdfs("pdfs")  # Load all PDFs at startup

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query")
    cdp_filter = request.json.get("cdp")  # Optional CDP filter

    results = store.search(user_query, cdp_filter=cdp_filter)
    

    formatted_results = [
        {
            "cdp": res["cdp"],
            "text": res["text"],
            "source": res.get("source", "Unknown")  # Ensure source exists
        }
        for res in results
    ]

    return jsonify({"response": formatted_results})

if __name__ == "__main__":
    app.run(debug=True)
