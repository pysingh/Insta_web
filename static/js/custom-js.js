
function change_active_status(object) {
    $('.tab-pane').removeClass('active');
    object.addClass('active');
}

function Likes() {
   like = document.getElementById('cmn-toggle-4').checked;
    if(like == true){
        document.getElementById('likes_switch').innerHTML = "Functionality Running...";
    }
    else {
        document.getElementById('likes_switch').innerHTML = "Functionality Not Running...";
    }
}
function load_spinner(){
  document.getElementById('loader').style.display = "block";
}

function delete_target_functionality(tagname, link, username, pid){
    load_spinner();
    $.ajax({
      url: link,
      type: "GET",
      data: {
          'username': username,
          'link_id': tagname,
          'pid': pid
      },
      contentType: "application/json;charset=utf-8",
      dataType: "json",
      success: function(data) {
          if(data.json_response == 'Deleted'){
              window.location.href = "/dashboard/"+username+"/";
          }
          else {
              alert("Some error Occured While deleting. Please try again!");
          }
      }
    });
}

function start_target_functionality(tagname,play_link,username, input_username){
    $.ajax({
      url: play_link,
      type: "GET",
      data: {
          'username': username,
          'input_username': input_username,
          'link_id': tagname
      },
      contentType: "application/json;charset=utf-8",
      dataType: "json",
      success: function(data) {
            document.getElementById(tagname).innerHTML = '<i class="fa fa-pause" aria-hidden="true"></i>';
            document.getElementById(tagname).setAttribute('onclick', "pause_target_functionality('"+tagname+"','"+data.url+"','"+username+"','"+input_username+"','"+data.pid+"')");
        }
    });
}
function pause_target_functionality(tagname,pause_link,username, input_username, pid){
  $.ajax({
      url: pause_link,
      type: "GET",
      data: {
          'username': username,
          'input_username': input_username,
          'pid': pid,
          'link_id': tagname
      },
      contentType: "application/json;charset=utf-8",
      dataType: "json",
      success: function(data) {
            document.getElementById(tagname).innerHTML = '<i class="fa fa-play" aria-hidden="true"></i>';
            document.getElementById(tagname).setAttribute('onclick', "start_target_functionality('"+tagname+"','"+data.url+"','"+username+"','"+input_username+"')");
        }
    });
}

