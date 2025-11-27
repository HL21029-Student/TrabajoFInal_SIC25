document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        errorMessage.textContent = '';

        const username = loginForm.username.value;
        const password = loginForm.password.value;

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                window.location.href = '/'; // Redirigir a la página principal
            } else {
                const data = await response.json();
                errorMessage.textContent = data.error || 'Error desconocido al iniciar sesión.';
            }
        } catch (error) {
            console.error('Error de red:', error);
            errorMessage.textContent = 'No se pudo conectar al servidor. Inténtelo más tarde.';
        }
    });
});