


function generateEventForm() {
  if ($("#eventForm").css("display") == "none") {
    $("#eventForm").show();
    $("#addEventBtn").text("Cancel")
  } else {
    $("#eventForm").hide();
    $("#addEventBtn").text("Add event")
  }
}

function showError(error) {
  $("#formAlert").show();
  $("#formAlert").text(error);
  var inter = setInterval(function() {
        $("#formAlert").hide();

      }, 6000);

  clearInterval(inter);

}

function addEvent() {

  $title = $("#eventTitle").val();
  $date = $("#eventDate").val();
  $time = $("#eventTime").val();
  console.log($title, $date, $time);

  $.ajax({
    url: "/ajax/addEvent",
    data: ({ title : $title, date: $date, time: $time }),
    type: "GET",
    success: function(data) {
      if (data.length > 0) {
        $("#userEvents").prepend(data);
        $("#eventTitle").val("");
        $("#eventDate").val("");
        $("#eventTime").val("");
      } else {
        showError(data.error);
      }


    },
    error: function(error) {
      console.log(error);
    },

  });
}


function setPeriod(periodId) {
  var period;

  if (periodId == 1) {
    period = "daily";
  } else if (periodId == 2) {
    period = "weekly";
  } else if (periodId == 3) {
    period = "monthly";
  } else {
    period = "all";
  }

  $.ajax({
    url: "/ajax/sortByPeriod",
    data: ({ period:period }),
    type: "GET",
    success: function(data) {
      if (data.length > 0) {
        $("#userEvents").html(data);
      } else {
      }

    },
    error: function(error) {
      console.log(error);
    },

  });

}



function eventCompleted(eventID, completedDate) {
  $("#"+eventID).text(completedDate);
  $("#"+eventID+"title").append("<span class='badge badge-danger'>COMPLETED</span>");
  $("#"+eventID+"btn").hide();

}

var counters = new Map();

function timeCounter(eventID, timeData) {

  var datetime = new Date(timeData).getTime();
  var inter = setInterval(function() {
    var now  = new Date().getTime();
    var rest_time = datetime - now;
    var days = Math.floor(rest_time / (1000 * 60 * 60 * 24));
    var hours = Math.floor((rest_time%(1000 * 60 * 60 * 24))/(1000 * 60 * 60));
    var minutes = Math.floor((rest_time % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((rest_time % (1000 * 60)) / 1000);
    $("#"+eventID).text("Left " + days + " days, " + hours +" hours and " + minutes + " min");
    if (days==0 && hours == 1) {
    } else if ((days==0 && hours == 0 && minutes == 0 && seconds == 0)) {
      eventCompleted(eventID, timeData);
      old_inter = counters.get(eventID);
      clearInterval(old_inter);
    }

  }, 1000);

  if (counters.has(eventID)) {
    old_inter = counters.get(eventID);
    clearInterval(old_inter);
    counters.set(eventID, inter);
  } else {
    counters.set(eventID, inter);
  }
}


    function startEdit(elementUrl) {
      if ($("#"+elementUrl+"updform").css("display") == "none") {
        $("#"+elementUrl+"updform").show();
        $("#"+elementUrl+"cont").hide();
      } else {
        $("#"+elementUrl+"updform").hide();
        $("#"+elementUrl+"cont").show();
      }
    }

    function showOptions(elementUrl) {
      if ($("#"+elementUrl+"div").css("display") == "none") {
        $("#"+elementUrl+"div").show();
        $("#"+elementUrl+"btn").text("Cancel")
      } else {
        $("#"+elementUrl+"div").hide();
        $("#"+elementUrl+"btn").text("Config")
      }
    }

    function deleteEvent(elementUrl) {

      $.ajax({
        url: "/ajax/deleteEvent",
        data: ({ event_url: elementUrl }),
        type: "GET",
        success: function(data) {
          if (data.resp == true) {
            $("#" + elementUrl + "cont").remove();
          }

        },
        error: function(error) {
          console.log(error);
        },

      });
    }

    function findEvent() {

      $eventQuery = $("#findInput").val();

      $.ajax({
        url: "/ajax/findEvent",
        data: ({ event_query:  $eventQuery}),
        type: "GET",
        success: function(data) {
          if (data.length > 0) {
            $("#userEvents").html(data);
          }

        },
        error: function(error) {
          console.log(error);
        },

      });
    }

    function saveUpdated(elementUrl) {
      $newTitle = $("#" + elementUrl + "newEventTitle").val();
      $newDate = $("#" + elementUrl + "newEventDate").val();
      $newTime =  $("#" + elementUrl + "newEventTime").val();
      console.log($newDate, $newTime, $newTitle, elementUrl);
      $.ajax({
        url: "/ajax/updateEvent",
        data: ({ title : $newTitle, date: $newDate, time: $newTime, event_url: elementUrl }),
        type: "GET",
        success: function(data) {
          if (data.resp == true) {
            $("#" + elementUrl + "title").text($newTitle);
            var date = $newDate + "T" + $newTime;
            timeCounter(elementUrl, date);
            console.log(date);
            startEdit(elementUrl);
          } else {
            $("#" + elementUrl + "formAlert").show();
            $("#" + elementUrl + "formAlert").text(data.error);
            var inter = setInterval(function() {
                  $("#" + elementUrl + "formAlert").hide();
                }, 6000);
            clearInterval(inter);
          }

        },
        error: function(error) {
          console.log(error);
        },

      });
    }
