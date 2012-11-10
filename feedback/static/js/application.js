var appUpdateProc; //update function

$(document).ready(function() {
	heartbeat();
});

var apptime = 1;
var nextUpdate = 1000;
function heartbeat() {
	apptime += 10;
	var addr = "static/appstate.json";
	if (apptime > nextUpdate && nextUpdate > 0) {
		nextUpdate = -1;
		$.ajax({
			url : addr,
			dataType : "json",
			success: function(data) {
				appUpdateProc(data);
				nextUpdate = apptime + 20000;
			},
			error : function(jqXHR, textStatus, errorThrown) {
				appUpdateProc(undefined, errorThrown);
				nextUpdate = apptime + 50000;
			}
		});
	}
	setTimeout(heartbeat, 10);
}

function addQuestion(text) {
/*
	$.ajax({
		type: 'POST',
		url: "studentq/addQuestion,
		data: {
			text : textcontent
		},
		success: function(data) {
			alert("ok - question added");
			updateNow();
		},
  		error: function(jqXHR, textStatus, errorThrown) {
  			alert("Cannot save");
  		}
	});
*/
}

function voteQuestion(qid,qpoint) {
	$.ajax({
		type: 'POST',
		url: "studentq/updatestate",
		data: {
			action : "vote",
			id : qid,
			points : qpoint
		},
		success: function(data) {
			alert("ok - voted");
			updateNow();
		},
  		error: function(jqXHR, textStatus, errorThrown) {
  			alert("Cannot save");
  		}
	});
}

function updateNow() {
	nextUpdate = apptime+1;
}

function updateApplicationState(data,error) {
	var state = data.state;
	var questions = state.questions;
	
	questions.sort(function(q1,q2) { return q2.votescore - q1.votescore; });
	
	$("#right_container").html("");
	questions.forEach(function(question) {
		var temp = $(".question-template");
		var qdiv = temp.clone();
		var id = question.id;
		qdiv.find(".text").html(question.text);
		qdiv.find(".votes").html(question.votescore);
		qdiv.find("#upvote").click(function() {
			voteQuestion(id,1);
		});
		qdiv.find("#downvote").click(function() {
			voteQuestion(id,-1);
		});
		
		qdiv.attr("class", "question");
		$("#right_container").append(qdiv);
		qdiv.show();
	});
}


// Mocks

function updateApplicationStateMock(data, error) {
	$("#callNo").html("Call: "+apptime);
	if (error) {
		$("#appstate").html("ERROR! "+error);
	} else {
		$("#appstate").html(data);
	}
}

function updateApplicationStateMock2(data,error) {
	var state = data.state;
	var questions = state.questions;
	
	questions.sort(function(q1,q2) { return q2.votescore - q1.votescore; });
	
	$("#window").html("");
	var ul = $("<ul />");
	questions.forEach(function(question) {
		ul.append("<li>"+question.text+"</li>");
	});
	$("#window").append(ul);
}