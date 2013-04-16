

(function ($, undefined) {
    $.fn.getCursorPosition = function() {
        var el = $(this).get(0);
        var pos = 0;
        if('selectionStart' in el) {
            pos = el.selectionStart;
        } else if('selection' in document) {
            el.focus();
            var Sel = document.selection.createRange();
            var SelLength = document.selection.createRange().text.length;
            Sel.moveStart('character', -el.value.length);
            pos = Sel.text.length - SelLength;
        }
        return pos;
    }
})(jQuery);

new function($) {
  $.fn.setCursorPosition = function(pos) {
    if ($(this).get(0).setSelectionRange) {
      $(this).get(0).setSelectionRange(pos, pos);
    } else if ($(this).get(0).createTextRange) {
      var range = $(this).get(0).createTextRange();
      range.collapse(true);
      range.moveEnd('character', pos);
      range.moveStart('character', pos);
      range.select();
    }
  }
}(jQuery);


$(document).ready(function() {
  $('.page-edit').find('.page-edit-controls').css('display', 'block');
});

function pageEditAdd(button, begin, end) {
  var box = $('.page-edit').find('.page-edit-textarea');
  var pos = box.getCursorPosition();

  box.val(box.val().substring(0, pos) + begin + end + box.val().substring(pos));
  
  box.setCursorPosition(pos + begin.length);

}

function pageEditBold(button) {
  pageEditAdd(button, '**', '**');
}
function pageEditItalic(button) {
  pageEditAdd(button, '*', '*');
}
function pageEditUrl(button) {
  //pageEditAdd(button, '*', '*')
  var result = prompt("URL location: ", "http://");
  if (!result) {
    return;
  }
  pageEditAdd(button, '[', '](' + result + ')');
}