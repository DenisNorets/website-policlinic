    const form = document.getElementById('form');
    const name = document.getElementById('name');
    const lastname = document.getElementById('last_name');
    const email = document.getElementById('email');
    const date = document.getElementById('date');
    const doctors = document.getElementById('doctors');
    var checkvalid = false;

$('.redirectbutton').click(function() {
form.addEventListener('submit', (e) => {
    e.preventDefault();
});
    window.location = '../main'
});

$('.clearbutton').click(function() {


form.addEventListener('submit', (e) => {
    e.preventDefault();
});

name.value = '';
lastname.value = '';
email.value = '';
date.value = '';
doctors.selectedIndex = 0;
setNeutralFor(name);
setNeutralFor(lastname);
setNeutralFor(date);
setNeutralFor(email);
setNeutralFor(doctors);
});

$('.submitbutton').click(function() {
    

form.addEventListener('submit', (e) => {
    e.preventDefault();

});

const namevalue = name.value.trim();
const lastnamevalue = lastname.value.trim();
const emailvalue = email.value.trim();
const datevalue = date.value.trim();
const doctorsvalue = doctors[doctors.selectedIndex].value;

if (doctorsvalue === 'none') {
    setErrorFor(doctors, 'Выберите врача');
} else {
    setSuccessFor(doctors);
}

if (namevalue === '') {
    setErrorFor(name, 'Имя не может быть пустым');
} else {
    setSuccessFor(name);
}

if (lastnamevalue === '') {
    setErrorFor(lastname, 'Фамилия не может быть пустой'); 
} else {
    setSuccessFor(lastname);
}

if (datevalue === '') {
    setErrorFor(date, 'Дата не может быть пустой'); 
} else {
    setSuccessFor(date);
}

if (emailvalue === '') {
    setErrorFor(email, 'Email не может быть пустым');
} else if(!isEmail(emailvalue)) {
    setErrorFor(email, 'Впишите валидный email, example@example.ex');
}
else {
    setSuccessFor(email);
}
if ((doctorsvalue !== 'none')&&(namevalue !== '')&&(lastnamevalue !== '')&&(datevalue !== '')&&(emailvalue !== '')&&(isEmail(emailvalue))) {
    checkvalid = true;
    email.disabled = 1;
    name.disabled = 1;
    lastname.disabled = 1;
    date.disabled = 1;
    doctors.disabled = 1;
    document.getElementById('submitbutton').disabled = 1;
    $('.submitbutton').css('pointer-events', 'none').css('background-color', '#33ffba');
} else {
    checkvalid = false;
}
if (checkvalid) {
    $('.js-overlay').fadeIn();
    $('main').css('filter','blur(5px)');
    
}



});

function setErrorFor(input, message) {
    const formControl = input.parentElement; // .form-control
    const small = formControl.querySelector('small');

    // add error message
    small.innerText = message;
    // add error class
    formControl.className = 'form-control error';
}

function setSuccessFor(input) {
    const formControl = input.parentElement;
    formControl.className = 'form-control success';
}

function setNeutralFor(input) {
    const formControl = input.parentElement;
    formControl.className = 'form-control';
}


function isEmail(email) {
    return /^([a-z\d\.-]+)@([a-z\d-]+)\.([a-z]{2,8})(\.[a-z]{2,8})?$/.test(email);
}


$('.js-close').click(function() {
    $('.js-overlay').fadeOut();
    $('main').css('filter', 'none');
});



