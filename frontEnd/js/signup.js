const form = document.getElementById("signup-form");

const checkPw = () => {
  const formData = new FormData(form);
  const pw1 = formData.get("password");
  const pw2 = formData.get("password2");
  if (pw1 === pw2) return true;
  else return false;
};

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  // 비밀번호 암호화하기
  const sha256Pw = sha256(formData.get("password"));
  formData.set("password", sha256Pw);
  const div = document.getElementById("info");

  //아이디 중복을 체크할것!!

  //비밀번호 체크
  if (checkPw()) {
    div.innerText = "";
    const res = await fetch("/signup", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    if (data === "200") {
      div.innerText = "가입이 완료되었습니다.";
      div.style.color = "blue";
      alert("회원가입에 성공했습니다."); //옛날방식이라 요즘은 쓰지 않음. 요즘은 토스트를 씀
      window.location.pathname = "/login.html";
    }
  } else {
    div.innerText = "비밀번호가 일치하지 않습니다.";
    div.style.color = "red";
  }
};

form.addEventListener("submit", handleSubmit);
