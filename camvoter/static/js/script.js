$(document).ready(function(){
    var width = 200, height = 200;
    var lastVoteCount = 0;
    var lastVoteTime = Date.now();
    var totalVotes = 0;
    var isVoting = false;
    var voteDuration = 10;
    var bleeper = d3.select('#votes')
        .attr('width', width)
        .attr('height', height)
        .append('g').attr('class', 'bleeper');
    bleeper.append('circle')
        .attr('fill', 'red')
        .attr('cx', width/2)
        .attr('cy', height/2);

    $(document).keypress(function(e){
        console.log(e);
        if( e.keyCode == 32 ) startVoting();
    });
    
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('vote count', function(msg) {
        var count = msg.data.count;
        bleeper.datum(msg.data).select('circle')
            .attr('r', function(d) {
                return d.count;
            })
        ;
        //$('#vote_count').html('<p>Received: ' + JSON.stringify(msg.data) + '</p>');
        var voteTime = Date.now();
        if( voteDuration < 0.001*( voteTime - voteStartTime ) ){
            isVoting = false;
            voteTime = voteStartTime+1000*voteDuration;
        }
        totalVotes += 0.5 * ( lastVoteCount + count ) * 0.001 * ( voteTime - lastVoteTime );
        lastVoteTime = voteTime;
        lastVoteCount = count;
        //$('#vote_count').html('<p>Votes '+totalVotes+'</p>');
    });

    var startVoting = function(){
        lastVoteTime = voteStartTime = Date.now();
        isVoting = true;
        totalVotes = 0;
        lastVoteCount = 0;
    }

    /*
    setInterval(function() {
        if( isVoting ) socket.emit('get votes', {'data':'nothing to say'});
        
    }, 40); */

    var update = function(){
        if( isVoting ) socket.emit('get votes', {'data':'nothing to say'});
        window.requestAnimationFrame = update;
    }

    update();
});
