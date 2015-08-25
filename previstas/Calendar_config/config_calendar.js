$(document).on('click', '.close', function() {
    $(".over").fadeOut();
});

var events = [ 
    { Title: "Five K for charity", Date: new Date("05/14/2013"), excerpt:"Lorem ipsum dolor sit amet, consectetur adipisicing elit. Amet, culpa, tempora sequi labore dicta"}, 
    { Title: "Dinner", Date: new Date("05/31/2013"), excerpt:"Cena de caridad ble"}, 
    { Title: "Meeting with manager", Date: new Date("05/10/2013"), excerpt:"Cena de caridad ble"}
];

$("#datepicker").datepicker({

    beforeShowDay: function(date) {
        var result = [true, '', null];
        var matching = $.grep(events, function(event) {
            return event.Date.valueOf() === date.valueOf();
        });

        if (matching.length) {
            result = [true, 'highlight', null];
        }
        return result;
    },
    onSelect: function(dateText) {
    var date,
        selectedDate = new Date(dateText),
        i = 0,
        event = null;

        while (i < events.length && !event) {
            date = events[i].Date;

            if (selectedDate.valueOf() === date.valueOf()) {
                event = events[i];
            }
            i++;
        }
            if (event) {
              
                $(".eventdata").empty();
                $(".over").fadeIn("slow");
                $(".eventdata").append("<h1>"+event.Title+"</h1><p>"+event.excerpt+"</p>");
            }
    }

});