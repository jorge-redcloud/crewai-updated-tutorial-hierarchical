from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import pprint

from analysis_engine import analyze_data
from tools.schema_tool import SchemaTool  # Correct import

app = Flask(__name__)

# ✅ CORS: allow any *.lovable.app domain
CORS(app, origins=[r"https://.*\.lovable\.app","http://localhost:3000"])

# ✅ Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


from flask import request, jsonify
import pandas as pd
import json
from tools.schema_tool import SchemaTool  # if you have it modularized

def group_conversation_logs(log_lines):
    grouped = []
    current_agent = "Unknown Agent"
    current_messages = []

    for entry in log_lines:
        line = entry.get("output", "").strip()

        # Detect agent line
        if line.startswith("🤖 Agent:"):
            # Save previous block
            if current_messages:
                grouped.append({
                    "agent": current_agent,
                    "output": "\n".join(current_messages),
                    "status": "log",
                    "task": "N/A"
                })
                current_messages = []

            # Update agent name
            current_agent = line.replace("🤖 Agent:", "").strip()
        else:
            current_messages.append(line)

    # Append last agent block
    if current_messages:
        grouped.append({
            "agent": current_agent,
            "output": "\n".join(current_messages),
            "status": "log",
            "task": "N/A"
        })

    return grouped

@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({"error": "No file provided"}), 400

    try:
        file = request.files['file']
        df = pd.read_csv(file)

        if df.empty:
            return jsonify({"error": "Uploaded CSV is empty."}), 400

        # ✅ 1. Generate schema markdown
        schema_tool = SchemaTool(df=df)
        schema_markdown = schema_tool._run()

        # ✅ 2. Run analysis
        crew_output = analyze_data(df)

        # ✅ 3. Parse final result
        result_text = crew_output.get("result", "")
        conversation_log = crew_output.get("conversation_log", "")
        conversation_thread = []

        # ✅ 4. Extract insights block from result
        try:
            if "```json" in result_text:
                insights_block = result_text.split("```json")[1].split("```")[0]
                insights_json = json.loads(insights_block)
            else:
                insights_json = {"raw_result": result_text}
        except Exception as parse_err:
            insights_json = {
                "error": f"Could not parse insights: {str(parse_err)}",
                "raw_result": result_text
            }

        # ✅ 5. Parse conversation log into displayable thread
        # Step 1: Capture the raw conversation
        conversation_log = crew_output.get("conversation_log", "")
        conversation_thread = []

        for line in conversation_log.splitlines():
            if line.strip():
                conversation_thread.append({
                    "agent": "unknown",
                    "task": "N/A",
                    "status": "log",
                    "output": line.strip()
                })

        # Step 2: Group and clean it
        conversation_thread = group_conversation_logs(conversation_thread)

        return jsonify({
            "message": "File processed and analyzed successfully",
            "data_schema_markdown": schema_markdown,
            "insights": insights_json,
            "conversation_thread": conversation_thread
        }), 200

    except pd.errors.ParserError:
        return jsonify({"error": "Invalid CSV format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ JSON-based analysis endpoint
@app.route("/analyze", methods=["POST"])
def analyze():
    json_data = request.get_json()
    if not json_data or "data" not in json_data:
        return jsonify({"error": "Missing 'data' field"}), 400

    try:
        insights = analyze_data(json_data["data"])
        return jsonify({"insights": insights}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/routes", methods=["GET"])
def list_routes():
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])

# ✅ Run server in env-aware mode
if __name__ == "__main__":
    env = os.getenv("environment", "development")  # 👈 make sure this matches Cloud Run's ENV var

    if env == "production":
        app.run(host="0.0.0.0", port=8080, debug=False)
    else:
        app.run(host="127.0.0.1", port=5001, debug=True)