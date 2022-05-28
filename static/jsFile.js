
/*
*
*
*
*
*
*
*
*
*
*
*
* ************* get words***************** */
var word = [];
$(document).ready(function () {
    $.get("http://localhost:8000/dictWord", function (d) {
        word = (d + "").split("*%*");
    });
});

/*
*
*
*
*
*
*
*
*
*
*
*
* ************** single word selected selected**************** */
let aaa = -1;
$(".transslatWord").on("mouseover", function () {
    if (window.getSelection().toString().length > 1) {
        aaa *= -1;
        if (aaa != -1) {
            $(
                "<iframe src=" +
                `https://targoman.ir/#${window.getSelection().toString()}` +
                ' frameborder="0" width="100%" height="100%"  id="transslatWordd"></iframe>'
            ).prependTo("body");
        } else {
            $("#transslatWordd").remove();
            $(".transslatWord").html("close transslat a word ")
        }

    }
});

/*
*
*
*
*
*
*
*
*
*
*
*
* ************** translate with google teranslate text**************** */
$(".transslattext").on("click", function () {
    if (window.getSelection().toString().length > 1) {
        $.post(
            "http://localhost:8000/urlgoogleteanslate",
            { data: window.getSelection().toString() },
            function (d) {
                window.open(d, '_blank');
            }
        );
    }
});
// let bbb = -1;
// $(".transslattext").on("mouseover", function () {
//     if (window.getSelection().toString().length > 1) {
//         bbb *= -1;
//         if (bbb != -1) {
//             $.post(
//                 "http://localhost:8000/urlgoogleteanslate",
//                 { data: window.getSelection().toString() },
//                 function (d) {
//                     // $(
//                     //     "<iframe src=" +
//                     //     `${d}` +
//                     //     ' frameborder="0" width="100%" height="100%" name="transslattextttttt" id="transslattextt"></iframe>'
//                     // ).prependTo("body");
//                     window.open(d, '_blank');
//                 }
//             );
//         } else {
//             $("#transslattextt").remove();
//         }
//     }
// });

/*
*
*
*
*
*
*
*
*
*
*
*
* ************** clear textarea **************** */
function claerTExtt() {
    let arr = $("#textarea")
        .val()
        .split(/\r?\n|\r/);

    let temp = "";

    arr.forEach((element) => {
        temp += element + " ";
    });

    arr = temp.split(/\.|\. /);

    temp = "";

    arr.forEach((element, index) => {
        index != arr.length - 1
            ? (temp += element.trim() + ".\n")
            : (arr[index] = null);
    });

    $("#textarea").val(temp);
}
$(".copyText").click(function () {
    claerTExtt();
});

/*
*
*
*
*
*
*
*
*
*
*
*
************** get translate ***************** */
$(".submit-bttn").click(function () {
    // sure submit-bttn is hide when subnited
    $(".submit-bttn").hide();

    // words I know
    $(".Wordss").html("");
    word.forEach((e) => {
        if (($("#textarea").val()).search(` ${e} `) != -1) {
            if (e.length >= 1) {
                $(".Wordss").append(
                    `<span class='${e} Wordsssssss'> ${e} </span>-`
                );
            }
        }
    });
    

    // end textarea have dot ?
    var leee = $("#textarea").val();
    for (let index = leee.length - 1; index >= leee.length - 5; index--) {
        leee[index].replace("\n", "");
    }
    if (
        leee[leee.length - 1].search(/\./) == -1 &&
        leee[leee.length - 1].search(/\n/) == -1
    ) {
        $("#textarea").val(leee + ".");
    }

    claerTExtt();

    $.post(
        "http://localhost:8000/translate/google",
        { data: $("#textarea").val() },
        function (d) {
            $(".submit-bttn").show();
            $("#result_google").text("");
            $("#result_google").html("");
            $("#result_google").html(d);
        }
    );

    $.post(
        "http://localhost:8000/translate/tarjome",
        { data: $("#textarea").val() },
        function (d) {
            $(".submit-bttn").show();
            $("#result_tarjome").text("");
            $("#result_tarjome").html("");
            $("#result_tarjome").html(d);
        }
    );
});



/*
*
*
*
*
*
*
*
*
*
*
*
* ************* show translate words that i know it ***************** */
var mouseX, mouseY;
$(document).mousemove(function (e) {
    mouseX = e.pageX;
    mouseY = e.pageY;
}).mouseover();
var tempppp;