function submit_info(button_name) {
    var max_follows_per_hour = '';
    var id = '';
    if (button_name == 'username_submit') {
        max_follows_per_hour = $("#username_max_follows_per_hour").val();
        id = 'username_display_error';
    }
    else if (button_name == 'tags_submit') {
        max_follows_per_hour = $("#tag_max_follows_per_hour").val();
        id = 'tag_display_error';
    }
    if (parseInt(max_follows_per_hour) > 30) {
        document.getElementById(id).innerHTML = 'Hours should be less then 30.';
        return;
    }
    $('#myModal').modal('toggle');
    var username = $("#username").text();
    $('#dashboard_body').css({'opacity': 0.5});
    document.getElementById('loader').style.display = 'block';


    if (button_name == 'username_submit') {
        var input = $("#username_input").val();
        $.ajax({
            url: "/dashboard_functions",
            type: "GET",
            data: {
                'username': username,
                'input': input,
                'max_follows_per_hour': max_follows_per_hour,
                'button_clicked': button_name
            },
            contentType: "application/json;charset=utf-8",
            dataType: "json",
            success: function (data) {
                data1 = '<div class="col-md-4"><div class="card" style="width: 13rem; margin-bottom: 30px;">' +
                    '<div style="background-color: lightblue; position: relative;padding:10px;text-align: center;">' +
                    '<span class="card-title" style="color: darkblue"><b>' + data.user.input_username + '</b></span></div>' +
                    '<div style="padding-top: 10px;">' +
                    '<div class="row" style="padding: 0px 10px 10px 10px;">' +
                    '<span class="col-md-4" >Following</span>' +
                    '<span class="col-md-3"></span>' +
                    '<span class="col-md-5" >' + data.user.following + '</span><br>' +
                    '</div>' +
                    '<div class="row" style="padding: 0px 10px 10px 10px;">' +
                    '<span class="col-md-4" >Follows</span>' +
                    '<span class="col-md-3"></span>' +
                    '<span class="col-md-5" >' + data.user.follow + '</span><br>' +
                    '</div>' +
                    '</div>' +
                    '<div class="" align="right" style="padding: 0px 10px 10px 10px;"><hr> ' +
                    '<a class="btn btn-primary fa-size" type="button" id="' + data.user.link_id + '" onclick="' + "pause_target_functionality(" + "'" + data.user.link_id + "','" + data.user.pause_link + "','" + data.user.username + "','" + data.user.input_username + "','" + data.user.pid + "');" + '">' +
                    "<i class='fa fa-pause' aria-hidden='true'></i></a> " +
                    '<a class="btn btn-warning fa-size" type="button" id="' + data.user.link_id + '" onclick="' + "delete_target_functionality(" + "'" + data.user.link_id + "','" + data.user.delete_link + "','" + data.user.username + "','" + data.user.pid + "');" + '">' +
                    "<i class='fa fa-trash' aria-hidden='true'></i>" +
                    '</a> ' +
                    '</div>' +
                    ' </div>' +
                    '</div></div>';
                $('#dashboard_body').css({'opacity': 1});
                document.getElementById('loader').style.display = 'None';

                document.getElementById("cards_panel").innerHTML += data1;
            }
        });
    }
    else if (button_name == 'tags_submit') {
        input = $("#tags_input").val();
        $.ajax({
            url: "/dashboard_functions",
            type: "GET",
            data: {
                'username': username,
                'max_follows_per_hour': max_follows_per_hour,
                'input': input,
                'button_clicked': button_name
            },
            contentType: "application/json;charset=utf-8",
            dataType: "json",
            success: function (data) {
                data1 = '<div class="col-md-4"><div class="card" style="width: 13rem; margin-bottom: 30px;">' +
                    '<div style="background-color: lightblue; position: relative;padding:10px;text-align: center;">' +
                    '<span class="card-title" style="color: darkblue"><b>' + data.user.input_tag + '</b></span></div>' +
                    '<div style="padding-top: 10px;">' +
                    '<div class="row" style="padding: 0px 10px 10px 10px;">' +
                    '<span class="col-md-5" >MEDIA_IDS</span>' +
                    '<span class="col-md-2"></span>' +
                    '<span class="col-md-5" >' + data.user.following + '</span><br>' +
                    '</div>' +
                    '<div class="row" style="padding: 0px 10px 10px 10px;">' +
                    '<span class="col-md-5" >USER_IDS</span>' +
                    '<span class="col-md-2"></span>' +
                    '<span class="col-md-5" >' + data.user.follow + '</span><br>' +
                    '</div>' +
                    '</div>' +
                    '<div class="" align="right" style="padding: 0px 10px 10px 10px;"><hr> ' +
                    '<a class="btn btn-primary fa-size" type="button" id="' + data.user.link_id + '" onclick="' + "pause_target_functionality(" + "'" + data.user.link_id + "','" + data.user.pause_link + "','" + data.user.username + "','" + data.user.input_tag + "','" + data.user.pid + "');" + '">' +
                    "<i class='fa fa-pause' aria-hidden='true'></i></a> " +
                    '<a class="btn btn-warning fa-size" type="button" id="' + data.user.link_id + '" onclick="' + "delete_target_functionality(" + "'" + data.user.link_id + "','" + data.user.delete_link + "','" + data.user.username + "','" + data.user.pid + "');" + '">' +
                    "<i class='fa fa-trash' aria-hidden='true'></i>" +
                    '</a> ' +
                    '</div>' +
                    ' </div>' +
                    '</div></div>';

                $('#dashboard_body').css({'opacity': 1});
                document.getElementById('loader').style.display = 'None';

                document.getElementById("cards_panel").innerHTML += data1;
            }
        });
    }
}