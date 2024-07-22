function generatePassengerFields(numPassengers) {
    const passengerFieldsDiv = document.querySelector('.passenger-details');

    // Clear existing passenger details
    passengerFieldsDiv.innerHTML = '';

    for (let i = 0; i < numPassengers; i++) {
        const passengerDiv = document.createElement('div');
        passengerDiv.classList.add('passenger');

        // Create and append label for the passenger
        const label = document.createElement('label');
        label.textContent = `Passenger ${i + 1}`;
        passengerDiv.appendChild(label);

        // Create and append input fields for passenger details
        const firstNameInput = document.createElement('input');
        firstNameInput.setAttribute('type', 'text');
        firstNameInput.setAttribute('placeholder', 'First Name');
        firstNameInput.setAttribute('required', 'required');
        passengerDiv.appendChild(firstNameInput);

        const lastNameInput = document.createElement('input');
        lastNameInput.setAttribute('type', 'text');
        lastNameInput.setAttribute('placeholder', 'Last Name');
        lastNameInput.setAttribute('required', 'required');
        passengerDiv.appendChild(lastNameInput);

        const genderSelect = document.createElement('select');
        const genderOption1 = document.createElement('option');
        genderOption1.setAttribute('value', 'male');
        genderOption1.textContent = 'Male';
        genderSelect.appendChild(genderOption1);
        const genderOption2 = document.createElement('option');
        genderOption2.setAttribute('value', 'female');
        genderOption2.textContent = 'Female';
        genderSelect.appendChild(genderOption2);
        genderSelect.setAttribute('required', 'required');
        passengerDiv.appendChild(genderSelect);

        const ageInput = document.createElement('input');
        ageInput.setAttribute('type', 'number');
        ageInput.setAttribute('placeholder', 'Age');
        ageInput.setAttribute('required', 'required');
        passengerDiv.appendChild(ageInput);

        const mobileInput = document.createElement('input');
        mobileInput.setAttribute('type', 'tel');
        mobileInput.setAttribute('placeholder', 'Mobile Number');
        mobileInput.setAttribute('required', 'required');
        passengerDiv.appendChild(mobileInput);

        // Append the passenger details div to the parent container
        passengerFieldsDiv.appendChild(passengerDiv);
    }
}

function validatePassengerFields() {
    const passengerFieldsDiv = document.querySelector('.passenger-details');
    const inputs = passengerFieldsDiv.querySelectorAll('input, select');
    for (const input of inputs) {
        if (!input.checkValidity()) {
            alert("Please fill in all passenger details.");
            return false;
        }
    }
    location.href = '/book-flight/{{flight.id}}';
    return true;
}

// Example usage: Assuming numPassengers is available as an input parameter
const numPassengers = 3; // Replace this with the actual number of passengers
generatePassengerFields(numPassengers);

document.querySelector('button').addEventListener('click', function(event) {
    if (!validatePassengerFields()) {
        event.preventDefault(); // Prevent the button from submitting the form or redirecting
    } else {
        location.href = '/book-flight/{{flight.id}}';
    }
});
