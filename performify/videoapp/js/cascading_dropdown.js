document.addEventListener('DOMContentLoaded', function () {
    const mainCategorySelect = document.getElementById('main_category');
    const subCategorySelect = document.getElementById('sub_category');
    const tagsContainer = document.getElementById('tags_container');

    mainCategorySelect.addEventListener('change', function () {
        fetch(`/get_subcategories/?category_id=${this.value}`)
            .then(response => response.json())
            .then(data => {
                subCategorySelect.innerHTML = '<option value="">Select SubCategory</option>';
                data.subcategories.forEach(subCat => {
                    subCategorySelect.innerHTML += `<option value="${subCat.id}">${subCat.name}</option>`;
                });
                tagsContainer.innerHTML = '';  // Clear tags when main category changes
            });
    });

    subCategorySelect.addEventListener('change', function () {
        fetch(`/get_tags/?subcategory_id=${this.value}`)
            .then(response => response.json())
            .then(data => {
                tagsContainer.innerHTML = '';
                data.tags.forEach(tag => {
                    tagsContainer.innerHTML += `<div>
                        <input type="checkbox" name="tags" value="${tag.name}" id="tag_${tag.id}">
                        <label for="tag_${tag.id}">${tag.name}</label>
                    </div>`;
                });
            });
    });
});
