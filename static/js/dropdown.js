document.querySelectorAll('.custom-dropdown').forEach(dropdown => {
    const selected = dropdown.querySelector('.selected-option');
    const text = dropdown.querySelector('.selection-text');
    const hiddenInput = dropdown.querySelector('.hidden-input');
    const options = dropdown.querySelectorAll('.dropdown-option');

    selected.addEventListener('click', (e) => {
        e.stopPropagation();
        document.querySelectorAll('.custom-dropdown').forEach(d => {
            if (d !== dropdown) d.classList.remove('active');
        });
        dropdown.classList.toggle('active');
    });

    options.forEach(option => {
        option.addEventListener('click', () => {
            text.textContent = option.textContent;
            hiddenInput.value = option.getAttribute('data-value');
            dropdown.classList.remove('active');
        });
    });
});

document.addEventListener('click', () => {
    document.querySelectorAll('.custom-dropdown').forEach(dropdown => {
        dropdown.classList.remove('active');
    });
});