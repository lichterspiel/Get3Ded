$(document).ready( ()=> {
	var room = document.getElementById("room_id").textContent;
	var socket = io.connect('http://' + document.domain + ':' + location.port + "/play"); 
	console.log(username)
	// join room
	socket.emit("join",{
		username: username,
		room: room
	});

	// tell the server to start giving the board data
	socket.on("start_loading", () =>{
		socket.emit("load_board")
	})
	// when board data is received change the dom

	socket.on("load", data => {
		for ( let i = 0; i < data.length; i++ )
		{
			for (let j = 0; j < data.length; j++)
			{
				// if it is not 0 change the icon in the dom to represent it
				if (data[i][j] != 0)
				{
					console.log(String(data[i][j]))
					var id = String(i) + String(j)
					document.getElementById(id).innerHTML = String(data[i][j]);
				}
			}	
		}
	})


	window.getPress = function getPress(id)
	{
		socket.emit("move", {id : id, icon: icon});
	}
	
	socket.on("valid", (data) =>{
		console.log(data.id)
		document.getElementById(data.id).innerHTML = data.icon;
		console.log("valid")
	})
	socket.on("invalid", () => {
		console.log("invalid")

	})
	socket.on("Winner", data =>{
		console.log(data.winner)
		if (icon == data.winner)
		{
			document.getElementById("overlay").style.display = "block";
		}
		else
		{
			document.getElementById("place").innerHTML= "Lost";
			document.getElementById("overlay").style.display = "block";
		}
		socket.emit("game_finished", {room: room, winner:data.winner})

	// add emit to delete room in db and update player win /loose count	


	})
	
	socket.on("disconnect", (reason) => {
		console.log("yeaaah")
		socket.emit("room_left", {
			room: room
		})
	})

		
})

	
