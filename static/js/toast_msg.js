document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let toasts = document.querySelectorAll('.custom-toast');
        toasts.forEach(function (toast) {
            toast.style.opacity = '0'; // Fade out
            toast.style.transform = 'translateX(120%)'; 
            setTimeout(() => toast.remove(), 400); 
        });
    }, 2000); 
});
