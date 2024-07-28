// Add a generic function for quiz type
function addQuizFormListener(formId, submitFunction) {
  const quizForm = document.getElementById(formId);
  if (quizForm) {
    quizForm.addEventListener ('submit', function(event) {
      event.preventDefault();
      submitFunction(); // call the specific function for this quiz
    });
  }
}
// Add event listerners for type of quiz
document.addEventListener('DOMContentLoaded', function() {
  addQuizFormListener("random-quiz", randomQuiz);
  addQuizFormListener("custom-quiz", customQuiz);
  addQuizFormListener("existing-quiz", existingQuiz);
  addQuizFormListener('quiz-form', submitQuiz);

  const numberOfQuestions = localStorage.getItem('numberOfQuestions');
  const quizType = localStorage.getItem('quizType');
  const quiz_questions = JSON.parse(localStorage.getItem('quiz_questions'));
  const courseForm = document.getElementById('courseForm');
  const quizResultsPage = document.getElementById('quiz-results');
  const finishQuizTrigger = document.getElementById('finish-quiz');

  if (quizResultsPage) {
    quizResults();
  }
  if (finishQuizTrigger) {
    finishQuizTrigger.addEventListener('click', function(event) {
      event.preventDefault();
      finishQuiz();
    })
  }

  
  if (courseForm) {
    if (numberOfQuestions && quiz_questions && quizType) {
      console.log('Number of Questions:', numberOfQuestions);
      console.log('Quiz Questions:', quiz_questions);
      console.log("Quiz Type:", quizType);
      populateQuiz(quiz_questions, quizType);
      startTimer();
    } else {
      console.error('No quiz data found in localStorage');
    } 
  }

  // Retry Quiz
  let retryButton = document.getElementById('retry-quiz-btn');
  if (retryButton) {
    retryButton.addEventListener('click', function(event) {
      event.preventDefault();
      retryQuiz();
    })
  }

  const retryQuizFlag = localStorage.getItem('retryQuiz');

  if (retryQuizFlag === 'true') {
    // Clear the retry flag
    localStorage.removeItem('retryQuiz');

    // Fetch the quiz questions and type from localStorage
    const questions = JSON.parse(localStorage.getItem('quizQuestions'));
    const quizType = localStorage.getItem('quizType');

    // Ensure questions data is valid
    if (questions && Array.isArray(questions)) {
      // Clear any existing answers or state
      const quizForm = document.getElementById('quiz-form');
      if (quizForm) {
        // Clear the quiz form and steps
        const quizSteps = document.getElementById('quiz-steps');
        if (quizSteps) {
          quizSteps.innerHTML = '';
        }
        quizForm.innerHTML = '';

        // Repopulate the quiz with the same questions
        populateQuiz(questions, quizType);
      }
    }
  }
 
});

let numberOfQuestions;
let quiz_questions;
let quizType;
let timer;
let startTime;
let timerInterval;

// Function to start or continue timer
function startTimer() {
  // Clear any existing timer data if starting a new quiz
  localStorage.removeItem('quizStartTime');
  
  // Set the start time
  startTime = new Date().getTime();
  localStorage.setItem('quizStartTime', startTime);

  // Clear any existing interval
  if (timerInterval) {
    clearInterval(timerInterval);
  }

  // Set timer to update every second
  timerInterval = setInterval(updateTimerDisplay, 1000);
}

