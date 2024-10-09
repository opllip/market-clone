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
    }
  } else {
    div.innerText = "비밀번호가 일치하지 않습니다.";
    div.style.color = "red";
  }
};

form.addEventListener("submit", handleSubmit);
