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
  const accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken); //로컬스토리지에 저장 -브라우저를 닫고 다시 켜도 남아있음
  //window.sessionStorage.setItem("token", accessToken); //세션에 저장 -브라우저를 닫고 다시 키면 없어져있음
  console.log(accessToken);

  //   div.innerText = "로그인되었습니다.";
  //   const btn = document.createElement("button");
  //   btn.innerText = "상품 가져오기!";
  //   btn.addEventListener("click", async () => {
  //     const res = await fetch("/items", {
  //       headers: {
  //         Authorization: `Bearer ${accessToken}`,
  //         // Bearer : access token을 쓸 때 쓰는 prfix
  //       },
  //     });
  //     const data = await res.json();
  //     console.log(data);
  //   });
  //   div.appendChild(btn);

  if (res.status === 200) {
    alert("로그인에 성공했습니다.");
    window.location.pathname = "/";
  } else if (res.status === 401) {
    alert("아이디 혹은 패스워드가 틀렸습니다.");
  }
};

form.addEventListener("submit", handleLogin);
