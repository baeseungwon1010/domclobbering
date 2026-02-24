from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/xss")
def xss():
    content = request.args.get("content", "")
    return jsonify({"content": content})


@app.route("/render")
def render():
    content = request.args.get("content", "")
    return jsonify({"content": content})


@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        url = request.form.get("url", "")
        if not url:
            return "url required", 400

        print(f"[DEBUG] Admin will visit: {url}")
        return "관리자에게 전송되었습니다. (실제 환경에서는 봇이 이 URL을 방문한다고 가정합니다)"

    return """
    <form method="post">
        <label>당신의 URL (예: http://localhost:5000/?content=...)<br>
            <input name="url" style="width:400px" />
        </label>
        <button type="submit">제출</button>
    </form>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

