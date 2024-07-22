// script.js

document.addEventListener('DOMContentLoaded', function() {
    // Function to generate passenger input fields
    function generatePassengerFields(numPassengers) {
        var passengerDetails = document.getElementById('passenger-form');
        passengerDetails.innerHTML = ''; // Clear existing fields

        for (var i = 0; i < numPassengers; i++) {
            var passengerDiv = document.createElement('div');
            passengerDiv.className = 'passenger';

            // Passenger number label
            var passengerLabel = document.createElement('label');
            passengerLabel.textContent = 'Passenger ' + (i + 1);
            passengerDiv.appendChild(passengerLabel);

            // First name input
            var firstNameLabel = document.createElement('label');
            firstNameLabel.textContent = 'First Name:';
            var firstNameInput = document.createElement('input');
            firstNameInput.type = 'text';
            firstNameInput.name = 'passenger-first-name-' + (i + 1);
            firstNameInput.required = true;

            // Last name input
            var lastNameLabel = document.createElement('label');
            lastNameLabel.textContent = 'Last Name:';
            var lastNameInput = document.createElement('input');
            lastNameInput.type = 'text';
            lastNameInput.name = 'passenger-last-name-' + (i + 1);
            lastNameInput.required = true;

            // Age input
            var ageLabel = document.createElement('label');
            ageLabel.textContent = 'Age:';
            var ageInput = document.createElement('input');
            ageInput.type = 'number';
            ageInput.name = 'passenger-age-' + (i + 1);
            ageInput.min = '1';
            ageInput.required = true;

            // Gender input
            var genderLabel = document.createElement('label');
            genderLabel.textContent = 'Gender:';
            var genderInput = document.createElement('select');
            genderInput.name = 'passenger-gender-' + (i + 1);
            genderInput.required = true;
            var genderOptions = ['Male', 'Female', 'Other'];
            genderOptions.forEach(function(option) {
                var optionElement = document.createElement('option');
                optionElement.textContent = option;
                genderInput.appendChild(optionElement);
            });

            // Phone number input
            var phoneLabel = document.createElement('label');
            phoneLabel.textContent = 'Phone Number:';
            var phoneInput = document.createElement('input');
            phoneInput.type = 'tel';
            phoneInput.name = 'passenger-phone-' + (i + 1);
            phoneInput.required = true;

            // Append inputs to passengerDiv
            passengerDiv.appendChild(firstNameLabel);
            passengerDiv.appendChild(firstNameInput);
            passengerDiv.appendChild(lastNameLabel);
            passengerDiv.appendChild(lastNameInput);
            passengerDiv.appendChild(ageLabel);
            passengerDiv.appendChild(ageInput);
            passengerDiv.appendChild(genderLabel);
            passengerDiv.appendChild(genderInput);
            passengerDiv.appendChild(phoneLabel);
            passengerDiv.appendChild(phoneInput);

            // Append passengerDiv to passengerDetails
            passengerDetails.appendChild(passengerDiv);
        }
    }

    // Initial generation of passenger input fields
    var numPassengersInput = document.getElementById('num-passengers');
    generatePassengerFields(numPassengersInput.value);

    // Event listener to regenerate passenger input fields when number of passengers changes
    numPassengersInput.addEventListener('change', function() {
        generatePassengerFields(this.value);
    });
});

function BookTicket(){
    alert("YYYYYYYYYYYYYYY");
    var numPassengers = document.getElementById('num-passengers').value;
    console.log("Number of Passengers:", numPassengers);
}

