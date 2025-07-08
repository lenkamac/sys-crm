document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: calendarEventsUrl,  // We'll define this in template!
        eventClick: function(info) {
            // Store event id and title in the modal for easy access
            document.getElementById('eventActionEventId').value = info.event.id;
            document.getElementById('eventActionModalTitle').textContent = info.event.title;

            // Open action modal
            var actionModal = new bootstrap.Modal(document.getElementById('eventActionModal'));
            actionModal.show();

            // Remove any old listeners to avoid stacking
            document.getElementById('editEventBtn').onclick = function() {
                actionModal.hide();
                // Prefill and show the edit modal
                document.getElementById('editEventId').value = info.event.id;
                document.getElementById('editEventTitle').value = info.event.title;
                document.getElementById('editEventStart').value = info.event.start.toISOString().slice(0, 16);
                document.getElementById('editEventEnd').value = info.event.end ? info.event.end.toISOString().slice(0, 16) : '';
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

function localToUTC(dateLocalString) {
    if (!dateLocalString) return null; // Return null for blank inputs (e.g., end date)
    const local = new Date(dateLocalString);
    if (isNaN(local)) return null;     // Also cover any invalid date
    return local.toISOString();
}

function formatDateDisplay(dtString) {
    if (!dtString) return "";
    const dateObj = new Date(dtString);
    // Show local string, or you can adjust the format as needed
    return dateObj.toLocaleString();
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