$("body").on("mouseover", "span.Wordsssssss", function () {
    $.post(
        // "http://localhost:8000/wordsIKnow/readAll",
        // "http://localhost:8000/wordsIKnow/delete",
        // "http://localhost:8000/wordsIKnow/update",
        // "http://localhost:8000/wordsIKnow/create",
        "http://localhost:8000/wordsIKnow/read",
        { data: ($(this).text()).trim() },
        async function (d) {
            tempppp = await d;
            tempppp = JSON.parse(tempppp)
            res = `
            index_ = ${tempppp.index_} \n</br>
            en = ${tempppp.en} \n</br>
            fa = ${tempppp.fa} \n</br>
            pronunciation = ${tempppp.pronunciation} \n</br>
            example = ${tempppp.example} \n</br>
            words_category = ${tempppp.words_category} \n</br>
            description = ${tempppp.description} \n</br>
            is_deleted = ${tempppp.is_deleted}</br>`
            $("#draggable #tabs-1").html(res);
        }
    );

    $('.wordAlert').css("display", "block")
    $('.wordAlert').css("top", mouseY)
    $('.wordAlert').css("left", mouseX)
    // $(".tabs").tabs();
    $("#draggable").draggable();
});


$("body").on("mouseout", "span.Wordsssssss", function () {
    $('.wordAlert').css("display", "none")
});



// $("body").on("click", ".tabs-2_link", function () {
//     $("._edit_index_").val(tempppp.index_)
//     $("._edit_en").val(tempppp.en)
//     $("._edit_fa").val(tempppp.fa)
//     $("._edit_pronunciation").val(tempppp.pronunciation)
//     $("._edit_example").val(tempppp.example)
//     $("._edit_words_category").val(tempppp.words_category)
//     $("._edit_description").val(tempppp.description)
//     $("._edit_is_deleted").val(tempppp.is_deleted)

//     $("body").on("click", ".edit_donee", function () {
//         $.post(
//             "http://localhost:8000/wordsIKnow/update",
//             {
//                 data:
//                     JSON.stringify(
//                         {
//                             index_: ($("._edit_index_").val()).trim(),
//                             en: ($("._edit_en").val()).trim(),
//                             fa: ($("._edit_fa").val()).trim(),
//                             pronunciation: ($("._edit_pronunciation").val()).trim(),
//                             example: ($("._edit_example").val()).trim(),
//                             words_category: ($("._edit_words_category").val()).trim(),
//                             description: ($("._edit_description").val()).trim(),
//                             is_deleted: ($("._edit_is_deleted").val()).trim()
//                         }
//                     )
//             },
//             async function (d) {
//                 res = await d;
//                 console.log(d);
//                 $("._edit_index_").val(res.index_)
//                 $("._edit_en").val(res.en)
//                 $("._edit_fa").val(res.fa)
//                 $("._edit_pronunciation").val(res.pronunciation)
//                 $("._edit_example").val(res.example)
//                 $("._edit_words_category").val(res.words_category)
//                 $("._edit_description").val(res.description)
//                 $("._edit_is_deleted").val(res.is_deleted)
//             }
//         );
//     });

// });





/*
*
*
*
*
*
*
*
*
*
*
*
* *************  close ***************** */
$("body").on("click", ".enddddd", function () {
    $.get(
        "http://localhost:8000/closeDrive",
        function (d) {
            alert(d)
        }
    );
});



/*
*
*
*
*
*
*
*
*
*
*
*
* *************  texat area length ***************** */
// $("body").on("focusout", "#textarea", function () {
//     $(".lentextare").html(($("#textarea").val()).length)
// });
setInterval(() => {
    $(".lentextare").html(($("#textarea").val()).length)
}, 50);



/*
*
*
*
*
*
*
*
*
*
*
*
* *************  site translate  ***************** */
$("body").on("click", ".siteeeeeeeeeeeee_radio", function () {
    var urll = prompt();
    if ($(".siteeeeeeeeeeeee_radio").prop("checked") == true && (urll != null || urll != undefined)) {
        $('#pdfffffffffffff').css("visibility", "hidden")
        $('#pdfffffffffffff').css("height", "0")
        $('#siteeeeeeeeeeeee').css("height", "540px")
        $(
            "<iframe src=" +
            `${urll}` +
            ' frameborder="0" width="100%" height="100%"  id="siteeeeeeeeeeeee_iframe"></iframe>'
        ).prependTo("#siteeeeeeeeeeeee");
    } else {
        $('#pdfffffffffffff').css("visibility", "visible")
        $('#pdfffffffffffff').css("height", "540px")
        $('#siteeeeeeeeeeeee').css("height", "0")
    }

});


// // $("body").on("lod", ".pdfobject-com #toolbar", function () {
// //     $('.wordAlert').css("display", "none")
// // });

// $("body").on("mouseover", ".pdfobject-com #toolbar", function () {
//     $('.pdfobject-com #toolbar').show()
// });
// $("body").on("mouseout", ".pdfobject-com #toolbar", function () {
//     $('.wordAlert').hide()
// });




