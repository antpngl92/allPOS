function showDate(d){
  var month = d.getMonth();
  var date  = d.getDate();
  var day   = d.getDay();

  var week_days = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4:'Thursday', 5: 'Friday', 6:'Saturday', 7:'Sunday'};
  const month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
  var today = week_days[day] + ", " + month_names[month] + " " + date;
  $('#date').html(today)

}
function showTime() {
    var date = new Date()
    var h = date.getHours(); 
    var m = date.getMinutes();

    h = (h < 10) ? "0" + h : h;
    m = (m < 10) ? "0" + m : m;
    var time = h + ":" + m
    $('#time').html(time)
    showDate(date);
    setTimeout(showTime, 1000);
  }
  showTime();