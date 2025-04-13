document.addEventListener('DOMContentLoaded', function () {
    const selectAllCheckbox = document.getElementById('select-all'); // Master checkbox
    const rowCheckboxes = document.querySelectorAll('.row-checkbox'); // All row checkboxes

    // Toggle all row checkboxes when the master checkbox is clicked
    selectAllCheckbox.addEventListener('change', function () {
        const isChecked = selectAllCheckbox.checked;
        rowCheckboxes.forEach((checkbox) => {
            checkbox.checked = isChecked;
        });
    });

    // Uncheck the master checkbox if any row checkbox is unchecked
    rowCheckboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', function () {
            if (!checkbox.checked) {
                selectAllCheckbox.checked = false;
            }
        });
    });

    // Check the master checkbox if all row checkboxes are checked
    rowCheckboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', function () {
            const allChecked = Array.from(rowCheckboxes).every((cb) => cb.checked);
            if (allChecked) {
                selectAllCheckbox.checked = true;
            }
        });
    });
});

document.getElementById('select-all').addEventListener('change', function(e) {
            const checkboxes = document.querySelectorAll('.lead-checkbox');
            checkboxes.forEach(function(checkbox) {
                checkbox.checked = e.target.checked;
            });
        });
