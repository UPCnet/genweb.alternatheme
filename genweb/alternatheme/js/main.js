// En aquest script agruparem tots els "document ready" quan sigui necessari

$(document).ready(function () {
  // set a TTL for it (change on production)
  jarn.i18n.setTTL(100000);
  // Load the i18n Plone catalog for genweb
  jarn.i18n.loadCatalog('genweb');
  _gw_i18n = jarn.i18n.MessageFactory('genweb');

  var intervalId = setInterval(function(event) {
     if (window._gw_i18n !== undefined && window._i18nsucks === true) {
         $('[type=file]').each(function(index, value) {
             $(value).customFileInput();
         });

         clearInterval(intervalId);
     }
  }, 50);

  // $('select:not([multiple])').dropkick();
  $('ul.dk_options_inner').addClass('scrollable');
  if ($(window).width() < 640 ) {
    /* aquestes dues classes que s'afegeixen són necessàries? aparentment funciona igual i llavors funciona bé la vista beta
    $('.nav-tabs').addClass('nav-stacked');
    $('.nav-pills').addClass('nav-stacked'); */
    $(document).scrollTop( $("#content").offset().top ); //aquí saltava un error perquè faltava '#'
  }
  $('.custom-chekbox[type="checkbox"]').customInput();
  $('.custom-radio[type="radio"]').customInput();

  $('[rel="tooltip"]').tooltip({container: 'body'});
  $('[rel="popover"]').popover();
  $(document).on('touchend click', '.amunt a', function() {
    $("html, body").animate({ scrollTop: 0 }, 'slow');
  });
  $('.dropdown:has(.badge)').addClass('nou');
  $('ul.dropdown-menu li:has(.actionMenuSelected)').addClass('active');

  $('.userScreen').click(function() {
    $('html').removeClass('simulated-mobile-view');
    $('html').removeClass('simulated-tablet-view');
    $("#content").getNiceScroll().hide();
    $("#content").css({ overflow: "visible" }); //fixa bug de l'scroll
  });
  $('.userTablet').click(function() {
    $("#content").css({ overflow: "hidden" }); //fixa bug de l'scroll
    $('html').removeClass('simulated-mobile-view');
    $('html').addClass('simulated-tablet-view');
    $("html.simulated-tablet-view #content").niceScroll({touchbehavior:false,cursorcolor:"#000",cursoropacitymax:0.75,cursoropacitymin: 0.25,cursorwidth:6});
    $("html.simulated-tablet-view #content").getNiceScroll().show();
    $("#content").getNiceScroll().resize();
  });
  $('.userMobile').click(function() {
    $("#content").css({ overflow: "hidden" }); //fixa bug de l'scroll
    $('html').removeClass('simulated-tablet-view');
    $('html').addClass('simulated-mobile-view');
    $("html.simulated-mobile-view #content").niceScroll({touchbehavior:false,cursorcolor:"#000",cursoropacitymax:0.75,cursoropacitymin: 0.25,cursorwidth:6});
    $("html.simulated-mobile-view #content").getNiceScroll().show();
    $("#content").getNiceScroll().resize();
  });

  var prettify = false;
  $("pre").each(function() {
      $(this).prepend('<code>');
      $(this).append('</code>');
      $(this).addClass('prettyprint linenums');
      prettify = true;
  });

  if ( prettify ) {
      $.getScript("/++genweb++static/js/prettify.js", function() {prettyPrint()});
  }


// Live search

 $("#cercaCapca").typeahead({
   source: function (query, process) {
      setTimeout(searchElements(query, process) , 300);
   },
   highlighter: function(item){
      var iitem = $("#cercaCapca").get(0).results[item];
      //info = items[item.split("#")[0]];
      var itm = "<i class='icon-"+iitem.icon+"'></i> " +
                 iitem.title +
                "<p class='xs margin0'>"+iitem.description+"</p>";
      return itm;
  },
  matcher: function (item) {
      return true;
  },
  updater: function(item) {
      window.location.href = $("#cercaCapca").get(0).results[item]['itemUrl'];
  },
  items: 12,
  minLength: 2
  });

 var searchElements = function( query, process ){
     $.get(document.getElementsByTagName('base')[0].href+"/typeaheadJson", { q: query }, function(data) {
          //Reseting containers
          var items = [];

          $.each(data, function(index, value) {
              items.push(index.toString());
          });
          $("#cercaCapca").get(0).results = data;
          process(items);
    });
 };

// actualització títol menú 1, mostra l'opció de primer nivell que hem seleccionat, es fa a partir del 2on valor de la llista del breadcrumb
  var lititol=$('ol.breadcrumb li:eq(1) a');// cas amb breadcrumb no visible
  if (lititol.length===0) lititol=$('ol.breadcrumb li:eq(1)');// cas amb breadcrumb visible
  var nouTitol=lititol.text();
  if (nouTitol) $('#titol-menu-1 a').text(nouTitol);

// actualització títol menú 2, mostra l'opció de primer nivell que hem seleccionat, es fa a partir del 3er valor de la llista del breadcrumb
/*  var lititol=$('ol.breadcrumb li:eq(2) a');// cas amb breadcrumb no visible
  if (lititol.length===0) lititol=$('ol.breadcrumb li:eq(2)');// cas amb breadcrumb visible
  var nouTitol=lititol.text();
  if (nouTitol) $('#titol-menu-2').text(nouTitol);*/


// RECAPTCHA
  if (window.hasOwnProperty('RecaptchaOptions')) {
    if (RecaptchaOptions !== undefined) {
      var translations = RecaptchaOptions['custom_translations'];
      $('div.recaptcha_only_if_incorrect_sol').text(translations['incorrect_try_again']);
      $('li.recaptcha_play_again span').text(translations['refresh_btn']);
      $('#recaptcha_reload').attr('alt',translations['refresh_btn']);
      $('a.recaptcha_only_if_image span').text(translations['audio_challenge']);
      $('#recaptcha_switch_audio').attr('alt',translations['audio_challenge']);
      $('a.recaptcha_only_if_audio span').text(translations['visual_challenge']);
      $('#recaptcha_switch_img').attr('alt',translations['visual_challenge']);
      $('li.recaptcha_help span').text(translations['help_btn']);
      $('#recaptcha_whatsthis').attr('alt',translations['help_btn']);

      input_text_default('audio');

      $('#recaptcha_switch_type').click(
        function(){
          input_text_default(Recaptcha['type']);
        }
      );
    }
  }

  function input_text_default(captcha_type){
    var text_default="";
    if (captcha_type==='image')  {
      text_default=translations['instructions_audio'];
    } else {
      text_default=translations['instructions_visual'];
    }
    $('#recaptcha_response_field').val(text_default);

  }
  // FI RECAPTCHA

  // Share popover specific
  $('.share_popover').popover({
      html:true,
      placement:'left',
      content:function(){
          return $($(this).data('contentwrapper')).html();
      }
  });

}); // End of $(document).ready

// Token input z3c.form widget
function keywordTokenInputActivate(id, newValues, oldValues) {
  $('#'+id).tokenInput(newValues, {
      theme: "facebook",
      tokenDelimiter: "\n",
      tokenValue: "name",
      preventDuplicates: true,
      prePopulate: oldValues
  });
}
