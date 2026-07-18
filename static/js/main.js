// Custom JS untuk Portofolio Flask

document.addEventListener('DOMContentLoaded', function () {
    // Otomatis tutup notifikasi flash message setelah 4 detik
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            var closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 4000);
    });
});
