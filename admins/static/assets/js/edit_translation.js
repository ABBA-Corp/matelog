$(document).on('click', '#add_item', () => {
    let new_id = Number($(".translation-id").last().html()) + 1
    console.log(new_id, $(".translation-id"))
    $('[name="item_count"]').val(new_id)
    $('#for_new_items').find('.translation-id').html(new_id)
    $('#for_new_items').find('.translate-key-inp').attr('name', `key[${new_id}]`)
    $('#for_new_items').find('.lang-val').each((i, e) => {
        let lang = $(e).attr('data-lang')
        $(e).attr('name', `value[${new_id}][${lang}]`)
    })

    let newItemHtml = $('#for_new_items').html()
    

    //$('#translations-list').html(
     //   $('#translations-list').html() + newItemHtml
    //)
    document.getElementById("translations-list").insertAdjacentHTML('beforeend', newItemHtml)
})


