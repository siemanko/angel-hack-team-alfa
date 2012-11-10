var appUpdateProc; //update function

$(document).ready(function() {
	heartbeat();
});

var apptime = 1;
var nextUpdate = 1000;
function heartbeat() {
	apptime += 10;
	var addr = "/studentq/getstate";
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
				nextUpdate = apptime + 30000;
			}
		});
	}
	setTimeout(heartbeat, 10);
}

function addQuestion(text) {
	$.ajax({
		type: 'POST',
		url: "/studentq/updatestate",
		data: {
			action : "addquestion",
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
}

function voteQuestion(qid,qpoint) {
	$.ajax({
		type: 'POST',
		url: "/studentq/updatestate",
		data: {
			action : "vote",
			id : qid,
			points : qpoint
		},
		success: function(data) {
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
console.log(questions.length);
	
	questions.sort(function(q1,q2) { return q2.votescore - q1.votescore; });
	
	var elements = [];
	questions.forEach(function(question) {
		var id = question.id;
		var qNode = $(".q-"+id);
		
		var temp = $(".question-template");
		var qdiv = temp.clone();
		qdiv.find(".text").html(question.text);
		qdiv.find(".votes").html(question.votescore);
		qdiv.find(".upvote").click(function() {
			voteQuestion(id,1);
		});
		qdiv.find(".downvote").click(function() {
			voteQuestion(id,-1);
		});
		
		qdiv.attr("class", "question");
		qdiv.addClass("q-"+id);
		
		//var math = document.getElementById("MathExample");
		if (qNode.size() > 0) {
			qdiv.show();
		} else {
			qdiv.fadeIn(1000);
		}
		elements.push(qdiv);
	});
	
	$("#right_container").html("");
	elements.forEach(function(el) {
		$("#right_container").append(el);
		MathJax.Hub.Queue(["Typeset",MathJax.Hub,el.get()]);
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
