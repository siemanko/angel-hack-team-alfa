var appUpdateProc; //update function

$(document).ready(function() {
	heartbeat();
});

var apptime = 1;
var nextUpdate = 1000;
function heartbeat() {
	apptime += 10;
	if (apptime > nextUpdate && nextUpdate > 0) {
		nextUpdate = -1;
		$.ajax({
			url : "studentq/getstate",
			dataType : "html",
			success: function(data) {
				appUpdateProc(data);
				nextUpdate = apptime + 2000;
			},
			error : function(jqXHR, textStatus, errorThrown) {
				appUpdateProc(undefined, errorThrown);
				nextUpdate = apptime + 5000;
			}
		});
	}
	setTimeout(heartbeat, 10);
}

function updateApplicationState() {
}

function updateApplicationStateMock(data, error) {
	$("#callNo").html("Call: "+apptime);
	if (error) {
		$("#appstate").html("ERROR! "+error);
	} else {
		$("#appstate").html(data);
	}
}

function addQuestion(text) {
}

function voteQuestion() {
}

function updateNow() {
	nextUpdate = apptime+1;
}