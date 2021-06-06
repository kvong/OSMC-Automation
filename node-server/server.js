const express = require('express');
const fs = require("fs");
const app = express();
const exec = require('child_process').exec;
const path = require('path');

app.use(express.static(path.join(__dirname, 'public')));

function execute(command, callback){
        exec(command, function(error, stdout, stderr){ callback(stdout);  });
}


app.get('/', function( req, res ) {
    res.sendFile( '/home/osmc/node-server/index.html' );
})

// Play FRIENDS
app.get('/friends', function( req, res ) {
    fs.writeFile('/home/osmc/.kodi/userdata/Automation.dat/selected_show.dat', 'FRIENDS', ( error ) => {
        if ( error ) throw err;
    });
    res.send('Selected Show: FRIENDS');
    execute('shutdown -r now', (cb) => {} );
})
// Play HIMYM
app.get('/himym', function( req, res ) {
    fs.writeFile('/home/osmc/.kodi/userdata/Automation.dat/selected_show.dat', 'HIMYM', ( error ) => {
        if ( error ) throw err;
    });
    res.send('Selected Show: BigBang');
    execute('shutdown -r now', (cb) => {} );
})
// Play BigBang
app.get('/bigbang', function( req, res ) {
    fs.writeFile('/home/osmc/.kodi/userdata/Automation.dat/selected_show.dat', 'BigBang', ( error ) => {
        if ( error ) throw err;
    });
    res.send('Selected Show: BigBang');
    execute('shutdown -r now', (cb) => {} );
})

const server = app.listen( 3000, function() {
    const host = server.address().address
    const port = server.address().port

    console.log( 'Server launched on port 3000' )
} )


