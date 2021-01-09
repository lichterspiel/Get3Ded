$(document).ready( ()=> {
	var room = document.getElementById("room_id").textContent;
	var socket = io.connect('http://' + document.domain + ':' + location.port + "/play"); 
	 //var username = {{ username| tojson}};//"{{ username }}";


	console.log(username)
	socket.on("connect",() => {
		socket.emit("join",{
			username: username,
			room: room
		});
		socket.emit("load_board")
	});
	window.getPress = function getPress(id)
	{
		// change this so when button is pressed send it to server -> validate -> change dom so it is not a button 
		socket.emit("move", {id : id, icon: icon})
	}
	
	socket.on("valid", (data) =>{
		console.log(data.id)
		document.getElementById(data.id).innerHTML = data.icon;
		console.log("valid")
	})
	socket.on("invalid", () => {
		console.log("invalid")

	})
	
	socket.on("disconnect", (reason) => {
		console.log("yeaaah")
		socket.emit("room_left", {
			room: room
		})
	})

		
})

	
