// ========================================
// AI Resume Screening System
// script.js
// ========================================

// Auto-hide alerts
setTimeout(() => {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {

        alert.classList.remove("show");

    });

}, 3000);


// Confirm before deleting
document.querySelectorAll(".btn-danger").forEach(button => {

    button.addEventListener("click", function(e){

        if(!confirm("Are you sure you want to delete this candidate?")){

            e.preventDefault();

        }

    });

});


// Highlight selected skills
document.querySelectorAll("input[type='checkbox']").forEach(box=>{

    box.addEventListener("change",function(){

        if(this.checked){

            this.parentElement.classList.add("text-primary","fw-bold");

        }

        else{

            this.parentElement.classList.remove("text-primary","fw-bold");

        }

    });

});


// Validate upload form
const form=document.querySelector("form");

if(form){

form.addEventListener("submit",function(e){

const file=document.querySelector("input[name='resume']");

if(file){

const filename=file.value.toLowerCase();

if(!filename.endsWith(".pdf")){

alert("Please upload only PDF resumes.");

e.preventDefault();

return;

}

}

const checked=document.querySelectorAll("input[name='skills']:checked");

if(checked.length===0){

alert("Select at least one required skill.");

e.preventDefault();

}

});

}


// Animate progress bars
window.addEventListener("load",()=>{

document.querySelectorAll(".progress-bar").forEach(bar=>{

const value=bar.style.width;

bar.style.width="0%";

setTimeout(()=>{

bar.style.transition="1s";

bar.style.width=value;

},200);

});

});


// Candidate search
const search=document.getElementById("searchCandidate");

if(search){

search.addEventListener("keyup",function(){

const value=this.value.toLowerCase();

const cards=document.querySelectorAll(".candidate-card");

cards.forEach(card=>{

card.style.display=

card.innerText.toLowerCase().includes(value)

? "block"

: "none";

});

});

}