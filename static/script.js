$(document).ready(function() {
    // Initialize Select2 with custom placeholder
    $('#symptomsSelect').select2({
        placeholder: "Search and select symptoms...",
        allowClear: true,
        width: '100%'
    });

    // Handle form submission
    $('#predictionForm').on('submit', function(e) {
        e.preventDefault();
        
        // Get selected values
        const selectedSymptoms = $('#symptomsSelect').val();
        const age = $('#ageInput').val();
        const gender = $('#genderSelect').val();
        
        if (!selectedSymptoms || selectedSymptoms.length === 0) {
            showError("Please select at least one symptom.");
            return;
        }
        if (!age || !gender) {
            showError("Please provide both age and gender.");
            return;
        }

        // Hide previous results and errors
        $('#resultContainer').addClass('d-none');
        $('#errorContainer').addClass('d-none');
        
        // Show loading spinner, disable button
        const btn = $('#predictBtn');
        const spinner = $('#loadingSpinner');
        const btnText = $('.btn-text');
        
        btn.prop('disabled', true);
        spinner.removeClass('d-none');
        
        // Prepare data
        const data = {
            symptoms: selectedSymptoms,
            age: parseInt(age),
            gender: gender
        };

        // Make API call
        $.ajax({
            url: '/predict',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                if (response.success) {
                    showResult(response.prediction, response.precautions);
                } else {
                    showError(response.error || "An unknown error occurred.");
                }
            },
            error: function(xhr) {
                let errorMsg = "Failed to connect to the server.";
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                }
                showError(errorMsg);
            },
            complete: function() {
                // Restore button state
                btn.prop('disabled', false);
                spinner.addClass('d-none');
            }
        });
    });

    function showResult(diseaseName, precautionList) {
        // Format string (e.g. Fungal infection -> Fungal Infection)
        const formattedName = diseaseName.split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
            
        $('#predictedDiseaseName').text(formattedName);

        // Handle Precautions
        const precautionsCont = $('#precautionsContainer');
        const list = $('#precautionsList');
        list.empty();

        if (precautionList && precautionList.length > 0) {
            precautionList.forEach(item => {
                list.append(`<li class="list-group-item bg-transparent border-0 py-1 ps-0 text-dark"><i class="fa-solid fa-check-circle text-success me-2"></i>${item}</li>`);
            });
            precautionsCont.removeClass('d-none');
        } else {
            precautionsCont.addClass('d-none');
        }
        
        // Remove d-none and trigger reflow for animation
        const cont = $('#resultContainer');
        cont.removeClass('d-none');
        
        // Smooth scroll to result
        $('html, body').animate({
            scrollTop: cont.offset().top - 100
        }, 500);
    }

    function showError(message) {
        $('#errorMessage').text(message);
        $('#errorContainer').removeClass('d-none');
    }
});
