document.addEventListener('DOMContentLoaded', function () {
    setTimeout(() => {
        const categorySelect = $('#id_category');  // Use jQuery to target Select2 element
        const subcategorySelect = document.querySelector('[name="subcategory"]');

        if (!categorySelect || !subcategorySelect) return;

        // Define the updateSubcategories function
        function updateSubcategories() {
            const categoryId = categorySelect.val();  // Get the selected category ID (using Select2 API)

            console.log('Category selected:', categoryId);  // Log the selected category ID

            if (!categoryId) return;  // Don't proceed if no category is selected

            // Make the API request to fetch subcategories based on the selected category ID
            fetch(`/api/get-subcategories/?category_id=${categoryId}`)
                .then(response => response.json())
                .then(data => {
                    console.log("API Response:", data);  // Log the API response

                    // Clear existing subcategory options
                    subcategorySelect.innerHTML = '';

                    // Add default option
                    const defaultOption = document.createElement('option');
                    defaultOption.value = '';
                    defaultOption.textContent = 'Select subcategory';
                    subcategorySelect.appendChild(defaultOption);

                    // Check if subcategories are available
                    if (data.subcategories && data.subcategories.length > 0) {
                        data.subcategories.forEach(sub => {
                            const option = document.createElement('option');
                            option.value = sub;  // Use the subcategory name as the value
                            option.textContent = sub;  // Use the subcategory name as the displayed text
                            subcategorySelect.appendChild(option);
                        });
                    } else {
                        const noSubOption = document.createElement('option');
                        noSubOption.value = '';
                        noSubOption.textContent = 'No subcategories available';
                        subcategorySelect.appendChild(noSubOption);
                    }

                    console.log('Subcategory dropdown updated:', subcategorySelect);  // Check if dropdown is updated
                })
                .catch(error => console.error('Error fetching subcategories:', error));
        }

        // Trigger the updateSubcategories function when the category changes (via Select2)
        categorySelect.on('change', function() {
            // Clear previous subcategory values when a new category is selected
            subcategorySelect.innerHTML = '';

            // Add default 'Select Subcategory' option to subcategory dropdown
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Loading subcategories...';
            subcategorySelect.appendChild(defaultOption);

            // Proceed to update subcategories based on selected category
            updateSubcategories();
        });

        // If a category is pre-selected on page load, run updateSubcategories to populate subcategories
        updateSubcategories();
    }, 100);  // Ensure the page has loaded before attaching the event
});
