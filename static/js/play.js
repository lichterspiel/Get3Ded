function getPress(id)
{
	// change this so when button is pressed send it to server -> validate -> change dom so it is not a button 
	document.getElementById(id).innerHTML = "X";
	console.log("Activated");
}

var socket = io.connect('http://' + document.domain + ':' + location.port + "/play");


socket.on('connect', function() {
	socket.emit( 'my_event', {
		data: 'User Connected'
	})
	socket.emit("join", {
		username: "Karlos",
		room : "123"
	})
	
	// override that form submit is not over http but over websocket
	var form = $( 'form' ).on( 'submit', function( e ) {
		// prevent submitting the form
		e.preventDefault()
		// get the input from the form
		let user_name = $( 'input.username' ).val()
    	let user_input = $( 'input.message' ).val()
	
		socket.emit( "my_event", {
    		user_name : user_name,
    		message : user_input
    	})
		console.log(user_name , user_input)
		// clear message field after submitting
    	$( 'input.message' ).val( '' ).focus()
	})
})

socket.on("my response", function( msg ) {
	console.log( msg )
  	if( typeof msg.user_name !== 'undefined' ) {
    $( 'div.message_holder' ).append('<div><b style="color:#fff"'+msg.user_name+'</b>'+msg.message+'</div>' )
	}
})
