function event_callback(event) {
	if (event.payload.control==1){
		temp=event.payload.temp;
    		erature=event.payload.erature;
		document.getElementById('temp').innerHTML = temp+"<span id='erature'>."+erature+"</span><strong>&deg;</strong>";
	}
	if (event.payload.control==0){
		state=event.payload.state;
		water=event.payload.water_state;
		light=event.payload.light_state;
		heating=event.payload.heat_state;
		
		document.getElementById("heat").checked = heating;
		document.getElementById("water").checked = water;
		document.getElementById("light").checked = light;
		set_state(state);
	}else if (event.payload.control==2) {
		heating=event.payload.heat_state;
		document.getElementById("heat").checked = heating;
	}else if (event.payload.control==3) {
		water=event.payload.water_state;
		light=event.payload.light_state;
		
		document.getElementById("water").checked = water;
		document.getElementById("light").checked = light;
	}

}

function heat_callback() {
    Z.call('heating_switch', [document.getElementById("heat").checked]);
}

function water_callback() {
    Z.call('water_switch', [document.getElementById("water").checked]);
}

function light_callback() {
    Z.call('light_switch', [document.getElementById("light").checked]);
}

function connected_callback() {
	Z.call('get_initial_state', [24], result_callback);
}

function result_callback(msg){
	state=msg.res.state;
	heat=msg.res.heat_state;
	water=msg.res.water_state;
	light=msg.res.light_state;
	desired=msg.res.desired_temp;

	$('#rangevalue').text(desired);
	set_state(state);
	document.getElementById("heat").checked = heat;
	document.getElementById("water").checked = water;
	document.getElementById("light").checked = light;
}

function slide_callback() {
    Z.call('set_desired_temp', [$('#rangevalue').val()]);
}

function set_state(value){
	if (value)
		document.getElementById('led').style.backgroundColor  = '#52ff1e';
	else 
		document.getElementById('led').style.backgroundColor  = '#ff0000';

}

function delay() {
	set_state(true);
	Z.call('set_state',[true]);
	var today = new Date();
	ore=document.getElementById("ore").value;
	min=document.getElementById("min").value;
	ore=(ore-today.getHours())*60*60*1000;
	min=(min-today.getMinutes())*60*1000;
	ms=min+ore;
	Z.call('set_delay',[ms]);
}


//inizializzazione

function initialize() {
	Z.init({
        on_event: event_callback, //quando la scheda invia qualcosa
        on_connected: connected_callback    //alla connessione tra scheda/app
 
    });
	//$('#rangevalue').change(slide_callback);
	$('#heat').click(heat_callback);
	$('#water').click(water_callback);
	$('#light').click(light_callback);
	$('#button').click(delay);
	$('.container').focus(function(){$(this).blur();});	
}