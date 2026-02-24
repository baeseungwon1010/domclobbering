## DOM Clobbering CTF

- **서버 실행**
  - `pip install -r requirements.txt`
  - `python app.py`

- **문제 설명**
  - `/` 에서 `?content=...` 쿼리 스트링으로 전달되는 내용이 DOMPurify를 거친 뒤 출력됩니다.
  - 클라이언트 측 스크립트는 `/xss?content=...` 에서 받은 `content` 값을 환경 변수 `window.set.env` 에 따라 필터링 여부를 결정합니다.
  - DOM Clobbering 을 이용해 `window.set` 을 DOM 엘리먼트로 덮어써 `window.set.env !== "production"` 조건을 만족시키면 필터링 없이 `innerHTML` 로 삽입됩니다.

- **관리자 봇**
  - `bot.py` 는 Selenium 기반 관리자 봇 스크립트입니다.
  - `python bot.py "http://localhost:5000/?content=..."` 형식으로 실행합니다.
  - 플래그는 프로젝트 루트의 `flag.txt` 에서 읽어옵니다. (실패 시 기본값 사용)
  - 봇은 방문 전 `FLAG` 쿠키를 설정하고, 페이지에서 실행되는 JS에 의해 플래그가 탈취될 수 있습니다.

