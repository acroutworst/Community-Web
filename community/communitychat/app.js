'use strict';

// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// AngularJS Chat Configuration
// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
angular.module('chat').constant( 'config', {
    "pubnub": {
        "publish-key"   : "pub-c-db3d4187-7d40-4dc2-9875-e6cd88d27be3",
        "subscribe-key" : "sub-c-09b0e576-a561-11e6-81d1-0619f8945a4f"
    }
} );

// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// Chat App Module
// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
var basicChat = angular.module( 'BasicChat', ['chat'] );

// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// Chat App Controller
// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
basicChat.controller( 'BasicController', [ 'Messages', function( Messages ) {

    // Self Object
    var chat = this;

    // Sent Indicator
    chat.status = "";

    // Keep an Array of Messages
    chat.messages = [];

    // Set User Data
    Messages.user({ name : sillyname() });

    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    // Empty the array of messages
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    function empty(){
        chat.messages.length = 0;
    }
    
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    // Get Received Messages and Add it to Messages Array.
    // This will automatically update the view.
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    var chatmessages = document.querySelector(".chat-messages");
    Messages.receive(function(msg){
        chat.messages.push(msg);
        if (JSON.stringify(msg) === "clear()"){
            empty();
        }
        setTimeout( function() {
            chatmessages.scrollTop = chatmessages.scrollHeight;
        }, 1200 );
    });

    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    // Send Messages
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    chat.send = function() {
        Messages.send({ data : chat.textbox });
        if (chat.textbox === "clear()"){
            empty();
        }
        chat.status = "sending";
        chat.textbox = "";
        setTimeout( function() { chat.status = "" }, 1200 );
    };

} ] );
