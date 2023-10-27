document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#add-item-form');

    form.addEventListener('submit', function (event) {
        const nameInput = document.querySelector('input[name="item_name"]');
        const priceInput = document.querySelector('input[name="item_price"]');
        const quantityInput = document.querySelector('input[name="item_quantity"]');
        const nameValue = nameInput.value.trim();
        const priceValue = priceInput.value.trim();
        const quantityValue = quantityInput.value.trim();

        if (!nameValue || !priceValue || !quantityValue) {
            event.preventDefault();
            alert('Please fill in all fields.');
        }
    });

    const markSoldButtons = document.querySelectorAll('.mark-sold-button');

    markSoldButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            if (!confirm('Mark this item as sold?')) {
                event.preventDefault();
            }
        });
    });
});
