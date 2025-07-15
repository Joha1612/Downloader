const API_URL = "https://your-render-url.onrender.com/get_info"; // Replace this

document.getElementById("urlForm").onsubmit = async (e) => {
  e.preventDefault();
  const url = document.getElementById("url").value;
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: "url=" + encodeURIComponent(url)
  });
  const data = await res.json();
  if (data.success) {
    const info = data.info;
    document.getElementById("title").innerText = info.title;
    document.getElementById("thumbnail").src = info.thumbnail;
    const tbody = document.getElementById("formatsBody");
    tbody.innerHTML = "";
    info.formats.forEach(f => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${f.ext.toUpperCase()}</td>
        <td>${f.resolution}</td>
        <td>${f.filesize} MB</td>
        <td><a href="${f.url}" target="_blank">Download</a></td>
      `;
      tbody.appendChild(row);
    });
    document.getElementById("videoInfo").style.display = "block";
  } else {
    alert("Error: " + data.error);
  }
};
