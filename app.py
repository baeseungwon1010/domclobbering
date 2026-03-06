import os
from pathlib import Path
from flask import Flask, request, render_template

app = Flask(__name__)


def load_flag() -> str:
    flag_path = Path("flag.txt")
    if flag_path.exists():
        data = flag_path.read_text(encoding="utf-8").strip()
        if data:
            return data
    return os.environ.get("MY_FLAG", "CTF{DUMMY_FLAG}")


@app.route("/")
def index():
    content = request.args.get("content", "")
    return render_template("index.html", content=content)


@app.route("/submit", methods=["POST"])
def submit():
    allowed_ips = {"127.0.0.1", "::1"}
    remote_ip = request.remote_addr or ""
    if remote_ip not in allowed_ips:
        return "forbidden", 403
    user_name = request.form.get("userName", "").strip()
    random_key = request.form.get("randomKey", "").strip()

    flag = None
    if random_key == "100000000":
        flag = load_flag()

    score = random_key

    # 간단한 결과 페이지
    return f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>HTML 평가 결과</title>
        <style>
            body {{ font-family: sans-serif; margin: 30px; }}
            .score {{ font-size: 20px; margin-top: 20px; }}
            .flag {{ margin-top: 20px; color: red; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>당신의 HTML 평가 결과</h1>
        <p>참가자 이름: {user_name or "익명"}</p>
        <p class="score">평가 점수: {score} 점</p>
        {"<p class='flag'>축하합니다! FLAG: " + flag + "</p>" if flag else ""}
        <p><a href="/">다시 도전하기</a></p>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)

