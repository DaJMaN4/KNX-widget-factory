$(function() {
  $('.color_tekst_knx').each(function(_, el) { 
    var addr = $(el).data('object');
    if (addr) {
      grp.listen(addr, function(obj) {
        var value = obj.value, color = 'black'; // default color

        if (value == true) {
           color = "Green";
        }
        else if (value == false) {
          color = "Red";
        }

       // $(el).css('border-color', color);
        $(el).css('color', color);
        //$(el).css('hsla', '1%', '1%', '1%', '0');
        //$(el).css('border-style', 'solid');
        //$(el).css('border-radius', '3px');
        //$(el).css('margin-top', '-2px');
        //$(el).css('border-width', '5px');
        //$(el).css('border-width', '5px');
      });
    }
  });
});



$(function() {
  $('.color_termostatmodus').each(function(_, el) { 
    var addr = $(el).data('object');
    if (addr) {
      grp.listen(addr, function(obj) {
        var value = obj.value, color = 'black'; // default color

        if (value == true) {
           color = "Red";
        }
        else if (value == false) {
          color = "Blue";
        }

       // $(el).css('border-color', color);
        $(el).css('color', color);
        //$(el).css('hsla', '1%', '1%', '1%', '0');
        //$(el).css('border-style', 'solid');
        //$(el).css('border-radius', '3px');
        //$(el).css('margin-top', '-2px');
        //$(el).css('border-width', '5px');
        //$(el).css('border-width', '5px');
      });
    }
  });
});



$(function() {
  $('.color-by-value').each(function(_, el) {
    var value_grense1 = grp.getvalue('40/7/1');//blue
    var value_grense2 = grp.getvalue('40/7/2');//green
    var value_farge1 = grp.getvalue('40/7/11');//blue
    var value_farge2 = grp.getvalue('40/7/12');//green
    var value_farge3 = grp.getvalue('40/7/13');//orange
    
    
    var addr = $(el).data('object');
    if (addr) {
      grp.listen(addr, function(obj) {
        var value = obj.value, color = 'black';

        if (value < value_grense1) {
           color = "#"+ value_farge1.toString(16);
        }
        else if (value >= value_grense1 && value <= value_grense2) {
          color = "#"+ value_farge2.toString(16);
          }
				else if (value > value_grense2) {
          color = "#"+ value_farge3.toString(16);
        }
        $(el).css('border-color', color);
        $(el).css('background-color', color);
        $(el).css('border-style', 'solid');
        $(el).css('border-radius', '3px');
      });
    }
  });
});



$(function() {
  $('.color-nattsenk').each(function(_, el) { 
    var addr = $(el).data('object');
    if (addr) {
      grp.listen(addr, function(obj) {
        var value = obj.value, color = 'black'; // default color

        if (value == 0) {
           color = "Gray";
          colorb = "Transparent";
        }
        else if (value == 1) {
          color = "White";
          colorb = "Red";
        }
        $(el).css('border-color', colorb);
        $(el).css('color', color);
        //$(el).css('hsla', '1%', '1%', '1%', '0');
        $(el).css('border-style', 'solid');
        $(el).css('border-radius', '3px');
        $(el).css('margin-top', '-2px');
        $(el).css('border-width', '5px');
        $(el).css('border-width', '5px');
        $(el).css('background-color', colorb);
      });
    }
  });
});
