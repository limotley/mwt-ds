﻿$(function () {
    $.ajaxSetup({ cache: false });


    // create the editor
    var container = document.getElementById("jsoneditor");
    var options = {
        mode: 'code',
        modes: ['code', 'tree'], // allowed modes
    };
    var editor = new JSONEditor(container, options);

    // set json
    /*
    var json = {
        "Age": 25,
        "Location": "New York",
        _multi: [
            {"a":1},
            { "a": 2 }
        ]
    };
    */
    var json = {
        "Age": 25,
        "Location": "New York",
        "Industry": "Tech"
    };
    editor.set(json);

    $(".Hostname").text(window.location.hostname);

    var lastJson = "";
    setInterval(function () {
        var userToken = $("#userToken").val();
        if (userToken != null && userToken.length > 0) {

            var newJson = editor.getText();
            if (lastJson == newJson)
                return;

            $.ajax({
                url: "/API/Validate/",
                headers: { 'auth': userToken },
                type: "POST",
                data: newJson,
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                cache: false,
                success: function (data) {
                    lastJson = newJson;
                    $("#vwstr").html("<pre>" + data.VWExample + "</pre>");
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    $("#vwstr").html("Invalid JSON structure.");
                }
            });
        }
    }, 500);

    function SubmitInteraction() {
        // Get Decision
        $.ajax({
            method: "POST",
            url: "/API/Policy",
            data: editor.getText(),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            cache: false,
            headers: {
                'auth': $("#userToken").val()
            },
        })
        .done(function (data) {
            $("#chosenAction").text(data.Action)
            $("#EventId").text(data.EventId);
            $("#rewardEventId").text(data.EventId);
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            $("#status").text("Error posting ineraction: " + textStatus + "  " + errorThrown);
        });
    }

    function SubmitObservation() {
        $.ajax({
            method: "POST",
            url: "/API/Reward/?eventId=" + $("#EventId").text(),
            data: $("#rewardInput").val(),
            headers: {
                'auth': $("#userToken").val()
            },
            cache: false,
        })
        .done(function (data) {
            $("#statusReward").text("Successfully sent reward of " + $("#rewardInput").val());
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            $("#status").text("Error sending reward: " + textStatus + "  " + errorThrown);
        });
    }

    $('#submit-interaction').click(SubmitInteraction);
    $('#submit-observation').click(SubmitObservation)
})