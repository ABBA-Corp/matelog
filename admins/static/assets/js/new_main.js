function submit_form(id) {
    console.log(id)
    let form = $(`#${id}`)
    let url = form.attr("action")
    let data = $(`#${id} :input`).serialize()

    $.ajax({
        url: url,
        data: data,
        type: 'POST',
        success: () => {
            $(form).parent().remove()
        }
    })

}

function form_submit_in_table(id) {
    console.log(id)
    let form = $(`#${id}`)
    let url = form.attr("action")
    let data = $(`#${id} :input`).serialize()

    $.ajax({
        url: url,
        data: data,
        type: 'POST',
        success: () => {
            $(form).parent().parent().parent().remove()
        }
    })
}

function copy(that) {
    var inp = document.createElement('input');
    document.body.appendChild(inp)
    inp.value = that.textContent
    inp.select();
    document.execCommand('copy', false);
    inp.remove();

    $.notify.addStyle('foo', {
        html:
            "<div>" +
            "<div class='clearfix'>" +
            "<div class='title' data-notify-html='title'/>" +
            "<div class='buttons'>" +
            "<button class='no'>Cancel</button>" +
            "<button class='yes' data-notify-text='button'></button>" +
            "</div>" +
            "</div>" +
            "</div>"
    });


    $.notify({
        title: 'Success'
    }, {
        style: 'foo',
        clickToHide: false,
        autoHide: false,
    });
}



$('.dropzone').each((i, e) => {
    Dropzone.options.myAwesomeDropzone = false;
    Dropzone.autoDiscover = false;
    var myDropzone = new Dropzone(e, {
        url: $(e).attr("data-url"),
        parallelUploads: 1,
        maxFiles: $('.dropzone').attr('data-max'),
        params: {
            "csrfmiddlewaretoken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "key": $(e).attr('data-key'),
            'id': $('input[name="id"]').val(),
            'url': window.location.href
        },
        previewsContainer: `#${$(e).find('.dz-preview-container').attr('id')}`,
        success: (file, response) => {
            var removeButton = Dropzone.createElement(`<a class="dz-remove" data-dz-remove>Удалить</a>`);
            removeButton.addEventListener("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                myDropzone.removeFile(file);

                data = {}
                data["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val()
                data['key'] = $('input[name="dropzone-key"]').val()
                data['file'] = response

                $.ajax({
                    url: $(e).attr('data-delete'),
                    type: 'POST',
                    data: data,
                    success: () => {
                        console.log('success')
                    },
                    error: () => {
                        console.log('error')
                    }

                })

            });
            file.previewElement.appendChild(removeButton);
        }
    });


})
