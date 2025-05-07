document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.querySelector('[name="category"]');
    const subcategorySelect = document.querySelector('[name="subcategory"]');

    if (!categorySelect || !subcategorySelect) {
        console.warn("Category or subcategory field not found.");
        return;
    }

    function fetchSubcategories(categoryId, selectedValue = '') {
        if (!categoryId) return;

        fetch(`/api/get-subcategories/?category_id=${categoryId}`)
            .then(response => response.json())
            .then(data => {
                const subcategories = data.subcategories || [];

                // Clear the current options
                subcategorySelect.innerHTML = '';

                if (subcategories.length === 0) {
                    const option = document.createElement('option');
                    option.value = '';
                    option.textContent = 'No subcategories available';
                    subcategorySelect.appendChild(option);
                } else {
                    const defaultOption = document.createElement('option');
                    defaultOption.value = '';
                    defaultOption.textContent = 'Select a subcategory';
                    subcategorySelect.appendChild(defaultOption);

                    subcategories.forEach(sub => {
                        const option = document.createElement('option');
                        option.value = sub;
                        option.textContent = sub;
                        if (sub === selectedValue) {
                            option.selected = true;
                        }
                        subcategorySelect.appendChild(option);
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching subcategories:', error);
            });
    }

    // Initial load: trigger if a category is already selected
    if (categorySelect.value) {
        fetchSubcategories(categorySelect.value, subcategorySelect.value);
    }

    // When user changes the category
    categorySelect.addEventListener('change', function () {
        fetchSubcategories(this.value);
    });
});
