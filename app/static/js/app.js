// Add event listerners for type of quiz
document.addEventListener('DOMContentLoaded', function() {
  let randomQuizForm = document.getElementById("random-quiz");
  let customizedQuizForm = document.getElementById("custom-quiz");
  let existingQuizForm = document.getElementById("existing-quiz");
  let quizForm = document.getElementById('quiz-form')

  // Random quiz
  if(randomQuizForm)
  {
    randomQuizForm.addEventListener('submit', function(event) {
      event.preventDefault();
      randomQuiz();
    });
  }

  // Custom quiz
  if (customizedQuizForm) {
    customizedQuizForm.addEventListener("submit", function(event) {
      event.preventDefault();
      customQuiz();
    });
  }

  // Existing quiz
  if (existingQuizForm) {
    existingQuizForm.addEventListener('submit', function(event) {
      event.preventDefault();
      existingQuiz();
    });
  }

  if (quizForm) {
    quizForm.addEventListener('submit', function(event) {
      event.preventDefault();
      quiz();
    })
  }
  
});

// Quiz generation: Handle random Quiz
function randomQuiz() {
  const selectQuestionCount = document.getElementById('question-count');
  const numberOfQuestions = selectQuestionCount.value;

  axios.post('/api/quiz', {
    question_count: numberOfQuestions
  })
  .then(function(response) {
    if (response.data.redirect_url) {
      window.location.href = response.data.redirect_url;
      
    } else {
      console.error("Error while creating quiz ", response.data.message);
    }

  })
  .catch(function(error) {
    // Handle error response
    if (error.response) {
      // Server responded with a status other than 2xx
      console.error('Error:', error.response.data.message);
    } else if (error.request) {
      // Request was made but no response was received
      console.error('No response received:', error.request);
    } else {
      // Something happened in setting up the request
      console.error('Error setting up request:', error.message);
    }
  });

}

// Quiz generation: Handle custom Quiz
function customQuiz() {
  const selectCategory = document.getElementById('category');
  const selectDifficulty = document.getElementById('difficulty');
  const selectQuestionCount = document.getElementById('question-count');
  const selectType = document.getElementById('quiz-type');

  const quizCategory = selectCategory.value;
  const quizDifficulty = selectDifficulty.value;
  const numberOfQuestions = selectQuestionCount.value;
  const quizType = selectType.value;

  axios.post('/api/quiz', {
    quiz_category: quizCategory,
    quiz_difficulty: quizDifficulty,
    question_count: numberOfQuestions,
    quiz_type: quizType
  })
  .then(function(response) {
    if (response.data.redirect_url) {


      window.location.href = response.data.redirect_url;
      
    } else {
      console.error("Error while creating quiz ", response.data.message);
    }

  })
  .catch(function(error) {
    // Handle error response
    console.log(error);
  })
  
}

// Quiz generation: Handle existing quizes
function existingQuiz() {
  const selectCategory = document.getElementById('category');
  const selectDifficulty = document.getElementById('difficulty');
  const selectQuestionCount = document.getElementById('question-count');
  const selectType = document.getElementById('quiz-type');

  const quizCategory = selectCategory.value;
  const quizDifficulty = selectDifficulty.value;
  const numberOfQuestions = selectQuestionCount.value;
  const quizType = selectType.value;

  axios.post('/api/quiz', {
    quiz_category: quizCategory,
    quiz_difficulty: quizDifficulty,
    question_count: numberOfQuestions,
    quiz_type: quizType
  })
  .then(function(response) {
    if (response.data.redirect_url) {
      window.location.href = response.data.redirect_url;
      console.log(response.data);
    } else {
      console.error("Error while creating quiz ", response.data.message);
    }

  })
  .catch(function(error) {
    // Handle error response
    console.log(error);
  })
}

// Handle Quiz
function quiz() {
  
}

