$(document).ready(function () {
    // Previsualización de la imagen
    $('#imageUpload').change(function () {
        readURL(this);
    });

    // Predicción
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Mostrar loader y ocultar botón de predicción
        $(this).hide();
        $('.loader').show();

        // Hacer la predicción
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Ocultar loader y mostrar resultado
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result span').html(data);

                // Permitir cargar una nueva imagen
                $('#btn-predict').show();
                $('#imageUpload').val('');
            },
            error: function (error) {
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result span').html('Error en la predicción. Intente nuevamente.');
                $('#btn-predict').show();
                $('#imageUpload').val('');
            }
        });
    });
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
            $('#imagePreview').hide();
            $('#imagePreview').fadeIn(650);
            $('.image-section').show();
            $('#result').hide();
            $('#result span').html('');
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function scrollToSection(sectionId) {
    var section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: "smooth", block: "start" });
    }
}

// Función para desplazarse suavemente al inicio de la página
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Función para desplazarse suavemente a una sección específica
function scrollToSection(sectionId) {
    var section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}
