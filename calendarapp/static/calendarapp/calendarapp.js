document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: calendarEventsUrl,  // We'll define this in template!
        eventClick: function(info) {
            if (confirm('Delete this event?')) {
                fetch(`delete_event/${info.event.id}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        info.event.remove(); // Remove from calendar
                    } else {
                        alert('Failed to delete event.');
                    }
                })
                .catch(() => alert('Error deleting event.'));
            }
        }
,
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








