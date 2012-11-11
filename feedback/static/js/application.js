var appUpdateProc; //update function
var heartbeatAddr;
var paramdic = {};
$(document).ready(function() {
	heartbeat();
	attentionButton(false);
  $("#ask-dropdown").click(function() {
    console.log("here");
    $("#ask-dropdown-content").html("");
    var loadingli = document.createElement('li');
    loadingli.appendChild(document.createTextNode("Loading..."));
    $("#ask-dropdown-content").append(loadingli);
    $.ajax({
	    type: 'POST',
	    url: "/teacherq/getquestions",
	    data: {},
	    success: function(data) {
        $("#ask-dropdown-content").html("");
        data.forEach(function(q) {
          var loadingli = $('<li />');
          var alink = $("<a />");
          alink.attr("href", '/teacherq/activatequestion/'+q.id);
          alink.html(q.text);
          loadingli.append(alink);
          $("#ask-dropdown-content").append(loadingli);
        }); 
	    },
		    error: function(jqXHR, textStatus, errorThrown) {

			    alert(errorThrown);
		    }
    });
  });
});


var apptime = 1;
var nextUpdate = 1000;
function heartbeat() {
	apptime += 10;
	var addr = heartbeatAddr;
	if (apptime > nextUpdate && nextUpdate > 0) {
		nextUpdate = -1;
		$.ajax({
			url : addr,
			dataType : "json",
      data : paramdic,
			success: function(data) {
				appUpdateProc(data);
				nextUpdate = apptime + 1000;
			},
			error : function(jqXHR, textStatus, errorThrown) {
				appUpdateProc(undefined, errorThrown);
				nextUpdate = apptime + 5000;
			}
		});
	}
	setTimeout(heartbeat, 1);
}

function attentionButton(change) {
$.ajax({
	type: 'GET',
	url: "/studentq/updateattention",
	data: {
		"change" : change,
	},
	success: function(data) {
		if (data.isConfused) {
			$("#npa").css("color", "red");
		} else {
			$("#npa").css("color", "grey");
		}
		updateNow();
	},
		error: function(jqXHR, textStatus, errorThrown) {
			alert(errorThrown);
		}
});
}

function addQuestion(textcontent, callback) {
	$.ajax({
		type: 'POST',
		url: "/studentq/updatestate",
		data: {
			action : "add",
			text : textcontent
		},
		success: function(data) {
			updateNow();
			callback();
		},
  		error: function(jqXHR, textStatus, errorThrown) {
  			alert("Cannot save");
  			callback();
  		}
	});
}

