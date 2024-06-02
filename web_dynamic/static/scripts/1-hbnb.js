

document.addEventListener("DOMContentLoaded", () => {
    $(document).ready(function () {
        const selectedAmenities = {}; // Use an object to store the selected amenities

        $('input[type="checkbox"]').on('change', function () {
            const amenityId = $(this).data('id');
            const amenityName = $(this).data('name');

            if (this.checked) {
                selectedAmenities[amenityId] = amenityName; // Add to the selected amenities
            } else {
                delete selectedAmenities[amenityId]; // Remove from the selected amenities
            }

            // Update the h4 tag with the list of selected amenities
            const h4Tag = $('.amenities h4');
            // h4Tag.text(Object.values(selectedAmenities).join(', '));
            h4Tag.text(selectedAmenities.join(', '));
        });
    });
});
