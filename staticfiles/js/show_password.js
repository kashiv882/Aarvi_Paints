document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.querySelector('input[name="password"]');

    if (passwordInput) {
        // Create wrapper div for relative positioning
        const wrapper = document.createElement("div");
        wrapper.style.position = "relative";

        // Insert wrapper before passwordInput
        passwordInput.parentNode.insertBefore(wrapper, passwordInput);
        wrapper.appendChild(passwordInput);

        // Create the eye toggle icon
        const toggleIcon = document.createElement("span");
        toggleIcon.innerHTML = "👁️";
        toggleIcon.style.position = "absolute";
        toggleIcon.style.right = "10px";
        toggleIcon.style.top = "50%";
        toggleIcon.style.transform = "translateY(-50%)";
        toggleIcon.style.cursor = "pointer";

        // Toggle password visibility
        toggleIcon.addEventListener("click", function () {
            const isPassword = passwordInput.type === "password";
            passwordInput.type = isPassword ? "text" : "password";
        });

        // Append the icon
        wrapper.appendChild(toggleIcon);
    }
});
