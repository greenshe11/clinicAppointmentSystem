// script.js

// Define an array to store events
let events = [];

// letiables to store event input fields and reminder list
let eventDateInput =
    document.getElementById("eventDate");
let eventTitleInput =
    document.getElementById("eventTitle");
let eventDescriptionInput =
    document.getElementById("eventDescription");
let reminderList =
    document.getElementById("reminderList");

// Counter to generate unique event IDs
let eventIdCounter = 1;



// Function to delete an event by ID
function deleteEvent(eventId) {
    // Find the index of the event with the given ID
    let eventIndex =
        events.findIndex((event) =>
            event.id === eventId);

    if (eventIndex !== -1) {
        // Remove the event from the events array
        events.splice(eventIndex, 1);
        preShowCalendar(currentMonth, currentYear);
        displayReminders();
    }
}

function getAppointments(month, year, day) {
    return fetch(`http://localhost:5000/api/appointments/forPatient?month=${month}&day=${day}&year=${year}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            return data; // Return the data to the caller
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            return []; // Return an empty array on error
        });
}


// Function to display reminders

// Function to generate a range of 
// years for the year select input
function generate_year_range(start, end) {
    let years = "";
    for (let year = start; year <= end; year++) {
        years += "<option value='" +
            year + "'>" + year + "</option>";
    }
    return years;
}

// Initialize date-related letiables
today = new Date();
currentMonth = today.getMonth();
currentYear = today.getFullYear();
selectYear = document.getElementById("year");
selectMonth = document.getElementById("month");

createYear = generate_year_range(1970, 2050);

document.getElementById("year").innerHTML = createYear;

let calendar = document.getElementById("calendar");

let months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
];
let days = [
    "Sun", "Mon", "Tue", "Wed",
    "Thu", "Fri", "Sat"];

$dataHead = "<tr>";
for (dhead in days) {
    $dataHead += "<th data-days='" +
        days[dhead] + "'>" +
        days[dhead] + "</th>";
}
$dataHead += "</tr>";

document.getElementById("thead-month").innerHTML = $dataHead;

monthAndYear =
    document.getElementById("monthAndYear");

preShowCalendar(currentMonth, currentYear);

// Function to navigate to the next month
function next() {
    currentYear = currentMonth === 11 ?
        currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    preShowCalendar(currentMonth, currentYear);
}

// Function to navigate to the previous month
function previous() {
    currentYear = currentMonth === 0 ?
        currentYear - 1 : currentYear;
    currentMonth = currentMonth === 0 ?
        11 : currentMonth - 1;
    preShowCalendar(currentMonth, currentYear);
}

// Function to jump to a specific month and year
function jump() {
    currentYear = parseInt(selectYear.value);
    currentMonth = parseInt(selectMonth.value);
    preShowCalendar(currentMonth, currentYear);
}

// Function to display the calendar
function resetClassName(newClass, oldClass) {
    // Get all elements with the old class name
    const elements = document.getElementsByClassName(oldClass);
    
    // Convert the HTMLCollection to an array to avoid live updates issue
    const elementsArray = Array.from(elements);
    
    // Loop through the elements and change their class name
    elementsArray.forEach(element => {
        element.className = newClass;
    });
}

function getAvailableTime(data){
    let hoursAll = [8,9,10,11,1,2,3,4]
    for (i=0; i<data.length; i++){
        const valueToRemove = data[i].appointment_hour
        // Find the index of the value
        const index = hoursAll.indexOf(valueToRemove);

        // Remove the element if found
        if (index !== -1) {
            hoursAll.splice(index, 1);
        }
    }
    return hoursAll
}
/*Hours:
8,9,10,11,1,2,3,4 */
function fetchAppointments(month, year, day, callback){
    getAppointments(month, year, day)
    .then(times => {
        callback(times)
    });
}

function timeChooser(hours) {
    // Get the collection of elements with the class 'hoursChoices'
    const dropDowns = document.getElementsByClassName("hoursChoices");
    
    // Ensure there's at least one element with the class name
    if (dropDowns.length > 0) {
        const dropDown = dropDowns[0]; // Access the first element in the collection

        // Clear existing options
        dropDown.innerHTML = '';

        // Create options for the dropdown
        let initial = '';
        const createChoice = (time) => {
            let value = time;
            if (time >= 8) {
                return `<option value="${value}">${value}:00 AM</option>`;
            } else {
                return `<option value="${value}">${value}:00 PM</option>`;
            }
        };

        // Append each option to the dropdown
        for (let i = 0; i < hours.length; i++) {
            initial += createChoice(hours[i]);
        }
        dropDown.innerHTML = initial;

    } else {
        console.error('No elements found with the class name "hoursChoices".');
    }
}

function sendFullDate(event){
    // Accessing the event's target element
    resetClassName('date-picker', 'date-picker date-active')
    const element = event.target.closest('td.date-picker');
    const month = element.getAttribute('data-month');
    const day = element.getAttribute('data-day');
    const year = element.getAttribute('data-year');
    let preReturn = false
    if (month == null || month == 'null'){
        preReturn = true
    }
    
    if (element.className != "date-picker"){
        preReturn = true
    }
    

    if (preReturn) {return timeChooser([])}
    element.className = element == `${element.className} date-active`? element.className : `${element.className} date-active`;
    fetchAppointments(month, year, day, (data) => {timeChooser(getAvailableTime(data))})
    // Method 1: Using getAttribute to access data attribute
   

    console.log(month, day, year)    
    

   
        

    // Method 2: Using dataset to access data attribute (Note: Dataset works with camelCase)
    
}

function isDateLessThanCurrent(year, month, day) {
    // Create a Date object for the current date
    const currentDate = new Date();
    
    // Create a Date object for the given date
    // Note: Month is 0-based in JavaScript's Date object, so we subtract 1 from the given month
    const givenDate = new Date(year, month - 1, day);
    
    return givenDate < currentDate;
}

function preShowCalendar(month, year){
    fetchAppointments(month+1, year, "null", (data)=>{showCalendar(month, year, data)})
}

function showCalendar(month, year, monthData) {
    let firstDay = new Date(year, month, 1).getDay();
    tbl = document.getElementById("calendar-body");
    tbl.innerHTML = "";
    monthAndYear.innerHTML = months[month] + " " + year;
    selectYear.value = year;
    selectMonth.value = month;
    console.log(monthData)
    
    

    const getFilledCount = (day, year) =>{
        let count = 0
        for (i=0; i<monthData.length; i++){
            if (monthData[i].appointment_day == day &&
                monthData[i].appointment_year == year
            ){
                count = count + 1
            }
        }
        return count
    }

    const evaluateCount = () =>{
        if (getFilledCount(date, year)>8){
            cell.className = `${cell.className} filled`
            return true
        }
        return false
    }

    let date = 1;
    for (let i = 0; i < 6; i++) {
        let row = document.createElement("tr");
        for (let j = 0; j < 7; j++) {
            if (i === 0 && j < firstDay) {
                cell = document.createElement("td");
                cellText = document.createTextNode("");
                cell.appendChild(cellText);
                row.appendChild(cell);
            } else if (date > daysInMonth(month, year)) {
                break;
            } else {
                cell = document.createElement("td");
                cell.className = "date-picker";
                cell.innerHTML = "<span>" + date + "</span";
                cell.onclick = (event) => {sendFullDate(event)}

                if (j==6 || j==0 || evaluateCount()){
                    cell.setAttribute("data-day", null);
                    cell.setAttribute("data-month", null);
                    cell.setAttribute("data-year", null);
                    cell.setAttribute("data-month_name", months[month]);
                }
                else if(
                    date === today.getDate() &&
                    year === today.getFullYear() &&
                    month === today.getMonth())
                {
                    cell.setAttribute("data-day", null);
                    cell.setAttribute("data-month", null);
                    cell.setAttribute("data-year", null);
                    cell.setAttribute("data-month_name", months[month]);
                  
                    cell.className = `${cell.className} today`;
                    
                    
                }
                else{
                    
                    cell.setAttribute("data-day", date);
                    cell.setAttribute("data-month", month + 1);
                    cell.setAttribute("data-year", year);
                    cell.setAttribute("data-month_name", months[month]);
                    
    
                }
                
                if (isDateLessThanCurrent(year, month+1, date)){
                    cell.className = `${cell.className} done`
                }
                row.appendChild(cell);
                date++;
                
            }
        }
        tbl.appendChild(row);
    }
}



// Function to get the number of days in a month
function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}
