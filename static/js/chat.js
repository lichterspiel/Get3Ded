var socket = io.connect("http://" + document.domain + ":" + location.port + "/room");

socket.on("connect", function(){
	var form = $("form").on("submit", function(e){
		e.preventDefault()
		let user_name = "Karl"//$("input.room_name_join").val()
		let room = $("input.room_name").val()
		
		socket.emit("join", {
			username : user_name,
			room: room
		})
		console.log(user_name, room)
	})
})