function addTeacherQuestion(textcontent,opt_a,opt_b,opt_c,opt_d,callback) {
	$.ajax({
		type: 'GET',
		url: "/teacherq/askquestion/submitquestion",
		data: {
			question : textcontent,
			ans_a : opt_a,
			ans_b : opt_b,
			ans_c : opt_c,
			ans_d : opt_d
		},
		success: function(data) {
			updateNow();
			callback();
		},
  		error: function(jqXHR, textStatus, errorThrown) {
  			alert("Cannot save");
  			callback();
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

function markAnswered(qid) {
	$.ajax({
		type: 'POST',
		url: "/studentq/updatestate",
		data: {
			action : "mark",
			id : qid
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

function ignoreUpdate(data,error) {
} 

function teacherAppUpdate(data,error) {


  drawChart(data.state.confusion);


	var state = data.state;
	var questions = state.questions;
	
	questions.sort(function(q1,q2) { 
		var q1s = q1.is_answered ? -1000 : q1.votescore; 
		var q2s = q2.is_answered ? -1000 : q2.votescore;
		return q2s - q1s; 
	});

  while(questions.length > 4) {
    questions.pop();
  }
	
	var elements = [];
	questions.forEach(function(question) {
		var id = question.id;
		var qNode = $(".q-"+id);
		
		var temp = $(".question-template");
		var qdiv = temp.clone();
		qdiv.find(".text").html(question.text);
		qdiv.find(".votes").html(question.votescore);
		qdiv.find(".markanswer").click(function() {
			markAnswered(id);
		});
		
		qdiv.attr("class", "question");
		qdiv.addClass("q-"+id);
		
		if (qNode.size() > 0) {
			qdiv.show();
			if (question.is_answered) {
				qdiv.css({ opacity: 0.5 });
				qdiv.css("background", "#DDFFDD");
				qdiv.find(".controls").hide();
				qdiv.find(".teacher_controls").hide();
			} else if (question.votescore <= 0) {
				qdiv.css({ opacity: 0.5 });
				qdiv.find(".votes").css("color", "red");
				qdiv.css("background", "#FFDDDD");
			} 
		} else {
			if (question.is_answered) {
				qdiv.fadeTo(1000, 0.5);
				qdiv.css("background", "#DDFFDD");
				qdiv.find(".controls").hide();
				qdiv.find(".teacher_controls").hide();
			} else if (question.votescore <= 0) {
				qdiv.fadeTo(1000, 0.5);
				qdiv.find(".votes").css("color", "red");
				qdiv.css("background", "#FFDDDD");
			} else {
				qdiv.fadeIn(1000);
			}
		}
		elements.push(qdiv);
	});
	
	$("#student-questions").html("");
	elements.forEach(function(el) {
		$("#student-questions").append(el);
		MathJax.Hub.Queue(["Typeset",MathJax.Hub,el.get()]);
	});
}

function updateApplicationState(data,error) {
	var state = data.state;
	var questions = state.questions;
console.log(questions.length);
	
	questions.sort(function(q1,q2) { 
		var q1s = q1.is_answered ? -1000 : q1.votescore; 
		var q2s = q2.is_answered ? -1000 : q2.votescore;
		return q2s - q1s; 
	});
	
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
		qdiv.find(".markanswer").click(function() {
			markAnswered(id);
		});
		
		qdiv.attr("class", "question");
		qdiv.addClass("q-"+id);
		
		if (qNode.size() > 0) {
			qdiv.show();
			if (question.is_answered) {
				qdiv.css({ opacity: 0.5 });
				qdiv.css("background", "#DDFFDD");
				qdiv.find(".controls").hide();
				qdiv.find(".teacher_controls").hide();
			} else if (question.votescore <= 0) {
				qdiv.css({ opacity: 0.5 });
				qdiv.find(".votes").css("color", "red");
				qdiv.css("background", "#FFDDDD");
			} 
		} else {
			if (question.is_answered) {
				qdiv.fadeTo(1000, 0.5);
				qdiv.css("background", "#DDFFDD");
				qdiv.find(".controls").hide();
				qdiv.find(".teacher_controls").hide();
			} else if (question.votescore <= 0) {
				qdiv.fadeTo(1000, 0.5);
				qdiv.find(".votes").css("color", "red");
				qdiv.css("background", "#FFDDDD");
			} else {
				qdiv.fadeIn(1000);
			}
		}
		elements.push(qdiv);
	});
	
	$("#right_container").html("");
	elements.forEach(function(el) {
		$("#right_container").append(el);
		MathJax.Hub.Queue(["Typeset",MathJax.Hub,el.get()]);
	});
}

//Easter egg
function initPacman() {
	$("#pacframe").attr("src", "/studentq/pacman");
}

function finalizePacman() {
	$("#pacframe").attr("src", "");
}

// Dialogs

function finalizeAskQuestion() {
	var text = $("#student_question").val();
	$("#student_question").val("");
	addQuestion(text, function() {
		updateNow();
	});
}

function finalizeAskTeacherQuestion() {
	var text = $("#ask_question").val();
	var ansA = $("#ans_a").val();
	var ansB = $("#ans_b").val();
	var ansC = $("#ans_c").val();
	var ansD = $("#ans_d").val();
	
	$("#ans_a").val("");
	$("#ans_b").val("");
	$("#ans_c").val("");
	$("#ans_d").val("");
	$("#ask_question").val();
	addTeacherQuestion(text,ansA,ansB,ansC,ansD,function() {
		updateNow();
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
