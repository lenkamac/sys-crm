document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: calendarEventsUrl,  // We'll define this in template!
        eventClick: function(info) {
                // You can use a prompt, a custom modal, or whatever suits your UI
                const action = prompt("Type 'edit' to edit, 'delete' to delete this event, or Cancel to abort.", "edit");

                if (action === "delete") {
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
                } else if (action === "edit") {
                    // Fill the edit modal with event data
                    document.getElementById('editEventId').value = info.event.id;
                    document.getElementById('editEventTitle').value = info.event.title;
                    document.getElementById('editEventStart').value = info.event.start.toISOString().slice(0, 16);
                    document.getElementById('editEventEnd').value = info.event.end ? info.event.end.toISOString().slice(0, 16) : '';
                    document.getElementById('editEventDesc').value = info.event.extendedProps.description || "";
                    var editModal = new bootstrap.Modal(document.getElementById('editEventModal'));
                    editModal.show();
                }
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
            start: document.getElementById('eventStart').value,
            end: document.getElementById('eventEnd').value,
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
            start: document.getElementById('editEventStart').value,
            end: document.getElementById('editEventEnd').value,
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
            // Get current date/time
            const now = new Date();
            // Filter for events after now, and sort by start
            const upcoming = events
                .filter(e => new Date(e.start) > now)
                .sort((a, b) => new Date(a.start) - new Date(b.start))
                .slice(0, 5); // Show next 5, adjust as needed

            const list = document.getElementById('upcoming-events-list');
            list.innerHTML = ''; // Clear existing

            if (upcoming.length === 0) {
                const li = document.createElement('li');
                li.textContent = "No upcoming events";
                li.className = "list-group-item";
                list.appendChild(li);
                return;
            }
            upcoming.forEach(e => {
                const li = document.createElement('li');
                li.className = "list-group-item";
                li.innerHTML = `<strong>${e.title}</strong><br>
                    <small>${new Date(e.start).toLocaleString()}</small>
                    ${e.description ? '<br>'+e.description : ''}`;
                list.appendChild(li);
            });
        });
});









