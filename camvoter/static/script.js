$(document).ready(function(){
    var width = 200, height = 200;
    
    var bleeper = d3.select('#votes')
        .attr('width', width)
        .attr('height', height)
        .append('g').attr('class', 'bleeper');
    bleeper.append('circle')
        .attr('fill', 'red')
        .attr('cx', width/2)
        .attr('cy', height/2)
    ;
    
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('vote count', function(msg) {
        bleeper.datum(msg.data).select('circle')
            .attr('r', function(d) {
                return d.count;
            })
        ;
        $('#vote_count').html('<p>Received: ' + JSON.stringify(msg.data) + '</p>');
    });

    setInterval(function() {
        socket.emit('get votes', {'data':'nothing to say'})
    }, 500); 
});
