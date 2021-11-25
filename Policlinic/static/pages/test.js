const quiz = document.getElementById('quiz');
const questions = document.getElementById('questions');
const indicator = document.getElementById('indicator');
const results = document.getElementById('results');
const btnnext = document.getElementById('btn-next');
const btnrestart = document.getElementById('btn-restart');
const testResult = document.getElementById('test-result');
const doneCheck = document.getElementById('done-check');

$('.btn-next').css('pointer-events', 'none').css('background-color', '#e9e9e9');

function redirect() {
    window.location = '../main';
}

const DATA = [
    {
        question: 'Какой меры из нижеперечисленных должны придерживаться люди при вспышке пневмонии, вызванной новым коронавирусом?',
        answers: [
            {
                id: '1',
                value: 'Обязательно носить маски',
                correct: true,
            },
            {
                id: '2',
                value: 'Игнорировать социальную дистанцию',
                correct: false,
            },
            {
                id: '3',
                value: 'Пренебрежительное отношение к гигиене',
                correct: false,
            },

        ]
    },
    {
        question: 'Во время чрезвычайного положения всем гражданам слеудет оставаться дома, за исключение какого случая:',
        answers: [
            {
                id: '4',
                value: 'Длительные выходы с целью физической активности',
                correct: false,
            },
            {
                id: '5',
                value: 'Приобретение товаров и услуг',
                correct: true,
            },
            {
                id: '6',
                value: 'Осуществлении профессиональной деятельности без наличия заявления',
                correct: false,
            },

        ]
    },
    {
        question: 'Во время чрезвычайного положения передвижение по дорогам общего использования разрешено только в опрделенном случае, а именно:',
        answers: [
            {
                id: '7',
                value: 'Осуществлении профессиональной деятельности без наличия заявления',
                correct: false,
            },
            {
                id: '8',
                value: 'Оказание помощи родным',
                correct: false,
            },
            {
                id: '9',
                value: 'Поездки несовершеннолетних и сопровождающих их лиц в школу',
                correct: true,
            },

        ]
    },
]

let localResults ={
    
};

const renderQuestions = (index) => {

    questions.dataset.currentStep = index;

    const renderAnswers = () => DATA[index].answers
            .map((answer) => `
                <li>
                    <label >
                        <input  class = "answer-input" type="radio"  name = ${index} value=${answer.id}>
                        ${answer.value}
                    </label>
                </li>
            `
        )
        .join('');

    questions.innerHTML = `
        <div class="quiz-questions-item">
            <div class="quiz-questions-item__question">${DATA[index].question}</div>
            <ul class="quiz-questions-item__answers">${renderAnswers()}</ul>
        </div>
    `;
};

const renderResults = () => {
    let doneAnswers = 0;
    let doneTest = '';

    const checkTrueAnswer = (answer, questionIndex) => {
        if (answer.correct && answer.id === localResults[questionIndex]) {
            doneAnswers = doneAnswers + 1;
        }
    }

    DATA.forEach((question, index) => {
        question.answers.map((answer) => checkTrueAnswer(answer, index))
    });

    testResult.innerHTML = `Ваш результат: ${doneAnswers   }/${DATA.length}`;

    if (doneAnswers === DATA.length) {
        doneCheck.innerHTML = `Тест успешно пройден!`;
        if(window.confirm("Хотите ли вы сохранить результаты теста?")) {localStorage.setItem("done", 1)}
    } else {
        doneCheck.innerHTML = `Тест не пройден`;
        if(window.confirm("Хотите ли вы сохранить результаты теста?")) {localStorage.setItem("done", 0)}
    }
;
};

quiz.addEventListener('change', (e) => {
    if (e.target.classList.contains('answer-input')) {
        localResults[e.target.name] = e.target.value;
        btnnext.disabled = false;
        $('.btn-next').css('pointer-events', 'auto').css('background-color', 'white');
        console.log(localResults)
        
    }
});

quiz.addEventListener('click', (e) => {
    if (e.target.classList.contains('btn-next')) {  
        const nextQuestionIndex = Number(questions.dataset.currentStep) +1;
        if (DATA.length === (nextQuestionIndex) +1) {
            btnnext.innerText = `Завершить тест`;
        } else {
            btnnext.innerText = `Далее`;
        }
        if (DATA.length === nextQuestionIndex) {
            //results
            questions.classList.add('questions--hidden');
            results.classList.add('results--visible');
            btnnext.classList.add('btn-next--hidden');
            btnrestart.classList.add('btn-restart--visible');

            renderResults();
        } else {
            //next
            renderQuestions(nextQuestionIndex);
        }
        
        btnnext.disabled = true;
        $('.btn-next').css('pointer-events', 'none').css('background-color', '#e9e9e9');
    }

    if (e.target.classList.contains('btn-restart')) {
        localResults = {};
        doneCheck.innerHTML = '';
        testResult.innerHTML = '';

        questions.classList.remove('questions--hidden');
        results.classList.remove('results--visible');
        btnnext.classList.remove('btn-next--hidden');
        btnrestart.classList.remove('btn-restart--visible');

        renderQuestions(0);
    }
});

renderQuestions(0);