function getToday(){
    var currentDate = new Date();    
//    var dd = currentDate.getDate();
//    day = ("0" + dd).slice(-2);
//    var mm = currentDate.getMonth() + 1;
//    mo = [ "January", "February", "March", "April", "May", "June",
//    "July", "August", "September", "October", "November", "December" ][mm]
//    var yyyy = currentDate.getFullYear();
//    today = day + '/' + mo + '/' + yyyy;
    today = currentDate.toString('dd/mm/yyyy')
    return today;
}

function getTomorrow(){
    var currentDate = new Date();    
    var nextDate = new Date(currentDate.getTime() + (24 * 60 * 60 * 1000));
    var dd = nextDate.getDate();
    day = ("0" + dd).slice(-2);
    var mm = nextDate.getMonth() + 1;
    mo = ("0" + mm).slice(-2);
    var yyyy = nextDate.getFullYear();
    tomorrow = day + '/' + mo + '/' + yyyy;
    return tomorrow;
}