$(document).ready(function() {
    $('.edit-btn').on('click', function() {
        // Get data attributes from the button
        var id = $(this).attr('data-id');
        var name = $(this).attr('data-name');
        var type = $(this).attr('data-type');
        var url = $(this).attr('data-url');
        var description = $(this).attr('data-description');
        
        // Populate the form fields
        $('#edit-id').val(id);
        $('#edit-name').val(name);
        $('#edit-type').val(type);
        $('#edit-url').val(url);
        $('#edit-description').val(description);
        
    });
});

function confirmDelete(id, type) {
    var confirmAction = confirm('Confirm to delete!');
    if (confirmAction) {
        window.location.href = '/delete?id=' + id + '&type=' + type;
    } else {
        // If the user clicks "cancel", do nothing
        console.log('Deletion canceled');
    }
}

$(".video_play").click(function(){
    var videoId = $(this).attr('data-id');
    window.location.href = window.location.origin + "/video-play?id=" + videoId;
});