// JavaScript to handle mouseover and mouseout events
var activeMethodPill = null;
var activeScenePill = null;
var activeModePill = null;
var activeVidID = 0;
var select = false;
var activeMethodPillHandwrite = null;
var activeScenePillHandwrite = null;
var activeModePillHandwrite = null;
var activeVidIDHandwrite = 0;
var activeMethodPillDynamic = null;
var activeScenePillDynamic = null;
var activeModePillDynamic = null;
var activeVidIDDynamic = 0;


$(document).ready(function () {
    var editor = CodeMirror.fromTextArea(document.getElementById("bibtex"), {
        lineNumbers: false,
        lineWrapping: true,
        readOnly: true
    });
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });

    activeMethodPill = $('.method-pill').filter('.active')[0];
    activeModePill = $('.mode-pill').filter('.active')[0];
    activeScenePill = $('.scene-pill').filter('.active')[0];
    activeMethodPillHandwrite = $('.method-pill-handwrite').filter('.active')[0];
    activeModePillHandwrite = $('.mode-pill-handwrite').filter('.active')[0];
    activeScenePillHandwrite = $('.scene-pill-handwrite').filter('.active')[0];
    activeMethodPillDynamic = $('.method-pill-dynamic').filter('.active')[0];
    activeModePillDynamic = $('.mode-pill-dynamic').filter('.active')[0];
    activeScenePillDynamic = $('.scene-pill-dynamic').filter('.active')[0];

    resizeAndPlay($('#sparsity')[0]);
});

function selectCompVideo(task, methodPill, scenePill, n_views, modePill) {
    // Your existing logic for video selection
    // var video = document.getElementById("compVideo");
    select = true;
    var videoSwitch = document.getElementById("compVideoSwitch");
    var textPrompt = document.getElementById("textPrompt");

    if (activeMethodPill) {
        activeMethodPill.classList.remove("active");
    }
    if (activeScenePill) {
        activeScenePill.classList.remove("active");
    }
    if (modePill) {
        activeModePill.classList.remove("active");
        modePill.classList.add("active");
        activeModePill = modePill;
    }
    activeMethodPill = methodPill;
    activeScenePill = scenePill;
    methodPill.classList.add("active");
    scenePill.classList.add("active");
    method = methodPill.getAttribute("data-value");
    pill = scenePill.getAttribute("data-value");
    mode = activeModePill.getAttribute("data-value");

    if (pill == 'bear') {
        textPrompt.innerHTML = '<strong>A Van Gogh-style cartoon bear walking in the forest.</strong>';
    } else if (pill == 'overlook-the-ocean') {
        textPrompt.innerHTML = '<strong>Top-down view of waves crashing against a rocky shore with turquoise waters, Cartoonish and Lighthearted Animation.</strong>';
    } else if (pill == 'shark-ocean') {
        textPrompt.innerHTML = '<strong>A sleek shark glides through clear waters, accompanied by a myriad of other fish, illuminated by the shimmering light from above, rendered in a dreamy pastel style.</strong>';
    } else if (pill == 'hot-air-ballon') {
        textPrompt.innerHTML = '<strong>Hot air balloons adrift over an ancient desert, Chibi Animation style.</strong>';
    } else if (pill == 'boat') {
        textPrompt.innerHTML = '<strong>A fishing boat sails near the coast, Chibi Animation style.</strong>';
    } 

    // if (videoSwitch.checked) {
    //     mode = 'depth'
    // } else {
    //     mode = 'rgb'
    // }

    // swap video to avoid flickering
    activeVidID = 1 - activeVidID;
    var video_active = document.getElementById("compVideo" + activeVidID);
    var video_hidden = document.getElementById("compVideo" + (1 - activeVidID));
    video_active.src = "videos/" + task + "_" + pill + "_" + method + "_vs_ours_" + mode + ".mp4";
    video_active.load();
}

