$('.projectCoverUpload').on("change", (e) => {
    console.log(e.target.files)
})


for (let item of document.querySelectorAll('.dropzone.dropzone-multiple')) {
    let key = item.dataset.key;
    item.dataset.dropzone = `{
            "url": "/admin/images/save",
            "params": {
                "csrfmiddlewaretoken": "${document.querySelector('input[name="csrfmiddlewaretoken"]').value}",
                "key": "${key}"
            }
        }`
}


$('.drop-image-a').on('click', () => {

})

function copy(item) {
    item.select()

    /* Copy the text inside the text field */
    document.execCommand("copy");

    console.log('copyed')
}

