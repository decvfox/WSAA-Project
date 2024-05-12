function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


function deleteRunner(runnerId) {
  fetch("/delete-runner", {
    method: "POST",
    body: JSON.stringify({ runnerId: runnerId }),
  }).then((_res) => {
    window.location.href = "/runner";
  });
}

