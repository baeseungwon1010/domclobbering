from flask import Flask, request, render_template, jsonify
import subprocess

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
        payload = request.form.get("payload", "")
        if not payload:
            return "content required", 400

        # bot.py를 별도 프로세스로 실행하여 payload 전달
        subprocess.Popen(["python", "bot.py", "--payload", payload])

        return "관리자에게 전송되었습니다."

    return """
    <form method="post">
        <label>Payload (예: &lt;img src=x onerror=alert(1)&gt;)<br>
            <textarea name="content" rows="5" cols="60"></textarea>
        </label>
        <button type="submit">제출</button>
    </form>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
