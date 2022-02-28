var uid;

$(function(){
    
    var mm;
    var listeningTime = 0;
    var second = 0;
    var endSec = 0;
    var minute = 0;
    var endMin = 0;
    var playing = false;

    function calc(end_min, end_sec) {
        if(playing) {
            clearInterval(mm);
        }else {
            playing = true;
        }
        second = 0;
        minute = 0;
        endSec = end_sec;
        endMin = end_min;
        mm = setInterval(function() {
            second += 1;
            if (second === 60){
                minute += 1;
                second = 0;
            }
            if (minute === endMin && second === endSec){
                minute = 0;
                second = 0;
            }

            listeningTime++;
            if(listeningTime === 5) {
                postData('https://linefresh-tiehua.herokuapp.com/listening', {user_id: uid});
                listeningTime = 0;
            }
            console.log("totalTime = "+listeningTime);

            $('#ply-min').text('0'+minute);
            if (second < 10){
                $('#ply-sec').text('0'+second);
            }else {
                $('#ply-sec').text(second);
            }
        }, 1000);
    }

    $('#playlist-btn').click(function(){
        $('#ply-min').text('00');
        $('#ply-sec').text('00');
        $('#song-name').text("Tengilen");
        $('#nowImg').attr("src", "../static/img/anu.png");
        $('#totalTime').text("/04:32");
        calc(4, 32);
    });
    $('#song1').click(function() {
        //alert("you clicked the song1");
        $('#ply-min').text('00');
        $('#ply-sec').text('00');
        $('#song-name').text("Tengilen");
        $('#nowImg').attr("src", "../static/img/anu.png");
        $('#totalTime').text("/04:32");
        calc(4, 32);
    });
    $('#song2').click(function() {
        //alert("you clicked the song2");
        $('#ply-min').text('00');
        $('#ply-sec').text('00');
        $('#song-name').text("愛 Ayi");
        $('#nowImg').attr("src", "../static/img/balai.png");
        $('#totalTime').text("/06:41");
        calc(6, 41);
    });
    $('#song3').click(function() {
        //alert("you clicked the song3");
        $('#ply-min').text('00');
        $('#ply-sec').text('00');
        $('#song-name').text("水災");
        $('#nowImg').attr("src", "../static/img/matzka.png");
        $('#totalTime').text("/04:32");
        calc(4, 32);
    });
    $('#song4').click(function() {
        //alert("you clicked the song4");
        $('#ply-min').text('00');
        $('#ply-sec').text('00');
        $('#song-name').text("Ari");
        $('#nowImg').attr("src", "../static/img/BouBu.png");
        $('#totalTime').text("/1:30");
        calc(1, 30);
    });
    $('#song5').click(function() {
        //alert("you clicked the song5");
        $('#ply-min').text('00');
        $('#ply-sec').text('00');
        $('#song-name').text("採集");
        $('#nowImg').attr("src", "../static/img/exit.png");
        $('#totalTime').text("/05:25");
        calc(5, 25);
    });
    $('#song6').click(function() {
        //alert("you clicked the song6");
        $('#ply-min').text('00');
        $('#ply-sec').text('00');
        $('#song-name').text("者波 cepo'");
        $('#nowImg').attr("src", "../static/img/cepo.png");
        $('#totalTime').text("/05:44");
        calc(5, 44);
    });
    $('#song7').click(function() {
        //alert("you clicked the song7");
        $('#ply-min').text('00');
        $('#ply-sec').text('00');
        $('#song-name').text("一直走");
        $('#nowImg').attr("src", "../static/img/andong.png");
        $('#totalTime').text("/03:31");
        calc(3, 31);
    });
    $('#song8').click(function() {
        //alert("you clicked the song8");
        $('#ply-min').text('00');
        $('#ply-sec').text('00');
        $('#song-name').text("毛毛歌");
        $('#nowImg').attr("src", "../static/img/longLive.png");
        $('#totalTime').text("/03:53");
        calc(3, 53);
    });
    $('#song9').click(function() {
        //alert("you clicked the song9");
        $('#ply-min').text('00');
        $('#ply-sec').text('00');
        $('#song-name').text("致布農青春");
        $('#nowImg').attr("src", "../static/img/paliulius.png");
        $('#totalTime').text("/04:38");
        calc(4, 38);
    });
    $('#song10').click(function() {
        //alert("you clicked the song10");
        $('#ply-min').text('00');
        $('#ply-sec').text('00');
        $('#song-name').text("致布農青春");
        $('#nowImg').attr("src", "../static/img/paliulius.png");
        $('#totalTime').text("/04:38");
        calc(4, 38);
    });
    $('#play-btn').click(function(){
        if(second === 0 && minute === 0 && !playing) {
            $('#ply-min').text('00');
            $('#ply-sec').text('00');
            $('#song-name').text("後山的山");
            $('#nowImg').attr("src", "../static/img/125.png");
            $('#totalTime').text("/05:01");
            calc(5, 1);
        }else {
            if(playing) {
                playing = false;
                clearInterval(mm);
            }else {
                playing = true;
                mm = setInterval(function() {
                    second += 1;
                    if (second === 60){
                        minute += 1;
                        second = 0;
                    }
                    $('#ply-min').text('0'+minute);
                    if (second < 10){
                        $('#ply-sec').text('0'+second);
                    }else {
                        $('#ply-sec').text(second);
                    }

                    if (minute === endMin && second === endSec){
                        minute = 0;
                        second = 0;
                    }

                    listeningTime++;
                    if(listeningTime === 5) {
                        postData('https://linefresh-tiehua.herokuapp.com/listening', {user_id: uid});
                        listeningTime = 0;
                    }
                    console.log("totalTime = "+listeningTime);
                }, 1000);
            }
        }
    });
});

window.onload = function (e) {
    liff.init({
        liffId: '1656598921-KN0L4QqG'
    }).then(() => {
        liff.getProfile().then(profile => {
            const userId = profile.userId;
            window.alert("點選播放任一歌曲，聆聽超過五秒即可完成任務");
            uid = userId;
        });
    });
};

function postData(url, data) {
    return fetch(url, {
        body: JSON.stringify(data),
        cache: 'no-cache',
        headers: {'content-type': 'application/json'},
        method: 'POST',
        mode: 'cors',
    })
}