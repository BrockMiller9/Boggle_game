$("form").on("submit", handleSubmit);
let score = 0;

let words = [];
let time = 60;
$("#timer").html(time);
async function handleSubmit(e) {
  e.preventDefault();
  // create a variable that equals the word submitted through the form
  let word = $("input").val();

  // do nothing if the form is empty
  if (!word) return;
  // send this word to the 'server' to have it check if it is an appropriate response.
  const res = await axios.get("/check-word", { params: { word: word } });
  let response = res.data.response;

  console.log(response);
  //   display response in DOM
  $("#response").html(response);

  // reset form
  $("form").trigger("reset");
  if (response === "ok") {
    if (words.includes(word)) {
      return;
    }
    words.push(word);
    score += word.length;
    $("#score").html(`Score: ${score}`);
  }
}

let countDown = setInterval(function () {
  // subtract one from time variable
  time--;
  $("#timer").html(time);
  stopTimer();
}, 1000);

function stopTimer() {
  if (time < 1) {
    clearInterval(countDown);
    $("form").hide();
    $(".container").append($("<span>").html("GAME OVER"));
    endGame();
  }
}

async function endGame() {
  await axios.post("/end-game", { score: score });
}
