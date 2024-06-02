

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
            h4Tag.text(Object.values(selectedAmenities).join(', '));
        });

        console.log(selectedAmenities);

        $.ajax({
            type: 'GET',
            url: "http://0.0.0.0:5001/api/v1/status/",
            data: {
                format: 'json'
            },
            error: () => {
                console.error('error while fetching the data');
            },
            success: function (data) {
                console.log(data.status);
                if (data.status === "OK") {
                    $('#api_status').addClass('available');
                }
                else {
                    $('#api_status').removeClass('available');
                }
            }
        });

        $('button').click(() => {
            $.ajax({
                url: "http://0.0.0.0:5001/api/v1/places_search/",
                type: 'POST',
                contentType: "application/json",
                data: JSON.stringify({ 'amenities': Object.keys(selectedAmenities) }),
                error: () => {
                    console.error('error while fetching the data');
                },

                success: function (data) {
                    let html = undefined;
                    var first_name = undefined;
                    var last_name = undefined;
                    console.log(data)
                    for (place of data) {

                        html = '<article>' + '<div class="title_box">' +
                            "<h2>" + place.name + "</h2>" +
                            '<div class="price_by_night">$' +
                            place.price_by_night +
                            '</div>' +
                            '</div>' +
                            '<div class="information">' + '<div class="max_guest">' +
                            place.max_guest + 'Guest' +
                            '</div>' + '<div class="number_rooms">' +
                            place.number_rooms + 'Bedroom' +
                            '</div>' + '<div class="number_bathrooms">' +
                            place.number_bathrooms + 'Bathroom' +
                            '</div >' + '</div >' +
                            '<div class="user">' +
                            '</div >' +
                            '<div class="description">' +
                            place.description +
                            '</div>' +
                            '</article >';

                        $('.places').append(html);

                        // Use a specific selector within the current article to append user information
                        const userContainer = $('.places article:last-child .user');

                        $.get("http://0.0.0.0:5001/api/v1/users/" + place.user_id, (data) => {
                            userContainer.append('<b>Owner:</b>' + data.first_name + " " + data.last_name);
                        });
                    }
                }
            });
        });
    });
});

