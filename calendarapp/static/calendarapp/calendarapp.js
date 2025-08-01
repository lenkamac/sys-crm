document.addEventListener('DOMContentLoaded', function() {

    // === Add flatpickr initialization at the start of this function ===
    flatpickr("#eventStart", {
        enableTime: true,
        dateFormat: "Y-m-d\\TH:i",
        time_24hr: true
    });
    flatpickr("#eventEnd", {
        enableTime: true,
        dateFormat: "Y-m-d\\TH:i",
        time_24hr: true
    });
    flatpickr("#editEventStart", {
        enableTime: true,
        dateFormat: "Y-m-d\\TH:i",
        time_24hr: true
    });
    flatpickr("#editEventEnd", {
        enableTime: true,
        dateFormat: "Y-m-d\\TH:i",
        time_24hr: true
    });


    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: calendarEventsUrl,  // We'll define this in template!
        eventTimeFormat: {  // uppercase H for 24h, lowercase i for minutes
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        },
        // === Add this below your eventClick ===
        dateClick: function(info) {
            // Clear previous form values
            document.getElementById('addEventForm').reset();

            // Pre-fill the "Start" field with clicked date
            // Convert date to "YYYY-MM-DDTHH:MM" format
            // If using dayGrid, time is 00:00
            const dateStr = info.dateStr.length > 10 ? info.dateStr : info.dateStr + 'T00:00';
            document.getElementById('eventStart').value = dateStr;

            // Optionally, also pre-fill "End" field (e.g., 1 hour after start)
            document.getElementById('eventEnd').value = "";

            // Show the add event modal
            var addModal = new bootstrap.Modal(document.getElementById('addEventModal'));
            addModal.show();
        },

        eventClick: function(info) {
            // Store event id and title in the modal for easy access
            document.getElementById('eventActionEventId').value = info.event.id;
            document.getElementById('eventActionModalTitle').textContent = info.event.title;
            document.getElementById('detailEventBtn').onclick = function() {
            // Fill in the details modal with the event's data
            document.getElementById('detailEventTitle').textContent = info.event.title || '';
            document.getElementById('detailEventStart').textContent = info.event.start ? formatDateDisplay(info.event.start) : '';
            document.getElementById('detailEventEnd').textContent = info.event.end ? formatDateDisplay(info.event.end) : 'No end';
            document.getElementById('detailEventDesc').textContent = info.event.extendedProps.description || '';

            actionModal.hide();
            var detailModal = new bootstrap.Modal(document.getElementById('eventDetailModal'));
            detailModal.show();
        };


            // Open action modal
            var actionModal = new bootstrap.Modal(document.getElementById('eventActionModal'));
            actionModal.show();

            // Remove any old listeners to avoid stacking
            document.getElementById('editEventBtn').onclick = function() {
                actionModal.hide();
                // Prefill and show the edit modal
                document.getElementById('editEventId').value = info.event.id;
                document.getElementById('editEventTitle').value = info.event.title;
                document.getElementById('editEventStart').value = toDatetimeLocal(info.event.start);
                document.getElementById('editEventEnd').value = info.event.end ? toDatetimeLocal(info.event.end) : '';
                document.getElementById('editEventDesc').value = info.event.extendedProps.description || "";
                var editModal = new bootstrap.Modal(document.getElementById('editEventModal'));
                editModal.show();
            };

            document.getElementById('deleteEventBtn').onclick = function() {
                actionModal.hide();
                if (confirm('Are you sure you want to delete this event?')) {
                    fetch(`delete_event/${info.event.id}/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            info.event.remove();
                            alert('Event deleted.');
                            refreshUpcomingEvents();
                        } else {
                            alert('Failed to delete event.');
                        }
                    })
                    .catch(() => alert('Error deleting event.'));
                }
            };
        },
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek, multiMonthYear',
        }
    });
    calendar.render();


    // Add-event form handler
    document.getElementById('addEventForm').addEventListener('submit', function(e) {
        e.preventDefault();

        // Gather form data
        var formData = {
            title: document.getElementById('eventTitle').value,
            start: localToUTC(document.getElementById('eventStart').value),
            end: localToUTC(document.getElementById('eventEnd').value),
            description: document.getElementById('eventDesc').value,
        };

        fetch('add_event/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network error.');
        })
        .then(data => {
            if (data.success) {
                // Optionally refresh the calendar:
                calendar.refetchEvents();
                refreshUpcomingEvents();
                // Hide modal
                var addEventModal = document.getElementById('addEventModal');
                var modalInstance = bootstrap.Modal.getInstance(addEventModal);
                modalInstance.hide();
                // Optionally clear form
                e.target.reset();
            } else {
                alert('Failed to add event.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding event');
        });
    });


    // Handle edit form submit
    document.getElementById('editEventForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const eventId = document.getElementById('editEventId').value;
        const data = {
            title: document.getElementById('editEventTitle').value,
            start: localToUTC(document.getElementById('editEventStart').value),
            end: localToUTC(document.getElementById('editEventEnd').value),
            description: document.getElementById('editEventDesc').value,
        };

        fetch(`update_event/${eventId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                calendar.refetchEvents();
                refreshUpcomingEvents();
                bootstrap.Modal.getInstance(document.getElementById('editEventModal')).hide();
            } else {
                alert('Failed to update event');
            }
        });
    });

    // Drag & Drop/resize logic
    function updateEvent(info) {
        fetch(`update_event/${info.event.id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                title: info.event.title,
                start: info.event.start.toISOString(),
                end: info.event.end ? info.event.end.toISOString() : null,
                description: info.event.extendedProps.description
            })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert('Failed to update event');
                info.revert(); // Revert to original position
            }
        });
    }


});

function toDatetimeLocal(date) {
    if (!date) return '';
    const d = (date instanceof Date) ? date : new Date(date);
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    return d.toISOString().slice(0,16);
}


// format for date and time
function formatDateDisplay(dateString) {
    const d = new Date(dateString);
    const pad = n => n < 10 ? '0' + n : n;
    return `${pad(d.getDate())}/${pad(d.getMonth() + 1)}/${d.getFullYear()} ` +
           `${pad(d.getHours())}:${pad(d.getMinutes())}`;
}


function localToUTC(dateLocalString) {
    if (!dateLocalString) return null; // Return null for blank inputs (e.g., end date)
    const local = new Date(dateLocalString);
    if (isNaN(local)) return null;     // Also cover any invalid date
    return local.toISOString();
}

// Helper to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// upcomming events
document.addEventListener('DOMContentLoaded', function () {
    loadUpcomingEvents();
    fetch(calendarEventsUrl)
        .then(response => response.json())
        .then(function(events) {
            const now = new Date();
            // Sort upcoming events by start (asc)
            const upcoming = events
                .filter(ev => new Date(ev.start) >= now)
                .sort((a, b) => new Date(a.start) - new Date(b.start))
                .slice(0, 5); // Only show next 5 by default. Adjust if needed

            const ul = document.getElementById('upcoming-events-list');
            ul.innerHTML = ""; // Clear old contents

            upcoming.forEach(event => {
                const li = document.createElement('li');
                li.classList.add('list-group-item');

                // Add end time if available. You can change format as needed
                let display = `<strong>${event.title}</strong><br>
                    <small>Start: ${formatDateDisplay(event.start)}</small><br>`;
                if (event.end) {
                    display += `<br><small>End: ${formatDateDisplay(event.end)}</small>`;
                }
                // Add the description under the date section, if it exists
                if (event.description) {
                    display += `<br><small class="text-muted">${event.description}</small>`;
                }

                li.innerHTML = display;
                ul.appendChild(li);
            });

            if (upcoming.length === 0) {
                ul.innerHTML = '<li class="list-group-item">No upcoming events!</li>';
            }
        });
});

let currentPage = 1;

function loadUpcomingEvents(page=1) {
    fetch(`upcoming_events/?page=${page}`)
        .then(response => response.json())
        .then(data => {
            const ul = document.getElementById('upcoming-events-list');
            ul.innerHTML = '';
            data.events.forEach(event => {
                const li = document.createElement('li');
                li.classList.add('list-group-item');
                let display = `<strong>${event.title}</strong><br>
                    <span>Start: ${formatDateDisplay(event.start)}</span>`;
                if (event.end) {
                    display += `<br><span>End: ${formatDateDisplay(event.end)}</span>`;
                }
                if (event.description) {
                    display += `<br><small class="text-muted">${event.description}</small>`;
                }
                li.innerHTML = display;
                ul.appendChild(li);
            });

            // Pagination controls
            const paginationDiv = document.getElementById('upcoming-pagination');
            paginationDiv.innerHTML = '';
            if (data.has_prev) {
                const prevBtn = document.createElement('button');
                prevBtn.className = 'btn btn-secondary btn-sm me-2';
                prevBtn.textContent = 'Previous';
                prevBtn.onclick = () => {
                    loadUpcomingEvents(data.page - 1);
                };
                paginationDiv.appendChild(prevBtn);
            }
            if (data.has_next) {
                const nextBtn = document.createElement('button');
                nextBtn.className = 'btn btn-secondary btn-sm';
                nextBtn.textContent = 'Next';
                nextBtn.onclick = () => {
                    loadUpcomingEvents(data.page + 1);
                };
                paginationDiv.appendChild(nextBtn);
            }
            currentPage = data.page;
        });
}

function refreshUpcomingEvents() {
    loadUpcomingEvents(1); // Always load first page, or pass desired page
}


