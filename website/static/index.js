function deleteRunner(runnerId) {
  fetch("/delete-runner", {
    method: "POST",
    body: JSON.stringify({ runnerId: runnerId }),
  }).then((_res) => {
    window.location.href = "/runner";
  });
}