const questions = [
    {
      category: "Animals",
      correct_answer: "False",
      difficulty: "medium",
      incorrect_answers: ["True"],
      question: "The Ceratosaurus, a dinosaur known for having a horn on the top of its nose, is also known to be a descendant of the Tyrannosaurus Rex.",
      type: "boolean"
    },
    {
      category: "History",
      correct_answer: "Navarre",
      difficulty: "hard",
      incorrect_answers: ["Galicia", "Granada", "Catalonia"],
      question: "The coat of arms of the King of Spain contains the arms from the monarchs of Castille, Leon, Aragon and which other former Iberian kingdom?",
      type: "multiple"
    },
    {
      category: "Entertainment: Video Games",
      correct_answer: "Ossan",
      difficulty: "medium",
      incorrect_answers: ["Jumpman", "Mr. Video", "Mario"],
      question: "What name did \"Mario\", from \"Super Mario Brothers\", originally have?",
      type: "multiple"
    },
    {
      category: "Entertainment: Music",
      correct_answer: "The Beatles (White Album)",
      difficulty: "easy",
      incorrect_answers: ["Rubber Soul", "Abbey Road", "Magical Mystery Tour"],
      question: "Which Beatles album does NOT feature any of the band members on its cover?",
      type: "multiple"
    },
    {
      category: "Entertainment: Video Games",
      correct_answer: "Piplup",
      difficulty: "easy",
      incorrect_answers: ["Totodile", "Oshawott", "Mudkip"],
      question: "Which water-type Pokémon starter was introduced in the 4th generation of the series?",
      type: "multiple"
    },
    {
      category: "Entertainment: Board Games",
      correct_answer: "True",
      difficulty: "hard",
      incorrect_answers: ["False"],
      question: "The board game Go has more possible legal positions than the number of atoms in the visible universe.",
      type: "boolean"
    },
    {
      category: "Entertainment: Video Games",
      correct_answer: "Lionel Messi",
      difficulty: "medium",
      incorrect_answers: ["Cristiano Ronaldo", "Wayne Rooney", "David Beckham"],
      question: "Which football player is featured on the international cover version of the video game FIFA 16?",
      type: "multiple"
    },
    {
      category: "Entertainment: Video Games",
      correct_answer: "Contraband",
      difficulty: "easy",
      incorrect_answers: ["Discontinued", "Diminshed", "Limited"],
      question: "In Counter-Strike: Global Offensive, what's the rarity of discontinued skins called?",
      type: "multiple"
    },
    {
      category: "Science & Nature",
      correct_answer: "4",
      difficulty: "medium",
      incorrect_answers: ["3", "5", "6"],
      question: "In Chemistry, how many isomers does Butanol (C4H9OH) have?",
      type: "multiple"
    },
    {
      category: "Entertainment: Music",
      correct_answer: "True",
      difficulty: "easy",
      incorrect_answers: ["False"],
      question: "Scatman John's real name was John Paul Larkin.",
      type: "boolean"
    }
  ];


  // let currentQuestionIndex = 0;
  // let score = 0;
  // const userAnswers = [];

  // function shuffle(array) {
  //   let currentIndex = array.length, randomIndex;
  //   while (currentIndex != 0) {
  //     randomIndex = Math.floor(Math.random() * currentIndex);
  //     currentIndex--;
  //     [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
  //   }
  //   return array;
  // }

  // function loadQuestion(index) {
  //   const question = questions[index];
  //   document.getElementById('question-title').textContent = `Question ${index + 1}`;
  //   document.getElementById('question-text').textContent = question.question;
  //   const answersDiv = document.getElementById('answers');
  //   answersDiv.innerHTML = '';

  //   const allAnswers = [...question.incorrect_answers, question.correct_answer];
  //   if (question.type === "multiple") {
  //     shuffle(allAnswers);
  //   } else if (question.type === "boolean") {
  //     shuffle(allAnswers);
  //   }

  //   allAnswers.forEach((answer) => {
  //     const label = document.createElement('label');
  //     label.classList.add('list-group-item');
  //     label.innerHTML = `<input type="radio" name="answer" value="${answer}"> ${answer}`;
  //     answersDiv.appendChild(label);
  //   });

  //   if (userAnswers[index] !== undefined) {
  //     document.querySelector(`input[name="answer"][value="${userAnswers[index]}"]`).checked = true;
  //   }
  // }

  // function showResult() {
  //   document.getElementById('quiz-container').classList.add('d-none');
  //   document.getElementById('result-container').classList.remove('d-none');
  //   document.getElementById('score-text').textContent = `Your score: ${score}/${questions.length}`;
  //   if (userAnswers.length === questions.length) {
  //     document.getElementById('view-answers-btn').style.display = 'block';
  //   }
  // }

  // document.getElementById('next-btn').addEventListener('click', () => {
  //   const selectedAnswer = document.querySelector('input[name="answer"]:checked');
  //   if (selectedAnswer !== null) {
  //     if (selectedAnswer.value === questions[currentQuestionIndex].correct_answer) {
  //       score++;
  //     }
  //     userAnswers[currentQuestionIndex] = selectedAnswer.value;
  //   }

  //   if (currentQuestionIndex < questions.length - 1) {
  //     currentQuestionIndex++;
  //     loadQuestion(currentQuestionIndex);
  //     document.getElementById('prev-btn').style.display = 'block';
  //   } else {
  //     showResult();
  //   }
  // });

  // document.getElementById('prev-btn').addEventListener('click', () => {
  //   if (currentQuestionIndex > 0) {
  //     currentQuestionIndex--;
  //     loadQuestion(currentQuestionIndex);
  //     if (currentQuestionIndex === 0) {
  //       document.getElementById('prev-btn').style.display = 'none';
  //     }
  //   }
  // });

  // document.getElementById('retry-btn').addEventListener('click', () => {
  //   currentQuestionIndex = 0;
  //   score = 0;
  //   userAnswers.length = 0;
  //   document.getElementById('quiz-container').classList.remove('d-none');
  //   document.getElementById('result-container').classList.add('d-none');
  //   loadQuestion(currentQuestionIndex);
  //   document.getElementById('prev-btn').style.display = 'none';
  //   document.getElementById('next-btn').style.display = 'block';
  //   document.getElementById('view-answers-btn').style.display = 'none';
  // });

  // document.getElementById('view-answers-btn').addEventListener('click', () => {
  //   let resultHTML = '<div class="card-body"><h5 class="card-title">Quiz Answers</h5>';
  //   questions.forEach((question, i) => {
  //     resultHTML += `<h5>Question ${i + 1}</h5><p>${question.question}</p>`;
  //     const allAnswers = [...question.incorrect_answers, question.correct_answer];
  //     shuffle(allAnswers);
  //     allAnswers.forEach(answer => {
  //       const correctClass = question.correct_answer == answer ? 'text-success' : '';
  //       const userClass = userAnswers[i] == answer ? 'font-weight-bold' : '';
  //       if (question.correct_answer === answer) {
  //         resultHTML += `<p class="${correctClass}">${answer} <span class="text-muted">(Correct)</span></p>`;
  //       } else {
  //         resultHTML += `<p class="${userClass}">${answer}</p>`;
  //       }
  //     });
  //   });
  //   resultHTML += '</div>';
  //   document.getElementById('result-container').innerHTML = resultHTML;
  // });

  // // Initialize the quiz
  // loadQuestion(currentQuestionIndex);

 