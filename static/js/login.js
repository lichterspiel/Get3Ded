const username = document.getElementById("username");
const password = document.getElementById("password");
const form = document.getElementById("form");
const errorElement = document.getElementById("error");

var forms = document.querySelectorAll(".needs-validation");
$(document).ready( () => {
	Array.prototype.slice.call( form ).forEach( (form) =>{
		form.addEventListener("submit", (e) =>
		{
			console.log("sss")
			if (!form.checkValidity())
			{
				e.preventDefault();
				e.stopPropagation();
			}

			form.classList.add("was validated");

		})
	})
})

