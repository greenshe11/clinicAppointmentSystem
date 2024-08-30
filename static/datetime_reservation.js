// script.js

// Define an array to store events
let events = [];

// Variables to store event input fields and reminder list
let eventDateInput = document.getElementById("dr-eventDate");
let eventTitleInput = document.getElementById("dr-eventTitle");
let eventDescriptionInput = document.getElementById("dr-eventDescription");
let reminderList = document.getElementById("dr-reminderList");

// Counter to generate unique event IDs
let eventIdCounter = 1;

// Function to delete an event by ID
function deleteEvent(eventId) {
    let eventIndex = events.findIndex((event) => event.id === eventId);
    if (eventIndex !== -1) {
        events.splice(eventIndex, 1);
        preShowCalendar(currentMonth, currentYear);
        displayReminders();
    }
}

function getAppointments(month, year, day) {
    return fetch(`http://localhost:5000/api/appointments/forPatient?Appointment_Month=${month}&Appointment_Day=${day}&Appointment_Year=${year}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            return [];
        });
}

function generate_year_range(start, end) {
    let years = "";
    for (let year = start; year <= end; year++) {
        years += "<option value='" + year + "'>" + year + "</option>";
    }
    return years;
}

// Initialize date-related variables
today = new Date();
currentMonth = today.getMonth();
currentYear = today.getFullYear();
selectYear = document.getElementById("dr-year");
selectMonth = document.getElementById("dr-month");

createYear = generate_year_range(1970, 2050);

document.getElementById("dr-year").innerHTML = createYear;

let calendar = document.getElementById("dr-calendar");

let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
let days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

$dataHead = "<tr>";
for (dhead in days) {
    $dataHead += "<th data-days='" + days[dhead] + "'>" + days[dhead] + "</th>";
}
$dataHead += "</tr>";

document.getElementById("dr-thead-month").innerHTML = $dataHead;

monthAndYear = document.getElementById("dr-monthAndYear");

preShowCalendar(currentMonth, currentYear);

function next() {
    currentYear = currentMonth === 11 ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    preShowCalendar(currentMonth, currentYear);
}

function previous() {
    currentYear = currentMonth === 0 ? currentYear - 1 : currentYear;
    currentMonth = currentMonth === 0 ? 11 : currentMonth - 1;
    preShowCalendar(currentMonth, currentYear);
}

function jump() {
    currentYear = parseInt(selectYear.value);
    currentMonth = parseInt(selectMonth.value);
    preShowCalendar(currentMonth, currentYear);
}

function resetClassName(newClass, oldClass) {
    const elements = document.getElementsByClassName(oldClass);
    const elementsArray = Array.from(elements);
    elementsArray.forEach(element => {
        element.className = newClass;
    });
}

function getAvailableTime(data){
    let hoursAll = [8,9,10,11,1,2,3,4];
    for (i=0; i<data.length; i++){
        const valueToRemove = data[i].Appointment_Time;
        const index = hoursAll.indexOf(valueToRemove);
        if (index !== -1) {
            hoursAll.splice(index, 1);
        }
    }
    return hoursAll;
}

function fetchAppointments(month, year, day, callback){
    getAppointments(month, year, day).then(times => {
        callback(times);
    });
}

function timeChooser(hours) {
    const dropDowns = document.getElementsByClassName("dr-hoursChoices");
    if (dropDowns.length > 0) {
        const dropDown = dropDowns[0];
        dropDown.innerHTML = '';
        let initial = '';
        const createChoice = (time) => {
            let value = time;
            if (time >= 8) {
                return `<option value="${value}">${value}:00 AM</option>`;
            } else {
                return `<option value="${value}">${value}:00 PM</option>`;
            }
        };
        for (let i = 0; i < hours.length; i++) {
            initial += createChoice(hours[i]);
        }
        dropDown.innerHTML = initial;
    } else {
        console.error('No elements found with the class name "dr-hoursChoices".');
    }
}

function sendFullDate(event){
    resetClassName('dr-date-picker', 'dr-date-picker dr-date-active');
    const element = event.target.closest('td.dr-date-picker');
    const month = element.getAttribute('data-month');
    const day = element.getAttribute('data-day');
    const year = element.getAttribute('data-year');
    let preReturn = false;
    if (month == null || month == 'null'){
        preReturn = true;
    }
    if (element.className != "dr-date-picker"){
        preReturn = true;
    }
    if (preReturn) {return timeChooser([])}
    element.className = element == `${element.className} dr-date-active`? element.className : `${element.className} dr-date-active`;
    fetchAppointments(month, year, day, (data) => {timeChooser(getAvailableTime(data))});
    console.log(month, day, year);
}

function isDateLessThanCurrent(year, month, day) {
    const currentDate = new Date();
    const givenDate = new Date(year, month - 1, day);
    return givenDate < currentDate;
}

function preShowCalendar(month, year){
    fetchAppointments(month+1, year, "null", (data)=>{showCalendar(month, year, data)});
}

function showCalendar(month, year, monthData) {
    let firstDay = new Date(year, month, 1).getDay();
    tbl = document.getElementById("dr-calendar-body");
    tbl.innerHTML = "";
    monthAndYear.innerHTML = months[month] + " " + year;
    selectYear.value = year;
    selectMonth.value = month;
    console.log(monthData);

    const getFilledCount = (day, year) =>{
        let count = 0;
        for (i=0; i<monthData.length; i++){
            if (monthData[i].Appointment_Day == day && monthData[i].Appointment_Year == year){
                count = count + 1;
            }
        }
        return count;
    }

    const evaluateCount = () =>{
        if (getFilledCount(date, year)>8){
            cell.className = `${cell.className} dr-filled`;
            return true;
        }
        return false;
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
                cell.className = "dr-date-picker";
                cell.innerHTML = "<a>" + date + "</a>";
                cell.onclick = (event) => {sendFullDate(event)}

                if (j==6 || j==0 || evaluateCount()){
                    cell.setAttribute("data-day", null);
                    cell.setAttribute("data-month", null);
                    cell.setAttribute("data-year", null);
                    cell.setAttribute("data-month_name", months[month]);
                }
                else if(date === today.getDate() && year === today.getFullYear() && month === today.getMonth()) {
                    cell.setAttribute("data-day", null);
                    cell.setAttribute("data-month", null);
                    cell.setAttribute("data-year", null);
                    cell.setAttribute("data-month_name", months[month]);
                    cell.className = `${cell.className} dr-today`;
                } else {
                    cell.setAttribute("data-day", date);
                    cell.setAttribute("data-month", month + 1);
                    cell.setAttribute("data-year", year);
                    cell.setAttribute("data-month_name", months[month]);
                }
                if (isDateLessThanCurrent(year, month+1, date)){
                    cell.className = `${cell.className} dr-done`;
                }
                row.appendChild(cell);
                date++;
            }
        }
        tbl.appendChild(row);
    }
}

function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}