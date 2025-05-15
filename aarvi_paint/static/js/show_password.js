document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.querySelector('input[name="password"]');

    if (passwordInput) {
        // Set the width of the password input
        passwordInput.style.width = "390px";
        passwordInput.style.paddingRight = "2.5rem"; // for icon spacing

        // Create wrapper for relative positioning
        const wrapper = document.createElement("div");
        wrapper.style.position = "relative";
        wrapper.style.display = "inline-block"; // ensure it fits properly

        // Insert wrapper before passwordInput
        passwordInput.parentNode.insertBefore(wrapper, passwordInput);
        wrapper.appendChild(passwordInput);

        // Create Font Awesome eye icon
        const toggleIcon = document.createElement("i");
        toggleIcon.className = "fa-solid fa-eye";
        toggleIcon.style.position = "absolute";
        toggleIcon.style.right = "10px";
        toggleIcon.style.top = "50%";
        toggleIcon.style.transform = "translateY(-50%)";
        toggleIcon.style.cursor = "pointer";
        toggleIcon.style.color = "#333";

        // Toggle password visibility
        toggleIcon.addEventListener("click", function () {
            const isPassword = passwordInput.type === "password";
            passwordInput.type = isPassword ? "text" : "password";
            toggleIcon.className = isPassword ? "fa-solid fa-eye-slash" : "fa-solid fa-eye";
        });

        // Append the icon to the wrapper
        wrapper.appendChild(toggleIcon);
    }
});