function selectCompVideoHandwrite(task, methodPillHandwrite, scenePillHandwrite, n_views, modePillHandwrite) {
    // Your existing logic for video selection
    // var video = document.getElementById("compVideo");
    select = true;
    var videoSwitch = document.getElementById("compVideoSwitch");
    var textPrompt = document.getElementById("textPrompt");

    if (activeMethodPillHandwrite) {
        activeMethodPillHandwrite.classList.remove("active");
    }
    if (activeScenePillHandwrite) {
        activeScenePillHandwrite.classList.remove("active");
    }
    if (modePillHandwrite) {
        activeModePillHandwrite.classList.remove("active");
        modePillHandwrite.classList.add("active");
        activeModePillHandwrite = modePillHandwrite;
    }
    activeMethodPillHandwrite = methodPillHandwrite;
    activeScenePillHandwrite = scenePillHandwrite;
    methodPillHandwrite.classList.add("active");
    scenePillHandwrite.classList.add("active");
    method = methodPillHandwrite.getAttribute("data-value");
    pill = scenePillHandwrite.getAttribute("data-value");
    mode = activeModePillHandwrite.getAttribute("data-value");

    // if (pill == 'dtu_scan45') {
    //     textPrompt.innerHTML = 'A camel walking in an enclosure with a wooden fence and greenery in the background, Minecraft world style.';
    // } else if (pill == 'llff_fern') {
    //     textPrompt.innerHTML = 'Hot air balloons adrift over an ancient desert, Chibi Animation style.';
    // } else {
    //     textPrompt.innerHTML = 'sdfjiosdhfiusdhf';
    // }

    // if (videoSwitch.checked) {
    //     mode = 'depth'
    // } else {
    //     mode = 'rgb'
    // }

    // swap video to avoid flickering
    activeVidIDHandwrite = 1 - activeVidIDHandwrite;
    var video_active = document.getElementById("compVideo0_handwrite");
    var video_hidden = document.getElementById("compVideo" + (1 - activeVidID));
    video_active.src = "videos/" + task + "_" + pill + "_" + method + "_vs_ours_" + mode + ".mp4";
    video_active.load();
}

function selectCompVideoDynamic(task, methodPillDynamic, scenePillDynamic, n_views, modePillDynamic) {
    // Your existing logic for video selection
    // var video = document.getElementById("compVideo");
    select = true;
    var videoSwitch = document.getElementById("compVideoSwitch");
    var textPrompt = document.getElementById("textPrompt");

    if (activeMethodPillDynamic) {
        activeMethodPillDynamic.classList.remove("active");
    }
    if (activeScenePillDynamic) {
        activeScenePillDynamic.classList.remove("active");
    }
    if (modePillDynamic) {
        activeModePillDynamic.classList.remove("active");
        modePillDynamic.classList.add("active");
        activeModePillDynamic = modePillDynamic;
    }
    activeMethodPillDynamic = methodPillDynamic;
    activeScenePillDynamic = scenePillDynamic;
    methodPillDynamic.classList.add("active");
    scenePillDynamic.classList.add("active");
    method = methodPillDynamic.getAttribute("data-value");
    pill = scenePillDynamic.getAttribute("data-value");
    mode = activeModePillDynamic.getAttribute("data-value");

    // if (pill == 'dtu_scan45') {
    //     textPrompt.innerHTML = 'A camel walking in an enclosure with a wooden fence and greenery in the background, Minecraft world style.';
    // } else if (pill == 'llff_fern') {
    //     textPrompt.innerHTML = 'Hot air balloons adrift over an ancient desert, Chibi Animation style.';
    // } else {
    //     textPrompt.innerHTML = 'sdfjiosdhfiusdhf';
    // }

    // if (videoSwitch.checked) {
    //     mode = 'depth'
    // } else {
    //     mode = 'rgb'
    // }

    // swap video to avoid flickering
    activeVidIDDynamic = 1 - activeVidIDDynamic;
    var video_active = document.getElementById("compVideo0_dynamic");
    var video_hidden = document.getElementById("compVideo" + (1 - activeVidID));
    video_active.src = "videos/" + task + "_" + pill + "_" + method + "_vs_ours_" + mode + ".mp4";
    video_active.load();
}