// Update timer display
function updateTimerDisplay() {
  const now = new Date().getTime();
  const startTime = parseInt(localStorage.getItem('quizStartTime'));
  const elapsed = now - startTime;
  
  const hours = Math.floor((elapsed % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((elapsed % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((elapsed % (1000 * 60)) / 1000);
  
  document.getElementById('timer').innerText = 
    `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// Function to stop the timer
function stopTimer() {
  clearInterval(timerInterval);
}

// Add event listener to reset timer when leaving the page
window.addEventListener('beforeunload', function() {
  stopTimer(); // Stop the timer
});

// Function to finish quiz and display elapsed time
function submitAnswers() {
  stopTimer(); // Stop the timer
  
  const endTime = new Date().getTime();
  const startTime = parseInt(localStorage.getItem('quizStartTime'));
  const totalTime = endTime - startTime;

  const hours = Math.floor((totalTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((totalTime % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((totalTime % (1000 * 60)) / 1000);

  const timeString = `${String(hours).padStart(2, '0')} hours ${String(minutes).padStart(2, '0')} minutes ${String(seconds).padStart(2, '0')} seconds`;
   // Save the time string in localStorage
   localStorage.setItem('quizCompletionTime', timeString);
   
  console.log(`Quiz completed in ${timeString}`);

  // Clear the stored start time
  localStorage.removeItem('quizStartTime');
  localStorage.setItem('quizCompleted', 'true'); // Mark quiz as completed
}


// Quiz generation: Handle random Quiz
function randomQuiz() {
  const selectQuestionCount = document.getElementById('question-count');
  const numberOfQuestions = selectQuestionCount.value;

  axios.post('/api/quiz', {
    question_count: numberOfQuestions
  })
  .then(function(response) {
    if (response.data.redirect_url) {
      data = response.data;
      quiz_questions = data.quiz_questions;
      quizType = "Random";

      localStorage.setItem('numberOfQuestions', numberOfQuestions);
      localStorage.setItem('quizType', quizType);
      localStorage.setItem('quiz_questions', JSON.stringify(quiz_questions));
     
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

// Quiz generation: Handle custom Quiz
function customQuiz() {
  const selectCategory = document.getElementById('category');
  const selectDifficulty = document.getElementById('difficulty');
  const selectQuestionCount = document.getElementById('question-count');
  const selectType = document.getElementById('answer-type');

  const quizCategory = selectCategory.value;
  const quizDifficulty = selectDifficulty.value;
  const numberOfQuestions = selectQuestionCount.value;
  const answerType = selectType.value;

  axios.post('/api/quiz', {
    quiz_category: quizCategory,
    quiz_difficulty: quizDifficulty,
    question_count: numberOfQuestions,
    answer_type: answerType
  })
  .then(function(response) {
    if (response.data.redirect_url) {
      data = response.data;
      quiz_questions = data.quiz_questions;
      quizType = "Custom";

      localStorage.setItem('numberOfQuestions', numberOfQuestions);
      localStorage.setItem('quizType', quizType);
      localStorage.setItem('quiz_questions', JSON.stringify(quiz_questions));
     
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
  const answerType = selectType.value;

  axios.post('/api/quiz', {
    quiz_category: quizCategory,
    quiz_difficulty: quizDifficulty,
    question_count: numberOfQuestions,
    quiz_type: answerType
  })
  .then(function(response) {
    if (response.data.redirect_url) {
      data = response.data;
      quiz_questions = data.quiz_questions;
      quizType = "Pre-Saved";

      localStorage.setItem('numberOfQuestions', numberOfQuestions);
      localStorage.setItem('quizType', quizType);
      localStorage.setItem('quiz_questions', JSON.stringify(quiz_questions));
     
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



function populateQuiz(questions, quizType) {
  const quizSteps = document.getElementById('quiz-steps');
  const quizForm = document.getElementById('quiz-form');
  const progressInfo = document.getElementById('quiz-progress-info');
  const progressBar = document.getElementById('progress-bar');

  //localStorage.setItem('quizCompleted', 'false');
  // startTimer();
  // Update quiz type in header
  document.getElementById('quiz-type').innerText = quizType;

  // Initialize progress bar
  function updateProgress(index) {
    const percentage = ((index + 1) / questions.length) * 100;
    progressBar.style.width = `${percentage}%`;
    progressBar.setAttribute('aria-valuenow', percentage);
    progressInfo.innerText = `Question ${index + 1} out of ${questions.length}`;
  }

  questions.forEach((question, index) => {
    // Step indicator
    const stepDiv = document.createElement('div');
    stepDiv.className = `step ${index === 0 ? 'active' : ''}`;
    stepDiv.setAttribute('data-target', `#question-${index + 1}`);
    quizSteps.appendChild(stepDiv);

    // Question card
    const questionDiv = document.createElement('div');
    questionDiv.id = `question-${index + 1}`;
    questionDiv.className = `bs-stepper-pane ${index === 0 ? 'active' : ''} stepper-block`;
    

    const cardDiv = document.createElement('div');
    cardDiv.className = 'card mb-4';

    const cardBodyDiv = document.createElement('div');
    cardBodyDiv.className = 'card-body question-container';

    // Question content
    const questionTextDiv = document.createElement('div');
    questionTextDiv.className = 'mt-5';
    questionTextDiv.innerHTML = `
      <span>Question ${index + 1}</span>
      <h3 class="mb-3 mt-1">${question.question}</h3>
    `;

    // Answer options
    const answersDiv = document.createElement('div');
    answersDiv.className = 'list-group';
    answersDiv.id = `${question.id}`;
    answersDiv.dataset.questionId = question.id;
    question.answers.forEach((answer, answerIndex) => {
      const answerDiv = document.createElement('div');
      answerDiv.className = 'list-group-item list-group-item-action';
      answerDiv.innerHTML = `
        <div class="form-check">
          <input class="form-check-input" type="radio" name="question-${index + 1}" id="answerRadioOption${index + 1}-${answerIndex}" value="${answer}">
          <label class="form-check-label stretched-link" for="answerRadioOption${index + 1}-${answerIndex}">
            ${answer}
          </label>
        </div>
      `;
      answersDiv.appendChild(answerDiv);
    });

    // Append content to card body
    cardBodyDiv.appendChild(questionTextDiv);
    cardBodyDiv.appendChild(answersDiv);

    // Append card to question div
    cardDiv.appendChild(cardBodyDiv);

    // Append card to question div
    questionDiv.appendChild(cardDiv);

    // Navigation buttons
    const navDiv = document.createElement('div');
    navDiv.className = 'mt-3 d-flex justify-content-between';
    if (index > 0) {
      navDiv.innerHTML += `
        <button class="btn btn-secondary" type="button" onclick="showPreviousQuestion(${index + 1})">
          <i class="fe fe-arrow-left"></i>
          Previous
        </button>
      `;
    } else {
      navDiv.innerHTML += `
        <div></div>
      `;
    }
    
    if (index < questions.length - 1) {
      navDiv.innerHTML += `
        <button class="btn btn-primary" type="button" onclick="showNextQuestion(${index + 1})">
          Next
          <i class="fe fe-arrow-right"></i>
        </button>
      `;
    } else {
      navDiv.innerHTML += `
        <button type="submit" class="btn btn-primary" onclick="submitAnswers()">
          Submit
        </button>
      `;
    }
    questionDiv.appendChild(navDiv);

    // Append question div to form
    quizForm.appendChild(questionDiv);

    // Initialize progress for the first question
    if (index === 0) {
      updateProgress(index);
    }
  });
}

function showNextQuestion(currentIndex) {
  document.getElementById(`question-${  currentIndex}`).classList.remove('active');
  document.getElementById(`question-${currentIndex + 1}`).classList.add('active');
  document.querySelector(`.step[data-target="#question-${currentIndex}"]`).classList.remove('active');
  document.querySelector(`.step[data-target="#question-${currentIndex + 1}"]`).classList.add('active');
  
  // Update progress
  updateProgress(currentIndex);
}

function showPreviousQuestion(currentIndex) {
  document.getElementById(`question-${currentIndex}`).classList.remove('active');
  document.getElementById(`question-${currentIndex - 1}`).classList.add('active');
  document.querySelector(`.step[data-target="#question-${currentIndex}"]`).classList.remove('active');
  document.querySelector(`.step[data-target="#question-${currentIndex - 1}"]`).classList.add('active');
  
  // Update progress
  updateProgress(currentIndex - 2); // Current index minus one for zero-based indexing
}

function updateProgress(index) {
  const percentage = ((index + 1) / document.querySelectorAll('.step').length) * 100;
  document.getElementById('progress-bar').style.width = `${percentage}%`;
  document.getElementById('progress-bar').setAttribute('aria-valuenow', percentage);
  document.getElementById('quiz-progress-info').innerText = `Question ${index + 1} out of ${document.querySelectorAll('.step').length}`;
}

 
function submitQuiz() {
  
  // Submit quiz logic here
  const answers = {};
 
  // Collect all selected answers
  document.querySelectorAll('input[type="radio"]:checked').forEach((input) => {
    // Extract question ID from the name attribute
    const answersDiv = input.closest('.list-group');
    const questionId = answersDiv.dataset.questionId;
    answers[questionId] = input.value;
  });
  // Send answer to backend for processing
  axios.post('/quiz', { answers: answers })
    .then(response => {
      // Handle successful response
      console.log('Quiz submitted successfully:', response.data);
      // Redirect or display a success message
      data = response.data
      score = data.percentage_score
      localStorage.setItem("score", score)
      window.location.href = '/results';
    })
    .catch(error => {
      // Handle error response
      console.error('Error submitting quiz:', error);
      // Display an error message
    });
}
function quizResults() {
  const quizTime = localStorage.getItem('quizCompletionTime');
  const quizScore = localStorage.getItem('score');

   // Ensure these values are not null before inserting them into the HTML
  if (quizTime && quizScore) {
    // Render the quiz completion time
    const quizTimeElement = document.getElementById('quiz-time');
    quizTimeElement.innerText = `Quiz completion time: ${quizTime}`;

    // Render the quiz score
    const scoreElement = document.querySelector('.text-dark');
    scoreElement.innerText = `${quizScore}% (${quizScore} points)`;

    const scoreCircle = document.getElementById('score-circle');
    scoreCircle.style.setProperty('--progress', quizScore);

    const scoreText = document.getElementById('score-text');
    scoreText.textContent = `${quizScore}%`;
  }
}

function finishQuiz() {
  const score = localStorage.getItem('score');


  localStorage.removeItem('quiz_questions');
  localStorage.removeItem('numberOfQuestions');
  localStorage.removeItem('quizType');
  localStorage.removeItem('score');
  localStorage.removeItem('quizCompletionTime');

  axios.post('/save-quiz', {score: score})
  .then(function(response){
    if (response.data.redirect_url) {
      window.location.href = response.data.redirect_url;
    } else {
      // Handle case where redirect URL is not provided
      console.error('Redirect URL not provided');
    }
  })
  .catch(function(error) {
    // Handle error in the request
    console.error('Error finishing quiz:', error);
  });
}

function retryQuiz() {
   // Set a flag in localStorage to indicate the quiz should be retried
  localStorage.setItem('retryQuiz', 'true');

   // Redirect to the quiz page
   window.location.href = '/quiz';
}