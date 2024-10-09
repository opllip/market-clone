const form = document.getElementById("login-form");

const handleLogin = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  // 비밀번호 암호화하기
  const sha256Pw = sha256(formData.get("password"));
  formData.set("password", sha256Pw);
  const div = document.getElementById("info");

  div.innerText = "";
  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  console.log(data);
  if (res.status === 200) {
    alert("로그인에 성공했습니다.");
    window.location.pathname = "/";
  } else if (res.status === 401) {
    alert("아이디 혹은 패스워드가 틀렸습니다.");
  }
};

form.addEventListener("submit", handleLogin);
