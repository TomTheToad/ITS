/* Javascript for ITS web data handling */

/* --- Client's Page --- */
// Load client information and reload page
function setClient() {
    var selected_client = $('#client_select :selected').val();
    var new_location = "http://localhost:5000/clients/" + selected_client;
    window.location.replace(new_location);
}

// Enable form editing by making inputs live
function editForm() {
    $(':disabled').css('background-color', 'white');
    $(':disabled').prop('disabled', false);
    setCurrentSpecies();
}

// Sets hidden field of new_client to True
function newClient() {
    editForm();
    $('#new_client').prop('value', 'True');
}

// Set current species in hidden field
function setCurrentSpecies() {
    var selected_species = $('#species_select :selected').val();
    $('#current_species').prop('value', selected_species);
}

// Deletes a client with warning without leaving the client's page
function deleteClient(){
    if (confirm("Are you sure you to delete this client?")) {
        delete_client= $('#client_id').val();
        var new_location = "http://localhost:5000/delete_client/" + delete_client
        window.location.replace(new_location)
    } else {
        window.location.replace("http://localhost:5000/clients")
    }
}

// Redirects to create_trip page and sends client_id
function bookTravel() {
    var client = $('#client_id').val();
    new_location = "http://localhost:5000/create_trip/" + client;
    window.location.replace(new_location)
}



/* --- Create Trip --- */
// Sets hidden value where (destination)
function setWhere(where, name) {
    $('#trip_where').prop('value', where);
    $('#destination').html('Destination: ' + name);
    $('#destination').css('color', 'green');
}

// sets travel method in hidden input
function setHow(how, name) {
    $('#trip_how').prop('value', how);
    $('#travel').html('Travel Method: ' + name);
    $('#travel').css('color', 'green');
}

// sets food choice in hidden input
function setFood(food, name) {
    $('#trip_food').prop('value', food);
    $('#food').html('Cuisine: ' + name);
    $('#food').css('color', 'green');
}

// Checks the value of a given item
function checkValue(toCheck, item) {
    if (toCheck == 'not_selected') {
        var message = "Please select a " + item;
        alert(message);
        return false;
    } else {
        return true;
    }

}

// form validation to check to see that
// all necessary choices are complete
// calls checkValue
function checkForm() {
    var setWhere = $('#trip_where').val();
    var setHow = $('#trip_how').val();
    var setFood = $('#trip_food').val();

    var feedback1 = checkValue(setWhere, "Destination.");
    if (feedback1 == true) {
        var feedback2 = checkValue(setHow, "Method of Travel.");
        if (feedback2 == true) {
            var feedback3 = checkValue(setFood, "Meal");
            if (feedback3 == true) {
                $('#create_trip').submit();
            }
        }
    }
}

/* agent_testing */
// form validation to check to see that
// all necessary choices are complete
// calls checkValue
function checkTestForm() {
    var setWhere = $('#trip_where').val();
    var setHow = $('#trip_how').val();
    var setFood = $('#trip_food').val();

    var feedback1 = checkValue(setWhere, "Destination.");
    if (feedback1 == true) {
        var feedback2 = checkValue(setHow, "Method of Travel.");
        if (feedback2 == true) {
            var feedback3 = checkValue(setFood, "Meal");
            if (feedback3 == true) {
                $('#agent_testing').submit();
            }
        }
    }
}

