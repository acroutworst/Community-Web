'use strict';

// Return a Silly Name
function sillyname() {
    // Basic Random
    function rnd(n) { return Math.floor(Math.random()*n) }

    // First Name
    return ["Anonymous"] +

    // Last Name
    ["Giraffe","Elephant","Aardvark","Squirrel","Tiger","Kitty",
    "Puppy","Snake","Velociraptor","Dinosaur","Guppy",
    "Shark","Anteater","Birdie"][rnd(14)];
}
