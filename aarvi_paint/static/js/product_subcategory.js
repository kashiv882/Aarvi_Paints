document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.querySelector('#id_category');
    const subcategorySelect = document.querySelector('#id_subcategory');
 
    if (!categorySelect || !subcategorySelect) return;

    // Function to update subcategories based on selected category
    function updateSubcategories() {
        const categoryId = categorySelect.value;
        if (!categoryId) return;

        // Make an API call to fetch subcategories based on the selected category ID
        fetch(`/api/get-subcategories/?category_id=${categoryId}`)
            .then(response => response.json())
            .then(data => {
                // Clear existing options
                subcategorySelect.innerHTML = '';

                // Add the default 'Select subcategory' option
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = 'Select subcategory';
                subcategorySelect.appendChild(defaultOption);

                // Check if we got subcategories in the response
                if (data.subcategories && data.subcategories.length > 0) {
                    data.subcategories.forEach(sub => {
                        const option = document.createElement('option');
                        option.value = sub;
                        option.textContent = sub;
                        subcategorySelect.appendChild(option);
                    });
                } else {
                    // No subcategories found
                    const noSubOption = document.createElement('option');
                    noSubOption.value = '';
                    noSubOption.textContent = 'No subcategories available';
                    subcategorySelect.appendChild(noSubOption);
                }
            })
            .catch(error => console.error('Error fetching subcategories:', error));
    }

    // Listen for category change event
    categorySelect.addEventListener('change', updateSubcategories);

    // Trigger subcategory update immediately if a category is pre-selected on page load
    updateSubcategories();
});
